# -*- coding: utf-8 -*-
"""General utility functions."""

from config import AppConfig

from pins4days.constants import GCS_CONFIG_KEY_REMOTE
from pins4days.constants import GCS_CONFIG_KEY_LOCAL


def load_config():
    """Loads in the Pins4Days config.

    Returns:
        dict: The Pins4Days config contents.
    """
    config = AppConfig(GCS_CONFIG_KEY_REMOTE, GCS_CONFIG_KEY_LOCAL)
    config.load_config()
    return config.contents
