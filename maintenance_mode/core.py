# -*- coding: utf-8 -*-

from maintenance_mode import settings
import importlib

if settings.MAINTENANCE_MODE_CACHE:
    from django.core.cache import cache


def get_io():
    module_name = "maintenance_mode.io.{backend}".format(
        backend=settings.MAINTENANCE_MODE_STORAGE
    )
    module = importlib.import_module(module_name)
    return getattr(module, "IO")()


def get_maintenance_mode():
    value = None

    if settings.MAINTENANCE_MODE_CACHE:
        # If cache enabled, try to get the value from cache.
        value = cache.get(settings.MAINTENANCE_MODE_CACHE_KEY)

    if not value:
        value = get_io().read_file(
            settings.MAINTENANCE_MODE_STATE_FILE_PATH, '0')
        if settings.MAINTENANCE_MODE_CACHE:
            # If cache enabled, and we are here means that the value is not in
            # cache yet. So we will set the value received from the file to
            # cache.
            cache.set(
                settings.MAINTENANCE_MODE_CACHE_KEY,
                value,
                settings.MAINTENANCE_MODE_CACHE_TIMEOUT
            )

    if value not in ['0', '1']:
        raise ValueError('state file content value is not 0|1')

    value = bool(int(value))
    return value


def set_maintenance_mode(value):

    if not isinstance(value, bool):
        raise TypeError('value argument type is not boolean')

    value = str(int(value))

    get_io().write_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, value)

    if settings.MAINTENANCE_MODE_CACHE:
        # Disable the cache.
        cache.delete(settings.MAINTENANCE_MODE_CACHE_KEY)
