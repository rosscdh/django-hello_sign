# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.views.decorators.csrf import csrf_exempt

from .views import HelloSignWebhookEventHandler


urlpatterns = patterns('',
    url(r'^hellosign/event/$', csrf_exempt(HelloSignWebhookEventHandler.as_view()), name='hellosign_webhook_event'),
)
