# -*- coding: utf-8 -*-

import unittest

from google.appengine.ext import testbed

from pins4days.config import AppConfig
from pins4days.config import InvalidConfigException
from pins4days.constants import GCS_CONFIG_KEY_REMOTE


class AppConfigTestCase(unittest.TestCase):

    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_app_identity_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_blobstore_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def test_load_config(self):
        app_config = AppConfig(GCS_CONFIG_KEY_REMOTE, 'test/data/app_config.yaml')
        app_config.load_config()
        expected = {
            'flask_app_config': {
                'slack_client_id': '1838492.4948',
                'slack_client_secret': 'd077f244def8a70e5ea758bd8352f',
                'slack_verification_token': '6da89cd09ab7937478a1d47d'
            },
            'flask_secret_key': '5ebe2294ecd0e0f08eab76'
        }
        self.assertEquals(expected, app_config.contents)
        self.assertEquals('/app_default_bucket/configs/pins4days.yaml', app_config.file_path)

    def test_invalid_config(self):
        app_config = AppConfig(GCS_CONFIG_KEY_REMOTE, 'test/data/app_config_invalid.yaml')
        with self.assertRaises(InvalidConfigException) as context:
            app_config.load_config()
