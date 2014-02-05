django-hellosign
================

Django integration app for hellosign


Installing
----------

```
pip install -r requirements.txt
```

Add to your settings.py

```
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'hello_sign',
)
```

Setup urls.py

```
urlpatterns = patterns('',
    url(r'^sign/', include('hello_sign.urls', namespace='sign')),
)

```


Run the tests
-------------

Run from a virtualenv with django pre-installed

```
python runtests.py
```