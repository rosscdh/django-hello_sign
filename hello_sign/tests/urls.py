# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sign/', include('hello_sign.urls', namespace='sign')),
)
