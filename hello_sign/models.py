# -*- coding: utf-8 -*-
from django.db import models
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


class HelloSignLog(models.Model):
    """
    Model to store the HelloSign Webhook Events
    """
    request = models.ForeignKey('sign.HelloSignRequest')
    event_type = models.CharField(max_length=32, db_index=True)
    dateof = models.DateTimeField(auto_now=False, auto_now_add=True, db_index=True)
    data = JSONField(default={})

    class Meta:
        # newest first
        ordering = ['-id']


from .signals import hellosign_webhook_event_recieved