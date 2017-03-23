# -*- coding: utf-8 -*-

import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


def runtests():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))

def runtests_s3():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_s3'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['tests'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) > 2:
        print 'runtests.py [local | s3] [cache]\n' \
              'by default it will run the tests for the local backend ' \
              'storage without cache'
        sys.exit(2)
    if 1 <= len(args) <= 2:
        if args[0] == 's3':
            runtests_s3()
        if args[0] == 'local':
            runtests()
        else:
            print 'runtests.py [local | s3]\n' \
                  'by default it will run the tests for the local backend ' \
                  'storage'
            sys.exit(2)
    runtests()

