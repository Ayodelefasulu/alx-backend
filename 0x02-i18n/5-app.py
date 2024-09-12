#!/usr/bin/env python3
"""
5-app.py
This module sets up a Flask app with Babel for internationalization
and localization. It includes functionality to mock user login and
set locale based on user preference or default settings.
"""

from flask import Flask, request, render_template, g
from flask_babel import Babel, get_locale

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> dict:
    """
    Retrieve user from mock user table based on 'login_as' parameter.
    Returns a user dictionary if ID is valid, else returns None.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Set global user before handling requests based on 'login_as' parameter.
    """
    g.user = get_user()


#@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match with the supported languages.
    Check for a locale parameter in the URL or user settings.
    """
    locale_param = request.args.get('locale')
    if locale_param and locale_param in ['en', 'fr']:
        return locale_param
    if g.user and g.user['locale']:
        return g.user['locale']
    return request.accept_languages.best_match(['en', 'fr'])


@app.route('/')
def index() -> str:
    """
    Render the index page with localized content.
    """
    return render_template('5-index.html')

@app.context_processor
def inject_locale() -> str:
    """
    Returns the default browser language setting
    """
    return {'get_locale': get_locale}


if __name__ == '__main__':
    app.run(debug=True)
