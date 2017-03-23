# -*- coding: utf-8 -*-
"""
.. module:: maintenance_mode.io.__init__.py
   :synopsis: Define IO class to store the maintenance mode in a file located
   in a S3 bucket. This class use the boto library to connect to S3.

.. moduleauthor:: Edgar Zamora Gomez <edgarzamoragomez@gmail.com>
"""
from maintenance_mode.io import AbstractIO
from maintenance_mode import settings

from boto.s3 import connect_to_region, key


class IO(AbstractIO):
    """ IO class to connect to S3 backend """
    def __init__(self):

        self.aws_s3_region = settings.AWS_S3_REGION
        self.access_key = settings.AWS_ACCESS_KEY
        self.secret_key = settings.AWS_SECRET_KEY
        self.bucket = settings.AWS_S3_BUCKET

        self.s3_connection = None

    def set_connection(self):
        if not self.s3_connection:
            self.s3_connection = connect_to_region(
                self.aws_s3_region,
                aws_access_key_id=self.access_key,
                aws_secret_access_key=self.secret_key
            )

    def read_file(self, file_path, default_content=''):
        """ TODO: Add docs """

        self.set_connection()

        try:
            s3_bucket = self.s3_connection.get_bucket(self.bucket)
            s3_key = key.Key(s3_bucket, file_path)
            return s3_key.get_contents_as_string()

        except Exception:
            return default_content
