# -*- coding: utf-8 -*-
"""
Todo:
    * Rename filename to bucket.
"""

import os
import yaml

from google.appengine.api import app_identity
import lib.cloudstorage as gcs

from constants import GCS_CONFIG_KEY_REMOTE
from constants import GCS_CONFIG_KEY_LOCAL


class AppConfig(object):
    """Handles reading in remote configs from Google Cloud Storage (GCS), and
    writing local files to the local development server.

    See the tutorial: https://cloud.google.com/appengine/docs/standard/python/googlecloudstorageclient/app-engine-cloud-storage-sample

    To view files in the local development server navigate to:
        http://localhost:8000/blobstore

        Note that the local development server file location is dictated by
        constants.GCS_CONFIG_KEY_LOCAL. This can be updated to suit your directory
        structure. You'll probably want to add that file to your .gitignore,
        especially if your config contains secrets.


    Attributes:
        contents (dict): The contents of the config file.
        filename (str): The name of the REMOTE config file.
    """

    def load_config(self):
        """Writes the local config file to GCS if this is executed on the local
        development server, and then loads the remote config file from GCS.
        """
        self._build_config_filename()
        self._write_local_config()
        self._load_config()

    def _load_config(self):
        """Loads the contents of the config file from GCS."""
        gcs_file = gcs.open(self.filename)
        contents = gcs_file.read()
        gcs_file.close()
        self.contents = yaml.load(contents)

    def _build_config_filename(self):
        """Builds the bucket location where the config file is located in GCS."""
        bucket_name = os.environ.get(
            'BUCKET_NAME',
            app_identity.get_default_gcs_bucket_name())
        self.filename = "/{}/{}".format(bucket_name, GCS_CONFIG_KEY_REMOTE)

    def _write_local_config(self):
        """Writes a local config file to GCS."""
        if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            with open(GCS_CONFIG_KEY_LOCAL, 'r') as stream:
                content = stream.read()
                gcs_file = gcs.open(self.filename, 'w', content_type='text/plain')
                gcs_file.write(content)
                gcs_file.close()
