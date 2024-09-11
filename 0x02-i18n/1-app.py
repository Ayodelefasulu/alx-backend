#!/usr/bin/env python3
"""
Flask app that demonstrates language translation using Flask-Babel.
"""

from flask import Flask, render_template
from flask_babel import Babel
import os


class Config:
    """
    Configuration class for Flask app.
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'


app: Flask = Flask(__name__)
app.config.from_object(Config)

# Instantiate Babel
babel: Babel = Babel(app)


@app.route('/')
def index() -> str:
    """
    Render the index page with a simple header.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)
