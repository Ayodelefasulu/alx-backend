#!/usr/bin/env python3
"""
6-app.py
This module sets up a Flask app with Babel for internationalization
and localization. It includes functionality to detect and set locale
from URL parameters, user settings, request headers, and defaults.
"""

from flask import Flask, request, render_template, g
from flask_babel import Babel, get_locale

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> dict:
    """
    Retrieve a user from the mock database based on login_as URL parameter.
    """
    user_id = request.args.get('login_as', type=int)
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """
    Set the global user on flask.g based on login_as URL parameter.
    """
    g.user = get_user()


#@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match with the supported languages.
    Check for a locale parameter in the URL, user settings, request headers,
    and fallback to the default locale.
    """
    """ locale_param = request.args.get('locale')
    if locale_param and locale_param in ['en', 'fr']:
        return locale_param

    user_locale = getattr(g, 'user', {}).get('locale')
    if user_locale and user_locale in ['en', 'fr']:
        return user_locale

    return request.accept_languages.best_match(['en', 'fr'])
    """
    locale_param = request.args.get('locale')
    if locale_param in ['en', 'fr']:
        return locale_param
    if g.user and g.user['locale'] in ['en', 'fr']:
        return g.user['locale']
    return request.accept_languages.best_match(['en', 'fr'])

@app.route('/')
def index() -> str:
    """
    Render the index page with localized content.
    """
    return render_template('6-index.html')

@app.context_processor
def inject_locale() -> str:
    """
    Returns the default browser language setting
    """
    return {'get_locale': get_locale}


if __name__ == '__main__':
    app.run(debug=True)