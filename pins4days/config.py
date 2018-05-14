# -*- coding: utf-8 -*-

import os
import yaml

from google.appengine.api import app_identity
import lib.cloudstorage as gcs

from constants import GCS_CONFIG_KEY_REMOTE
from constants import GCS_CONFIG_KEY_LOCAL


class AppConfig(object):

    def load_config(self):
        self._build_config_filename()
        self._write_local_config()
        gcs_file = gcs.open(self.filename)
        contents = gcs_file.read()
        gcs_file.close()
        self.contents = yaml.load(contents)

    def _build_config_filename(self):
        bucket_name = os.environ.get(
            'BUCKET_NAME',
            app_identity.get_default_gcs_bucket_name())
        self.filename = "/{}/{}".format(bucket_name, GCS_CONFIG_KEY_REMOTE)

    def _write_local_config(self):
        if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
            with open(GCS_CONFIG_KEY_LOCAL, 'r') as stream:
                content = stream.read()
                gcs_file = gcs.open(self.filename, 'w', content_type='text/plain')
                gcs_file.write(content)
                gcs_file.close()
