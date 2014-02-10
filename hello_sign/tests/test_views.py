# -*- coding: utf-8 -*-
from django.core.cache import cache
from django.dispatch import receiver
from django.test import TestCase, Client
from django.core.urlresolvers import reverse


from ..models import HelloSignRequest, HelloSignLog
from ..views import HelloSignWebhookEventHandler
from ..signals import hellosign_webhook_event_recieved

from .data import HELLOSIGN_200_RESPONSE, HELLOSIGN_WEBHOOK_EVENT_DATA
from .models import TestMonkeyModel

import json

"""
Test signal listner to handle the signal fired event
"""
@receiver(hellosign_webhook_event_recieved)
def on_hellosign_webhook_event_recieved(**kwargs):
    cache.set('hellosign_webhook_event_recieved_keys', kwargs.keys())


class HelloSignWebhookEventHandlerTest(TestCase):
    """
    Test the handleing of HelloSign webhook events

    as per: http://www.hellosign.com/api/gettingStarted "Handling callbacks"

    NOTE: Your endpoint will need to return a 200 HTTP code and a response body
    containing the following text: "Hello API Event Received". Otherwise,
    the callback will be considered a failure and will be retried later.
    """
    subject = HelloSignWebhookEventHandler
    client = Client

    def setUp(self):
        super(HelloSignWebhookEventHandlerTest, self).setUp()
        self.monkey = TestMonkeyModel.objects.create(slug='test-monkey')
        self.monkey_content_object = self.monkey.get_content_type_object()

        self.signature_request_id = HELLOSIGN_WEBHOOK_EVENT_DATA['SIGNATURE_REQUEST_SENT']['signature_request'].get('signature_request_id')

        self.request = HelloSignRequest.objects.create(content_object_type=self.monkey_content_object,
                                                       object_id=self.monkey.pk,
                                                       signature_request_id=self.signature_request_id,
                                                       data=HELLOSIGN_200_RESPONSE)

    def get_webhook_event_post_data(self):
        """
        NB: HelloSign wraps the json data in another json object called "json"
        i.e. HelloSign sends a post object with key "json" that is set to an actual
        string of JSON
        """
        return { 'json': json.dumps(HELLOSIGN_WEBHOOK_EVENT_DATA['SIGNATURE_REQUEST_SENT']) }

    def get_hellosign_post_response(self):
        return self.client.post(reverse('sign:hellosign_webhook_event'), self.get_webhook_event_post_data())

    def test_response_contains_required_text(self):
        # emulate a HelloSign Post
        resp = self.get_hellosign_post_response()

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Hello API Event Received')

    def test_hellosign_webhook_event_recieved_fired(self):
        # emulate a HelloSign Post
        resp = self.get_hellosign_post_response()
        self.assertEqual(cache.get('hellosign_webhook_event_recieved_keys'), ["hellosign_log", "signal", "signature_request_id", "hellosign_request", "event_type", "data", "sender"])

    def test_response_creates_correct_objects(self):
        # emulate a HelloSign Post
        resp = self.get_hellosign_post_response()

        hsrequest_object = HelloSignRequest.objects.get(content_object_type=self.monkey_content_object,
                                     object_id=self.monkey.pk)
        hs_logs = hsrequest_object.hellosignlog_set.all()
        log = hs_logs[0]

        self.assertEqual(hs_logs.count(), 1)
        self.assertEqual(log.event_type, 'signature_request_sent')
        self.assertEqual(log.data, HELLOSIGN_WEBHOOK_EVENT_DATA['SIGNATURE_REQUEST_SENT'])

