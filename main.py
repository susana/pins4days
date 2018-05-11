# -*- coding: utf-8 -*-

import logging

import requests
from flask import Flask
from flask import request
from flask import jsonify
from flask import redirect
from flask import make_response
from lib.werkzeug.urls import Href

from pins4days.utils import load_config
from pins4days.event import PinEvent
from pins4days.constants import SLACK_OAUTH_URL
from pins4days.constants import SLACK_AUTH_URL


app = Flask(__name__)
app.config.update(load_config())


@app.before_request
def authorize_request():
    json = request.get_json()

    if ('token' not in json or
        json['token'] != app.config['slack_verification_token']):
        return make_response(
            jsonify(message="Missing or unrecognized token."),
            401)

@app.route('/api/pins', methods=['POST'])
def api_pins():
    json = request.get_json()

    # Handle the very first and only auth call.
    if 'challenge' in json:
        challenge = json['challenge']
        return jsonify(challenge=challenge)

    pin_event = PinEvent.factory(json)
    return make_response("", 200)
