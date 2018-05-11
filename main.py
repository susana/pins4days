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
from pins4days.models import Pin
from pins4days.constants import SLACK_OAUTH_URL
from pins4days.constants import SLACK_AUTH_URL


app = Flask(__name__)
app.config.update(load_config())


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

    pin_event = PinEvent.factory(json)
    return make_response("", 201)


def handle_api_pins_get(request):
    user_id = request.args.get('user_id')
    if user_id:
        pins = Pin.query_user(user_id).fetch(10)
    else:
        pins = Pin.query_all()

    response = {
        'data': {
            'pins': [pin.to_dict() for pin in pins]
        }
    }
    return jsonify(response)
