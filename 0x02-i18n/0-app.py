#!/usr/bin/env python3
"""
A basic Flask app that serves an index page.
"""

from flask import Flask, render_template

app: Flask = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Renders the index page with the 'Hello world' header.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)
