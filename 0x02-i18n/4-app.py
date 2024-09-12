#!/usr/bin/env python3
"""
4-app.py
This module sets up a Flask app with Babel for internationalization
and localization.
It includes functionality to detect and set locale from URL parameters.
"""

from flask import Flask, request, render_template
from flask_babel import Babel, _


app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app)


#@babel.localeselector
def get_locale() -> str:
    """
    Determine the best match with the supported languages.
    Check for a locale parameter in the URL. If present and supported, use it.
    Otherwise, use the default locale.
    """
    locale_param = request.args.get('locale')
    print(f"Locale parameter: {locale_param}")
    if locale_param and locale_param in ['en', 'fr']:
        return locale_param
    default_locale = request.accept_languages.best_match(['en', 'fr'])
    print(f"Returning default locale: {default_locale}")
    return default_locale

@app.route('/')
def index() -> str:
    """
    Render the index page with localized content.
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(debug=True)
