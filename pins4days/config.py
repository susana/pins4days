# -*- coding: utf-8 -*-

import os
import yaml

from google.appengine.api import app_identity
import lib.cloudstorage as gcs

from constants import KEY_FLASK_APP_CONFIG
from constants import KEY_FLASK_SECRET_KEY


class AppConfig(object):
    """Handles reading in configs from Google Cloud Storage (GCS), and
    writing local configs to the local development server.

    See the tutorial: https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/app-engine-cloud-storage-sample

    To view files in the local development server navigate to:
        http://localhost:8000/blobstore

        Note that the local development server file location is dictated by
        LOCAL_APP_CONFIG_PATH defined in app.yaml. This can be updated to suit
        your directory structure.


    Attributes:
        contents (dict): The contents of the config file.
        file_path (str): The name of the REMOTE config file.
        remote_path (str): The path to the app config file in a REMOTE
        GCS bucket. This should not include the bucket name.
        local_path (str): The subpath to the app config YAML file in a LOCAL
        directory relative to the root of this app.
    """

    def __init__(self, remote_path, local_path):
        """
        Args:
            remote_path (str): The path to the app config file in a REMOTE
            GCS bucket. This should not include the bucket name.
            local_path (TYPE): The subpath to the app config YAML file in a LOCAL
            directory relative to the root of this app.
        """
        self.remote_path = remote_path
        self.local_path = local_path
        self.contents = None
        self.file_path = None

    def load_config(self):
        """Writes the local config file to GCS if this is executed on the local
        development server, and then loads the remote config file from GCS.
        """
        self._build_config_file_path()
        self._write_local_config()
        self._load_config()
        if not self._has_required_values():
            raise InvalidConfigException(
                'App config is missing required key/values.')

    def _load_config(self):
        """Loads the contents of the config file from GCS."""
        gcs_file = gcs.open(self.file_path)
        contents = gcs_file.read()
        gcs_file.close()
        self.contents = yaml.load(contents)

    def _has_required_values(self):
        app_config_keys = set([
            'slack_client_id',
            'slack_client_secret',
            'slack_verification_token'
        ])
        top_level_keys = set([KEY_FLASK_APP_CONFIG, KEY_FLASK_SECRET_KEY])
        return (top_level_keys.issubset(set(self.contents.keys())) and
            app_config_keys.issubset(set(self.contents[KEY_FLASK_APP_CONFIG].keys())))


    def _build_config_file_path(self):
        """Builds the bucket location where the config file is located in GCS."""
        bucket_name = os.environ.get(
            'BUCKET_NAME',
            app_identity.get_default_gcs_bucket_name())
        self.file_path = "/{}/{}".format(bucket_name, self.remote_path)

    def _write_local_config(self):
        """Writes a local config file to GCS."""
        if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            with open(self.local_path, 'r') as stream:
                content = stream.read()
                gcs_file = gcs.open(self.file_path, 'w', content_type='text/plain')
                gcs_file.write(content)
                gcs_file.close()


class InvalidConfigException(Exception):
    pass
