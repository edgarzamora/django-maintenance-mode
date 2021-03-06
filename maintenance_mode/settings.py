# -*- coding: utf-8 -*-

from django.conf import settings

import os


MAINTENANCE_MODE = getattr(settings, 'MAINTENANCE_MODE', False)

MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = getattr(
    settings, 'MAINTENANCE_MODE_IGNORE_IP_ADDRESSES', None)

MAINTENANCE_MODE_IGNORE_STAFF = getattr(
    settings, 'MAINTENANCE_MODE_IGNORE_STAFF', False)

MAINTENANCE_MODE_IGNORE_SUPERUSER = getattr(
    settings, 'MAINTENANCE_MODE_IGNORE_SUPERUSER', False)

MAINTENANCE_MODE_IGNORE_TEST = getattr(
    settings, 'MAINTENANCE_MODE_IGNORE_TEST', False)

MAINTENANCE_MODE_IGNORE_URLS = getattr(
    settings, 'MAINTENANCE_MODE_IGNORE_URLS', None)

MAINTENANCE_MODE_REDIRECT_URL = getattr(
    settings, 'MAINTENANCE_MODE_REDIRECT_URL', None)

MAINTENANCE_MODE_STORAGE = getattr(
    settings, 'MAINTENANCE_MODE_STORAGE', 'local')

MAINTENANCE_MODE_STATE_FILE_PATH = getattr(
    settings,
    'MAINTENANCE_MODE_STATE_FILE_PATH',
    os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'maintenance_mode_state.txt'
    ) if MAINTENANCE_MODE_STORAGE is 'local' else 'maintenance_mode_state.txt'
)

MAINTENANCE_MODE_TEMPLATE = getattr(
    settings, 'MAINTENANCE_MODE_TEMPLATE', '503.html')

MAINTENANCE_MODE_TEMPLATE_CONTEXT = getattr(
    settings, 'MAINTENANCE_MODE_TEMPLATE_CONTEXT', None)

# S3

AWS_ACCESS_KEY = getattr(settings, 'AWS_ACCESS_KEY', None)
AWS_S3_REGION = getattr(settings, 'AWS_S3_REGION', None)
AWS_SECRET_KEY = getattr(settings, 'AWS_SECRET_KEY', None)
AWS_S3_BUCKET = getattr(settings, 'AWS_S3_BUCKET', None)

# Cache
MAINTENANCE_MODE_CACHE = getattr(settings, 'MAINTENANCE_MODE_CACHE', False)

MAINTENANCE_MODE_CACHE_TIMEOUT = getattr(
    settings, 'MAINTENANCE_MODE_CACHE_TIMEOUT', None)

MAINTENANCE_MODE_CACHE_KEY = getattr(
    settings, 'MAINTENANCE_MODE_CACHE_KEY', 'maintenance_mode_state')
