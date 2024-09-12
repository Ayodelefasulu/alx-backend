#!/usr/bin/env python3
"""
7-app.py
This module sets up a Flask app with Babel for internationalization
and localization, including time zone management.
It includes functionality to detect and set time zone from URL parameters
and user settings.
"""

from flask import Flask, request, g, render_template
from flask_babel import Babel, get_locale
import pytz

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
babel = Babel(app)


#@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match with the supported languages.
    Check for a locale parameter in the URL, user settings,
    request headers, and use the default locale if none found.
    """
    locale_param = request.args.get('locale')
    if locale_param in ['en', 'fr']:
        return locale_param
    if g.user and g.user.get('locale') in ['en', 'fr']:
        return g.user['locale']
    return request.accept_languages.best_match(['en', 'fr'])


#@babel.timezoneselector
def get_timezone() -> str:
    """
    Determine the best match for the time zone.
    Check for a time zone parameter in the URL, user settings,
    and use the default time zone if none found. Validate time zones.
    """
    timezone_param = request.args.get('timezone')
    if timezone_param:
        try:
            pytz.timezone(timezone_param)
            return timezone_param
        except pytz.UnknownTimeZoneError:
            pass
    if g.user and g.user.get('timezone'):
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request():
    """
    Set the user for the current request if login_as is provided.
    """
    user_id = request.args.get('login_as')
    if user_id and user_id.isdigit():
        user_id = int(user_id)
        g.user = users.get(user_id)
    else:
        g.user = None


@app.route('/')
def index() -> str:
    """
    Render the index page with localized content and time zone information.
    """
    return render_template('7-index.html', timezone=get_timezone())

@app.context_processor
def inject_locale() -> str:
    """
    Returns the default browser language setting
    """
    return {'get_locale': get_locale}

if __name__ == '__main__':
    app.run(debug=True)
