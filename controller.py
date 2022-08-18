"""
Route management.

This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML static
to be displayed.

"""

import flask
from flask import *
import model

"may be useful when the name of 'static' and 'templates' files change"
# app = flask.Flask(__name__, template_folder='templates', static_folder='static')

app = flask.Flask(__name__)


@app.route('/')
def introduction_page():
    """ Here is the route for index page """
    return render_template('index.html')
