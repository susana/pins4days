# -*- coding: utf-8 -*-

from config import AppConfig


def load_config():
    config = AppConfig()
    config.load_config()
    return config.contents
