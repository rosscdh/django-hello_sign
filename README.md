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

Use the HelloSignModelMixin on your document model and call

```
my_object = MyObject.objects.get(slug='test-document-for-signing')
resp = my_object.send_for_signing()
```

Remember that you must override the method "hs_document" & "hs_title" on
the object that uses the HelloSignModelMixin

__myobject.models.py__

```
class MyObject(HelloSignModelMixin, models.Model):
    def hs_title():
        return function_or_string_for_title()

    def hs_document():
        return function_that_returns_a_file_object_for_sending_to_hellosign()
```

The function that returns the File object
"function_that_returns_a_file_object_for_sending_to_hellosign" in this case.
can be a class method or indeed a seperate service that compiles html or some
other markup format into a pdf/doc/docx file


Helpers
-------------

Management Command to register the webhook callback endpoint at HelloSign

```
python manage.py hellosign_set_callback :url_to_your_site_for_testing_or_prod
```


Run the tests
-------------

Run from a virtualenv with django pre-installed

```
python runtests.py
```
