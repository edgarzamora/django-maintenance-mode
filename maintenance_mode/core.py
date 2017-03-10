# -*- coding: utf-8 -*-

from maintenance_mode import io, settings


def get_io():
    if settings.MAINTENANCE_MODE_STORAGE is 's3':
        return io.S3IO(
            aws_s3_region=settings.AWS_S3_REGION,
            access_key=settings.AWS_ACCESS_KEY,
            secret_key=settings.AWS_SECRET_KEY,
            bucket=settings.AWS_S3_BUCKET
        )

    else:
        return io.GenericIO()


def get_maintenance_mode():

    value = get_io().read_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, '0')

    if not value in ['0', '1']:
        raise ValueError('state file content value is not 0|1')

    value = bool(int(value))
    return value


def set_maintenance_mode(value):

    if not isinstance(value, bool):
        raise TypeError('value argument type is not boolean')

    value = str(int(value))

    get_io().write_file(settings.MAINTENANCE_MODE_STATE_FILE_PATH, value)
