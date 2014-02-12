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


Setup your signal handler

```
from hello_sign.signals import hellosign_webhook_event_recieved


@receiver(hellosign_webhook_event_recieved)
def on_hellosign_webhook_event_recieved(sender, hellosign_log, signature_request_id, hellosign_request, event_type, data, **kwargs):
    """
    Handle the signal
    """
    logging.info('Recieved event: %s for request: %s' % (event_type, hellosign_request,))
    engageletter = hellosign_request.source_object
    user, status = hellosign_log.signer_status

    if hellosign_log.event_type == 'signature_request_viewed':
        # Mark for this event
        handle_signature_request_viewed()

    elif hellosign_log.event_type == 'signature_request_signed':
        # Mark for this event
        handle_signature_request_signed()

    elif hellosign_log.event_type == 'signature_request_sent':
        # Mark for this event
        handle_signature_request_sent()

    elif hellosign_log.event_type == 'signature_request_all_signed':
        # Mark for this event
        handle_signature_request_all_signed()

    elif hellosign_log.event_type == 'signature_request_invalid':
        # Mark for this event
        handle_signature_request_invalid()

    elif hellosign_log.event_type == 'file_error':
        # Mark for this event
        handle_file_error()

    else:
        # Invalid Event log as error and or raise exception
        handle_invalid()


```

Template Tags
-------------

In order to make use of the HelloSign Javascript object (OAuth)

in your template

```
{% load hello_sign_tags %}

{% signer_url_js my_object_with_mixin user.email %}
```

Which will then the signature url for that user. 

HelloSign expires the url as soon as its looked at. However does not send an event
So it makes it difficult to invalidate the signer_url



Helpers
-------------

Management Command to register the webhook callback endpoint at HelloSign

The standard url for the callback view is __/sign/hellosign/event/__
Assuming you have set the urls up as above.

```
python manage.py hellosign_set_callback :your_site_url/sign/hellosign/event/
```


Run the tests
-------------

Run from a virtualenv with django pre-installed

```
python runtests.py
```
