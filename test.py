from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):
  # TODO -- write tests for every view function / feature!
    def setUP(self):
        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_homepage(self):
        """make sure the session has the information and the HTML is live"""
        with self.client:
            res = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('num_plays'))
            self.assertIn(b'<p>High Score:', res.data)
            self.assertIn(b'Score:'. res.data)
            self.assertIn(b"Seconds Left:", res.data)

    def test_valid_word(self):
        """is the word valid """
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [["T", "H", "A", "T", "T"],
                                    ["T", "H", "A", "T", "T"],
                                    ["T", "H", "A", "T", "T"],
                                    ["T", "H", "A", "T", "T"],
                                    ["T", "H", "A", "T", "T"]]

        response = self.client.get('/check-word?word = that')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """see if word is in the dictionary"""
        self.client.get("/")
        response = self.client.get('/check-word?word=impossible')
        self.assertEqual(response.json['result'], 'not-on-board')

    def not_english_word(self):
        """Test if word is on board """
        self.client.get('/')
        res = self.client.get('/check-word?word=akjdflkjasldkfj')
        self.assertEqual(res.json['result'], 'not-a-word')
