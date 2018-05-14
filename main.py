# -*- coding: utf-8 -*-

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
from pins4days.event import PinEvent
from pins4days.models import Pin
from pins4days.models import User
from pins4days.models import EntityDoesNotExist
from pins4days.models import IncorrectPassword
from pins4days.user import AppUser


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
    user = User.get_by_id(username)
    return AppUser(user) if user else None


@app.route('/signup', methods=['POST', 'GET'])
def signup():
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
    if current_user.is_authenticated:
        return redirect(url_for('pins'))

    if request.method == 'GET':
        return render_template('login.html')

    return handle_login_post(request)


def handle_login_post(request):
    if not validate_form(request.form):
        return make_response(
            render_template('login.html', error='E_BAD_FORM'), 400)

    try:
        user = User.login(request.form['username'], request.form['password'])
        app_user = AppUser(user)
        if app_user:
            login_user(app_user)
            return redirect(url_for('pins'), 302)
    except EntityDoesNotExist as e:
        return make_response(
            render_template('login.html', error='E_ENTITY_DOES_NOT_EXIST'), 404)
    except IncorrectPassword as e:
        return make_response(
            render_template('login.html', error='E_INCORRECT_PASSWORD'), 400)


def validate_form(form):
    return (form['username'].replace(' ', '') and form['username'] is not None and
        form['password'].replace(' ', '') and form['password'] is not None)


@app.route('/pins', methods=['GET'])
@login_required
def pins():
    username = current_user.username
    return render_template(
        'pins.html',
        username=username,
        pins=Pin.query_all())


@app.route('/api/pins', methods=['POST', 'GET'])
def api_pins():
    if request.method == 'POST':
        return handle_api_pins_post(request)
    elif request.method == 'GET':
        return handle_api_pins_get(request)


def handle_api_pins_post(request):
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

    PinEvent.factory(json)
    return make_response('', 201)


def handle_api_pins_get(request):
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
