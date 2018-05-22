# -*- coding: utf-8 -*-

import logging
import json

from flask import Flask
from flask import request
from flask import make_response

from pins4days.event import PinnedMessage


app = Flask(__name__)


@app.route('/worker/create_pin', methods=['POST'])
def create_pin():
    """Creates a pin.

    Returns:
        Response:
    """
    pin_data = json.loads(request.data)
    PinnedMessage.factory(pin_data)
    return make_response('', 201)
