[![PyPI version](https://badge.fury.io/py/django-maintenance-mode.svg)](https://badge.fury.io/py/django-maintenance-mode)
[![Build Status](https://travis-ci.org/fabiocaccamo/django-maintenance-mode.svg?branch=master)](https://travis-ci.org/fabiocaccamo/django-maintenance-mode)
[![coverage](https://codecov.io/gh/fabiocaccamo/django-maintenance-mode/branch/master/graph/badge.svg)](https://codecov.io/gh/fabiocaccamo/django-maintenance-mode)

# django-maintenance-mode
django-maintenance-mode shows a 503 error page when **maintenance-mode** is **on**.

It works at application level, so your django instance should be up.

It doesn't use database and doesn't prevent database access.

##Requirements
- Python 2.7, 3.4, 3.5, 3.6
- Django 1.7, 1.8, 1.9, 1.10

##Installation

1. Run ``pip install django-maintenance-mode`` or [download django-maintenance-mode](http://pypi.python.org/pypi/django-maintenance-mode) and add the **maintenance_mode** package to your project
2. Add ``'maintenance_mode'`` to ``settings.INSTALLED_APPS`` before custom applications
3. Add ``'maintenance_mode.middleware.MaintenanceModeMiddleware'`` to ``settings.MIDDLEWARE_CLASSES`` as last middleware
4. Add your custom ``templates/503.html`` file
5. Restart your application server

##Configuration (optional)

All these settings are optional, if not defined in ``settings.py`` the default values (listed below) will be used.

```python

# if True the maintenance-mode will be activated
MAINTENANCE_MODE = False

# by default, a file named "maintenance_mode_state.txt" will be created in the same directory of the settings.py file
# you can customize the state file path in case the default one is not writable
MAINTENANCE_MODE_STATE_FILE_PATH = 'maintenance_mode_state.txt'

# if True the staff will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_STAFF = False

# if True the superuser will not see the maintenance-mode page
MAINTENANCE_MODE_IGNORE_SUPERUSER = False

# By default the value is 'local', which save the mode status in the local machine.
# If the server is running in more than one server it allows to save the file in AWS S3
# using the Third part library boto. See AWS S3 section below for more information. 
MAINTENANCE_MODE_STORAGE = 'local'

#list of ip-addresses that will not be affected by the maintenance-mode
#ip-addresses will be used to compile regular expressions objects
MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = ()

# list of urls that will not be affected by the maintenance-mode
# urls will be used to compile regular expressions objects
MAINTENANCE_MODE_IGNORE_URLS = ()

# if True the maintenance mode will not return 503 response while running tests
# useful for running tests while maintenance mode is on, before opening the site to public use
MAINTENANCE_MODE_IGNORE_TEST = False

# the absolute url where users will be redirected to during maintenance-mode
MAINTENANCE_MODE_REDIRECT_URL = None

# the template that will be shown by the maintenance-mode page
MAINTENANCE_MODE_TEMPLATE = '503.html'

# the path of the function that will return the template context -> 'myapp.mymodule.myfunction'
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

##Usage

####Python
```python
from maintenance_mode.core import get_maintenance_mode, set_maintenance_mode

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

####Templates
```html
{% if maintenance_mode %}
<!-- html -->
{% endif %}
```

####Terminal

Run ``python manage.py maintenance_mode <on|off>``

*(****This is not Heroku-friendly because*** *any execution of heroku run `manage.py` will be run on a separate worker dyno, not the web one. Therefore* ***the state-file is set but on the wrong machine****)*

####URLs
Superusers can change maintenance-mode using the following urls:

``/maintenance-mode/off/``

``/maintenance-mode/on/``

##License
Released under [MIT License](LICENSE).
