[![PyPI version](https://badge.fury.io/py/django-maintenance-mode.svg)](https://badge.fury.io/py/django-maintenance-mode)
[![Build Status](https://travis-ci.org/fabiocaccamo/django-maintenance-mode.svg?branch=master)](https://travis-ci.org/fabiocaccamo/django-maintenance-mode)
[![coverage](https://codecov.io/gh/fabiocaccamo/django-maintenance-mode/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/django-maintenance-mode)

# django-maintenance-mode
django-maintenance-mode shows a 503 error page when **maintenance-mode** is **on**.

It works at application level, so your django instance should be up.

It doesn't use database and doesn't prevent database access.

## Requirements
- Python 2.7, 3.4, 3.5, 3.6
- Django 1.7, 1.8, 1.9, 1.10

## Installation

1. Run ``pip install django-maintenance-mode`` or [download django-maintenance-mode](http://pypi.python.org/pypi/django-maintenance-mode) and add the **maintenance_mode** package to your project
2. Add ``'maintenance_mode'`` to ``settings.INSTALLED_APPS`` before custom applications
3. Add ``'maintenance_mode.middleware.MaintenanceModeMiddleware'`` to ``settings.MIDDLEWARE_CLASSES`` as last middleware
4. Add your custom ``templates/503.html`` file
5. Restart your application server

## Configuration (optional)

All these settings are optional, if not defined in ``settings.py`` the default values (listed below) will be used.

```python

# if True the maintenance-mode will be activated
MAINTENANCE_MODE = False

# by default, a file named "maintenance_mode_state.txt" will be created 
# in the same directory of the settings.py file you can customize the 
# state file path in case the default one is not writable
MAINTENANCE_MODE_STATE_FILE_PATH = 'maintenance_mode_state.txt'

# if True the staff will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_STAFF = False

# if True the superuser will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_SUPERUSER = False

# By default the value is 'local', which save the mode status in 
# the local machine. If the server is running in more than one server 
# it allows to save the file in AWS S3 using the Third part library 
# boto. See AWS S3 section below for more information. 
MAINTENANCE_MODE_STORAGE = 'local'

# if True the maintenance mode status will be cached in the default 
# cache configuration on the Django project.
MAINTENANCE_MODE_CACHE = False

# by default, the key used for cache is "maintenance_mode_state". You
# can customize the key name. If cache not enabled this value will be
# ignored.
MAINTENANCE_MODE_CACHE_KEY = 'maintenance_mode_state'

# It’s the number of seconds the value should be stored in the cache
# By default is None (the value will be cached forever).
# If MAINTENANCE_MODE_CACHE is false this value is ignored.
MAINTENANCE_MODE_CACHE_TIMEOUT = None

#list of ip-addresses that will not be affected by the maintenance-mode
#ip-addresses will be used to compile regular expressions objects
MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = ()

# list of urls that will not be affected by the maintenance-mode
# urls will be used to compile regular expressions objects
MAINTENANCE_MODE_IGNORE_URLS = ()

# if True the maintenance mode will not return 503 response while 
# running tests useful for running tests while maintenance mode is on, 
# before opening the site to public use
MAINTENANCE_MODE_IGNORE_TEST = False

# the absolute url where users will be redirected to during
# maintenance-mode
MAINTENANCE_MODE_REDIRECT_URL = None

# the template that will be shown by the maintenance-mode page
MAINTENANCE_MODE_TEMPLATE = '503.html'

# the path of the function that will return the template 
# context -> 'myapp.mymodule.myfunction'
MAINTENANCE_MODE_TEMPLATE_CONTEXT = None
```

#### Using **AWS S3** as storage backend

Change the mode storage in the configuration to 's3'
```python
# Define the storage mode as 's3'
MAINTENANCE_MODE_STORAGE = 's3'
```

The maintenance mode is using [boto](http://boto.cloudhackers.com/en/latest/) library to connect to S3. See the configurations fields required used to connect to S3.
```python
AWS_ACCESS_KEY = ''
AWS_S3_REGION = ''
AWS_SECRET_KEY = ''
AWS_S3_BUCKET = ''
```
#### Using **CACHE**

In case that you are running a multi-server environment and you chose the AWS S3 storage backend, we recommend to use the cache functionality. The cache can be used also using the local storage mode, but if you already have this value in your local machine maybe it is not necessary, but it is up to you.
The maintenance mode middleware needs to check the maintenance mode status for each query received to know if the mode is enabled or not. 
Once you chose to store this value in S3, it means that you will need to make one request to S3 for each query. 
In order to reduce the number of requests to S3, we offer the possibility to save this value in a cache system. 

Using the configuration values reported above, you can enable/disable the cache, and also you can define the cached timeout. 

If the cache is enabled:

- It only will call S3 each time that the mode status change. When a WRITE acction is done to S3, the cache value will be disabled.
- When one query comes in, it will try to read the value from cache. If the value is not in the cache or it is disabled, it will go to S3 to take the status value. Once it takes the value, it will add this value on the cache. So, the next queries will read this value from cache.  e to store this value in S3, it means that you will need to make one request to S3 for each query.

This library will use the default Cache server configured in the Django project. For more information related on Cache for Django visit this link: [https://docs.djangoproject.com/en/1.10/topics/cache/](https://docs.djangoproject.com/en/1.10/topics/cache/)

#### Extra configuration
Add **maintenance_mode.urls** to ``urls.py`` if you want superusers able to set maintenance_mode using urls.

```python
urlpatterns = [
    ...
    url(r'^maintenance-mode/', include('maintenance_mode.urls')),
    ...
]
```
Add **maintenance_mode.context_processors.maintenance_mode** to your context_processors list in ``settings.py`` if you want to access the maintenance_mode status in your templates.

```python
TEMPLATES = [
    {
        #...
        'OPTIONS': {
            'context_processors': [
                #...
                'maintenance_mode.context_processors.maintenance_mode',
                #...
            ],
        },
        #...
    },
]
```

## Usage

#### Python
```python
from maintenance_mode.core import (
    get_maintenance_mode, set_maintenance_mode
)

set_maintenance_mode(True)

if get_maintenance_mode():
    set_maintenance_mode(False)
```
or
```python
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        call_command('maintenance_mode', 'on')

        #call your command(s)

        call_command('maintenance_mode', 'off')



```

#### Templates
```html
{% if maintenance_mode %}
<!-- html -->
{% endif %}
```

#### Terminal

Run ``python manage.py maintenance_mode <on|off>``

*(****This is not Heroku-friendly because*** *any execution of heroku run `manage.py` will be run on a separate worker dyno, not the web one. Therefore* ***the state-file is set but on the wrong machine****)*

#### URLs
Superusers can change maintenance-mode using the following urls:

``/maintenance-mode/off/``

``/maintenance-mode/on/``

## License
Released under [MIT License](LICENSE).
