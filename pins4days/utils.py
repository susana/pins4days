# -*- coding: utf-8 -*-
"""General utility functions.
"""

from config import AppConfig
import os
import json

from google.appengine.api import urlfetch
from werkzeug.urls import Href

from pins4days.constants import LOCAL_APP_CONFIG_PATH_KEY
from pins4days.constants import REMOTE_APP_CONFIG_PATH_KEY


def load_config():
    """Loads in the Pins4Days config.

    Returns:
        dict: The Pins4Days config contents.
    """
    config = AppConfig(
        os.environ[REMOTE_APP_CONFIG_PATH_KEY],
        os.environ[LOCAL_APP_CONFIG_PATH_KEY])
    config.load_config()
    return config.contents


def get_channel_pins(channel_id, token):
    """Fetches all pinned messages from a particular channel.

    Args:
        channel_id (str): Slack channel ID.
        token (str): Slack user token.

    Returns:
        str: Response as a JSON string.

    Raises:
        Exception: Description
    """
    href = Href('https://slack.com/api/pins.list')
    url = href({'channel': channel_id, 'token': token})
    result = urlfetch.fetch(url)
    if result.status_code == 200:
        return json.loads(result.content)

    raise Exception('resultz {} {}'.format(result.status_code, result.content))
