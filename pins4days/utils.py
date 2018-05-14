# -*- coding: utf-8 -*-
"""General utility functions."""

from config import AppConfig


def load_config():
    """Loads in the Pins4Days config.

    Returns:
        dict: The Pins4Days config contents.
    """
    config = AppConfig()
    config.load_config()
    return config.contents
