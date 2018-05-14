# -*- coding: utf-8 -*-
"""Pins4Days app constants.

Attributes:
    GCS_CONFIG_KEY_LOCAL (str): The path to the local Pins4Days app config.
    GCS_CONFIG_KEY_REMOTE (str): The path to the remote Pins4Days app config
    in GCS.
    KEY_FLASK_APP_CONFIG (str): The key for the Flask app configs that must
    be present in the GCS_CONFIG_* files.
    KEY_FLASK_SECRET_KEY (str): The key for the Flask app secret key that must
    be present in the GCS_CONFIG_* files.
    SLACK_AUTH_URL (str): Slack's auth URL.
    SLACK_OAUTH_URL (str): Slack's auth URL.
"""

GCS_CONFIG_KEY_LOCAL = 'dev/config.yaml'
GCS_CONFIG_KEY_REMOTE = 'configs/pins4days.yaml'

SLACK_OAUTH_URL = 'https://slack.com/api/oauth.access'
SLACK_AUTH_URL = 'https://slack.com/oauth/authorize'

KEY_FLASK_APP_CONFIG = 'flask_app_config'
KEY_FLASK_SECRET_KEY = 'flask_secret_key'
