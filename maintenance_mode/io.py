# -*- coding: utf-8 -*-

from boto.s3 import connect_to_region, key, bucket


class GenericIO(object):

    def read_file(self, file_path, default_content=''):
        """ TODO: Add docs """
        try:
            handler = open(file_path, 'r')
            content = handler.read()
            handler.close()
            return content or default_content

        except IOError:
            return default_content

    def write_file(self, file_path, content):
        """ TODO: Add docs """
        try:
            handler = open(file_path, 'w+')
            handler.write(content)
            handler.close()
            return True

        except IOError:
            return False


class S3IO(GenericIO):
    def __init__(self, aws_s3_region, access_key, secret_key, bucket):

        self.aws_s3_region = aws_s3_region
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket = bucket

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
        try:
            s3_bucket = self.s3_connection.get_bucket(self.bucket)
            s3_key = key.Key(s3_bucket, file_path)
            return s3_key.get_contents_as_string()

        except Exception:
            return default_content

    def write_file(self, file_path, content):
        """ TODO: Add docs """

        self.s3_connection()

        try:
            s3_bucket = self.s3_connection.get_bucket(self.bucket)
            s3_key = key.Key(s3_bucket, file_path)
            s3_key.set_contents_from_string(content, headers={
                'Content-Type': 'text/plain',
            })
            return True

        except Exception:
            return False
