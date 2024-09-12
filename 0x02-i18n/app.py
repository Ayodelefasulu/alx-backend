#!/usr/bin/env python3
"""
7-app.py
This module sets up a Flask app with Babel for
internationalization and localization.
It includes functionality to detect and set locale and
timezone from URL parameters or user settings.
"""

from flask import Flask, request, render_template, g
from flask_babel import Babel, _
import pytz
from datetime import datetime
from typing import Optional

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[dict]:
    """
    Retrieve user information based on 'login_as' parameter in request URL.

    Returns:
        dict: User information if the user ID is valid; None otherwise.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Set a global user on 'flask.g' based on the 'get_user' function.
    """
    g.user = get_user()


#@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match with the supported languages.

    Checks for a locale parameter in URL, user settings, & request headers.
    Defaults to 'en' if no match is found.

    Returns:
        str: The locale to use.
    """
    locale_param = request.args.get('locale')
    if locale_param in ['en', 'fr']:
        return locale_param

    if getattr(g, 'user', None) and g.user.get('locale') in ['en', 'fr']:
        return g.user['locale']

    return request.accept_languages.best_match(['en', 'fr'])


#@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the best match with the supported time zones.

    Checks for a timezone parameter in URL, user settings,
    and defaults to 'UTC'.
    Validates the timezone to ensure it is supported.

    Returns:
        str: The timezone to use.
    """
    timezone_param = request.args.get('timezone')
    if timezone_param:
        try:
            pytz.timezone(timezone_param)
            return timezone_param
        except pytz.UnknownTimeZoneError:
            return 'UTC'

    if getattr(g, 'user', None) and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.UnknownTimeZoneError:
            return 'UTC'

    return 'UTC'


@app.route('/')
def index() -> str:
    """
    Render the index page with localized content and
    the current time based on the inferred timezone.

    Returns:
        str: Rendered HTML template.
    """
    tz = get_timezone()
    current_time = datetime.now(pytz.timezone(
        tz)).strftime('%b %d, %Y, %I:%M:%S %p')
    return render_template('7-index.html', current_time=current_time)


@app.context_processor
def inject_locale() -> str:
    """
    Returns the default browser language setting
    """
    return {'get_locale': get_locale}


if __name__ == '__main__':
    app.run(debug=True)
