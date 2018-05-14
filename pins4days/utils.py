# -*- coding: utf-8 -*-

from config import GCSConfig

from lib.flask import request, url_for
from werkzeug.contrib.cache import MemcachedCache


def load_config():
    config = GCSConfig()
    config.build_config_filename()
    config.write_local_config()
    return config.load_config()


def set_session_configs(app, config):
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SESSION_MEMCACHED'] = MemcachedCache()
    app.secret_key = config['flask_secret_key']
