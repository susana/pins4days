# -*- coding: utf-8 -*-
"""Entry point for the Pins4Days app that runs on Google App Engine (standard).

This app utilizes:
- Flask framework
- flask-login for user session management
- NDB client library for connecting to Google Cloud Datastore (NoSQL!), and
storing pins and user info.
- Google Cloud Storage (GCS) for storing configs
- Memcache for session storage

Attributes:
    app (obj): Flask app.
    config (AppConfig): An object that handles reading in configs from GCS.
    These configs are inserted into app.config and made available to the Flask
    app.
    login_manager (LoginManager): User session manager.

Todo:
    * Handle duplicate user creation in signup().
    * Investigate possible exceptions for User creation and add exception
    handling to signup().
    * Handle pagination, aka return more than 10 pins from the /pins view and
    /api/pins endpoint!
    * Read in existing pins and store them.
    * Add auth to GET /api/pins.
"""

import logging

from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from flask import make_response
from flask import url_for
from flask import render_template
from flask_login import login_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import current_user
from werkzeug.contrib.cache import MemcachedCache

from pins4days.constants import KEY_FLASK_APP_CONFIG
from pins4days.constants import KEY_FLASK_SECRET_KEY
from pins4days.utils import load_config
from pins4days.event import PinnedMessage
from pins4days.models.pin import Pin
from pins4days.models.user import User
from pins4days.models.exceptions import EntityDoesNotExistException
from pins4days.models.exceptions import IncorrectPasswordException
from pins4days.appuser import AppUser


app = Flask(__name__)
config = load_config()
app.config.update(config[KEY_FLASK_APP_CONFIG])
app.config['SESSION_TYPE'] = 'memcached'
app.config['SESSION_MEMCACHED'] = MemcachedCache()
app.secret_key = config[KEY_FLASK_SECRET_KEY]
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(username):
    """Loads a User model instance based on their unique username.

    Args:
        username (str): The user's username which they created upon sign up.

    Returns:
        AppUser or None: Returns an AppUser if the User exists in the DB.
        Returns None if the user does not exist.
    """
    user = User.get_by_id(username)
    return AppUser(user) if user else None


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    """Handles user sign up. This requires that the user create a unique
    username, and a password.

    If the user is already logged in, redirect them to the main /pins page.
    If the user is not logged in, show them the signup form.
    If they've submitted the signup form, create a new user, and then redirect
    them to the /login page.

    Returns:
        Response: See flow described above.
    """
    if current_user.is_authenticated:
        return redirect(url_for('pins'))

    if request.method == 'GET':
        return render_template('signup.html')

    username = request.form['username']
    password = request.form['password']

    User.init_with_encryption(id=username, password=password)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs in user, creating a session in memcache.

    If the user is already logged in, redirect them the /pins page.
    If the user is not logged in, show them the login form. See
    handle_login_post() for more details on this step..

    Returns:
        Response: See flow described above.
    """
    if current_user.is_authenticated:
        return redirect(url_for('pins'))

    if request.method == 'GET':
        return render_template('login.html')

    return handle_login_post(request)


def handle_login_post(request):
    """Validates user form data and logs in user.

    If the form is submitted with invalid inputs, show the error template.
    If the user attempts to log in as a user that does not exist, show the error
    template.
    If the user attempts to log in with an existing username and incorrect
    password, show the error template.
    Otherwise, if the form was valid and the username exists with the correct
    password submitted, that user is logged in, and redirected to the /pins
    page.


    Args:
        request (Request): HTTP request.

    Returns:
        Response:
    """
    if not validate_form(request.form):
        return make_response(
            render_template('login.html', error='E_BAD_FORM'), 400)

    try:
        user = User.login(request.form['username'], request.form['password'])
        app_user = AppUser(user)
        if app_user:
            login_user(app_user)
            return redirect(url_for('pins'), 302)
    except EntityDoesNotExistException as e:
        return make_response(
            render_template('login.html', error='E_ENTITY_DOES_NOT_EXIST'), 404)
    except IncorrectPasswordException as e:
        return make_response(
            render_template('login.html', error='E_INCORRECT_PASSWORD'), 400)


def validate_form(form):
    """Executes simple form validation. Checks for None or empty string values.

    Args:
        form (MultiDict): The form data that was POST'd.

    Returns:
        bool: If username or password contain None or empty strings, False is
        returned. Otherwise, True is returned.
    """
    return (form['username'].replace(' ', '') and form['username'] is not None and
        form['password'].replace(' ', '') and form['password'] is not None)


@app.route('/pins', methods=['GET'])
@login_required
def pins():
    """Renders the /pins page template.

    Returns:
        TYPE: Description
    """
    username = current_user.username
    return render_template(
        'pins.html',
        username=username,
        pins=Pin.query_all().fetch(10))


@app.route('/api/pins', methods=['POST', 'GET'])
def api_pins():
    """Fetches or creates Pins.

    See handle_api_pins_post() and handle_api_pins_get() for more details.

    Returns:
        Response:
    """
    if request.method == 'POST':
        return handle_api_pins_post(request)
    elif request.method == 'GET':
        return handle_api_pins_get(request)


def handle_api_pins_post(request):
    """Handles POST requests to /api/pins.

    If the JSON POST request body contains the 'challenge' or 'token' keys,
    perform Slack's URL verification handshake. For more details, see:
    https://api.slack.com/events-api#url_verification.
    Otherwise, create a Pin (and its attachments).

    Args:
        request (Request):

    Returns:
        Response:
    """
    json = request.get_json()
    if ('token' not in json or
        json['token'] != app.config['slack_verification_token']):
        return make_response(
            jsonify(message='Missing or unrecognized token.'),
            401)

    if 'challenge' in json:
        # Handle the very first and only auth call.
        challenge = json['challenge']
        return jsonify(challenge=challenge)

    PinnedMessage.factory(json)
    return make_response('', 201)


def handle_api_pins_get(request):
    """Handles GET requests to /api/pins.

    If 'user_id' query param is set, pins for that user are returned.
    Otherwise, the most recently pinned messages are returned.

    Args:
        request (Request):

    Returns:
        Response:
    """
    user_id = request.args.get('user_id')
    if user_id:
        pins = Pin.query_user(user_id).fetch(10)
    else:
        pins = Pin.query_all().fetch(10)

    response = {
        'data': {
            'pins': [pin.to_dict() for pin in pins]
        }
    }
    return jsonify(response)
