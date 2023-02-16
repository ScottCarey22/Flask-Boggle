class BoggleGame {
    // new game
    constructor(boardId, secs = 60) {
        this.secs = secs;
        this.displayTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);
        this.timer = setInterval(this.tick.bind(this), 1000);
        // tick every second as a count down
        $(".add-word", this.board).on("submit", this.handleSubmit.bind((this)))
    }
    // list of picked words
    showWord(word) {
        $(".words", this.board).append($("<ul>", { text: word }));
    }



    // show score 
    showMessage(msg, cls) {
        $('.msg', this.board)
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`)
    }
    // handle the submission of words
    async handleSubmit(e) {
        e.preventDefault();
        const $word = $('.word', this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`${word} was already used`, "err");
            return
        }
        // check server for validity
        const res = await axios.get("/check-word", { params: { word: word } });
        if (res.data.result === "not-word") {
            this.showMessage(`${word} is not a valid English word`, "err");
        } else if (res.data.result === "not-on-board") {
            this.showMessage(`${word} is not a valid word on this board`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.endGame();
            this.words.add(word);
            this.showMessage(`Added: ${word}`, "ok");
        }

        $word.val("").focus();
    }

    // timer
    displayTimer() {
        $(".timer", this.board).text(this.secs);
    }

    // countdown
    async tick() {
        this.secs -= 1;
        this.displayTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.endGame();
        }
    }

    // end game: calculate score
    async endGame() {
        $('.add-word', this.board).hide();
        const res = await axios.post("/post-score", { score: this.score });
        if (res.data.newHighscore) {
            this.showMessage(`NEW HIGHSCORE: ${this.score}`, "ok");
        }
        else {
            this.showMessage(`Your Score was ${this.score}`, "ok")
        }
    }
}
