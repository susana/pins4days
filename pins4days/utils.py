# -*- coding: utf-8 -*-

from config import GCSConfig


def load_config():
    config = GCSConfig()
    config.build_config_filename()
    config.write_local_config()
    return config.load_config()
