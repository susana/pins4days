# -*- coding: utf-8 -*-
"""General utility functions."""

from config import AppConfig
import os

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
