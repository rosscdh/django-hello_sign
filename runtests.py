# -*- coding: utf-8 -*-
import os, sys
from django.conf import settings
from django.core.management import call_command

DIRNAME = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DIRNAME, 'database.db'),
    }
}

settings.configure(DEBUG = True,
                   DATABASES=DATABASES,
                   USE_TZ=True,
                   HELLOSIGN_AUTHENTICATION = ("founders@lawpal.com", "test2007"),
                   HELLOSIGN_API_KEY='12345678910111213141516171819201234567891011121314151617181920',
                   HELLOSIGN_CLIENT_ID='9sc892aa172754698e3fa30dedee3836',
                   HELLOSIGN_CLIENT_SECRET='8d330244b9971abfe789f5224551139e',
                   ROOT_URLCONF='hello_sign.tests.urls',
                   INSTALLED_APPS = ('django.contrib.auth',
                                     'django.contrib.contenttypes',
                                     'django.contrib.sessions',
                                     'django.contrib.admin',
                                     'hello_sign',
                                     'hello_sign.tests',))


from django.test.simple import DjangoTestSuiteRunner

call_command('syncdb', interactive=False)

failures = DjangoTestSuiteRunner().run_tests(['hello_sign',], verbosity=1)
if failures:
    sys.exit(failures)