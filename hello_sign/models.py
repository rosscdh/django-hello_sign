# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField


class HelloSignRequest(models.Model):
    """
    Model to store the HelloSign Signing Request info
    """
    content_object_type = models.ForeignKey('contenttypes.ContentType', db_index=True)
    object_id = models.IntegerField(db_index=True)
    signature_request_id = models.CharField(max_length=128, db_index=True)
    dateof = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    data = JSONField(default={})

    class Meta:
        # newest first
        ordering = ['-dateof']

    def __unicode__(self):
        return u'HelloSign Request for %s' % self.source_object

    @property
    def source_object(self):
        return self.content_object_type.get_object_for_this_type(pk=self.object_id)


class HelloSignLog(models.Model):
    """
    Model to store the HelloSign Webhook Events
    """
    request = models.ForeignKey('hello_sign.HelloSignRequest')
    event_type = models.CharField(max_length=32, db_index=True)
    dateof = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    data = JSONField(default={})

    class Meta:
        # newest first
        ordering = ['-id']

    @property
    def response_data(self):
        return self.data['signature_request'].get('response_data', [])

    @property
    def signatures(self):
        return self.data['signature_request'].get('signatures', [])

    @property
    def signer_status(self):
        """
        Return the User object and status for this log
        """
        first = None
        response_data = self.response_data
        #
        # reversed is used because HS send the complete response_data
        # and simply keeps appending to it thus the most recent elements are 
        # the last elements on the list
        #
        for item in reversed(response_data):
            #
            # get the item with the type "signature"
            # because all kinds of crazy are passed in from HS
            #
            if item.get('type') == "signature":
                first = item
                break

        if first is not None:
            signature_id = first.get('signature_id')

            for signer in self.signatures:
                signer_email_address = signer.get('signer_email_address')

                if signer.get('signature_id') == signature_id:
                    status_code = signer.get('status_code')
                    user = User.objects.get(email=signer_email_address)
                    return (user, status_code)

        return (None, None)





from .signals import hellosign_webhook_event_recieved