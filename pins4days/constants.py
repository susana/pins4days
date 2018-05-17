# -*- coding: utf-8 -*-
"""Pins4Days app constants.

Attributes:
    KEY_FLASK_APP_CONFIG (str): The key for the Flask app configs that must
    be present in the GCS_CONFIG_* files.
    KEY_FLASK_SECRET_KEY (str): The key for the Flask app secret key that must
    be present in the GCS_CONFIG_* files.
    SLACK_AUTH_URL (str): Slack's auth URL.
    SLACK_OAUTH_URL (str): Slack's auth URL.
"""

SLACK_OAUTH_URL = 'https://slack.com/api/oauth.access'
SLACK_AUTH_URL = 'https://slack.com/oauth/authorize'

KEY_FLASK_APP_CONFIG = 'flask_app_config'
KEY_FLASK_SECRET_KEY = 'flask_secret_key'

LOCAL_APP_CONFIG_PATH_KEY = 'LOCAL_APP_CONFIG_PATH'
REMOTE_APP_CONFIG_PATH_KEY = 'REMOTE_APP_CONFIG_PATH'
