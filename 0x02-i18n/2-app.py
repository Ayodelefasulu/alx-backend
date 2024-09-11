#!/usr/bin/env python3
"""
Flask application that demonstrates language selection using Flask-Babel.
"""

from flask import Flask, render_template, request
from flask_babel import Babel

# Initialize Flask app
app: Flask = Flask(__name__)

# Configuration class


class Config:
    """
    Configuration class for Flask app, including supported languages.
    """
    LANGUAGES = ['en', 'fr']  # Supported languages
    BABEL_DEFAULT_LOCALE = 'en'  # Default locale
    BABEL_DEFAULT_TIMEZONE = 'UTC'  # Default timezone


app.config.from_object(Config)

# Initialize Babel
babel: Babel = Babel(app)


#@babel.localeselector
def get_locale() -> str:
    """
    Select the best language match from the request's Accept-Language headers.

    :return: The best matching locale from the supported languages.
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Render the index page.

    :return: Rendered index.html template.
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run(debug=True)
