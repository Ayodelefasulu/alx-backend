#!/usr/bin/env python3
"""
A simple Flask app that detects the browser locale.
"""

from flask import Flask, request, render_template
from flask_babel import Babel, get_locale

app = Flask(__name__)

# Configuration for supported languages


class Config:
    LANGUAGES = ['en', 'fr']  # English and French
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


@app.route('/')
def index():
    """
    Renders the index page, which will display in the detected language.

    :return: Rendered template for index page.
    """
    return render_template('3-index.html')


@app.context_processor
def inject_locale():
    """
    Returns the default browser language setting
    """
    return {'get_locale': get_locale}


if __name__ == "__main__":
    app.run(debug=True)
