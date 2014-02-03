# -*- coding: utf-8 -*-
"""
HelloSign webhook Event
"""
from django.dispatch import Signal

hellosign_webhook_event_recieved = Signal(providing_args=['signature_request_id',
                                                          'event_type',
                                                          'data',
                                                          'hellosign_request',
                                                          'hellosign_log'])