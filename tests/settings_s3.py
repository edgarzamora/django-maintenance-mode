# -*- coding: utf-8 -*-

from .settings import *

# S3 settings
# Add here your AWS S3 credentials in order to run the unittests for this
# backend
AWS_ACCESS_KEY = ''
AWS_S3_REGION = ''
AWS_SECRET_KEY = ''
AWS_S3_BUCKET = ''

MAINTENANCE_MODE_STORAGE = 's3'

# Optionally you can define the filepath on amazon s3 (sub-bucket)
# MAINTENANCE_MODE_STATE_FILE_PATH = ''
