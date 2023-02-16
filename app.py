from boggle import Boggle
from flask import Flask, session, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "winner123"

boggle_game = Boggle()


@app.route('/')
def make_boggle_board():
    """create boggle board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get('highscore', 0)
    num_plays = session.get("num_plays", 0)

    return render_template("base.html", board=board, highscore=highscore, num_plays=num_plays)


@app.route('/check-word')
def check_word():
    """see if word is in dictionary"""
    word = request.args['word']
    board = session['board']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route('/post-score', methods=["POST"])
def post_score():
    """Get a score, number of plays, and update when neccessary"""
    score = request.json['score']
    highscore = session.get('highscore', 0)
    num_plays = session.get('num_plays', 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newHighscore=score > highscore)
