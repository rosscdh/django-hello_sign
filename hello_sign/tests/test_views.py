# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from model_mommy import mommy

from toolkit.casper.workflow_case import BaseScenarios
from toolkit.apps.workspace.tests.data import HELLOSIGN_200_RESPONSE
from toolkit.apps.engageletter.models import EngagementLetter

from ..models import HelloSignRequest, HelloSignLog
from ..views import HelloSignWebhookEventHandler
from .data import HELLOSIGN_WEBHOOK_EVENT_DATA

import json


class HelloSignWebhookEventHandlerTest(BaseScenarios, TestCase):
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
        self.basic_workspace()

        signature_request_id = HELLOSIGN_WEBHOOK_EVENT_DATA['signature_request'].get('signature_request_id')

        self.engageletter = mommy.make('engageletter.EngagementLetter',
                                        slug='d1c545082d1241849be039e338e47aa0',
                                        status=EngagementLetter.STATUS.customer_sign_and_send)

        content_object = self.engageletter.get_content_type_object()

        self.subject.tool = mommy.make('sign.HelloSignRequest',
                                       content_object_type=content_object,
                                       object_id=self.engageletter.pk,
                                       signature_request_id=signature_request_id,
                                       data=HELLOSIGN_200_RESPONSE)
        

    def test_response_contains_required_text(self):
        # emulate a HelloSign Post
        resp = self.client.post(reverse('sign:hellosign_webhook_event'), json.dumps(HELLOSIGN_WEBHOOK_EVENT_DATA), content_type="application/json")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, 'Hello API Event Received')

    def test_response_creates_correct_objects(self):
        # emulate a HelloSign Post
        resp = self.client.post(reverse('sign:hellosign_webhook_event'), json.dumps(HELLOSIGN_WEBHOOK_EVENT_DATA), content_type="application/json")

        hsrequest_object = HelloSignRequest.objects.get(content_object_type=self.engageletter.get_content_type_object(),
                                     object_id=self.engageletter.pk)
        hs_logs = hsrequest_object.hellosignlog_set.all()
        log = hs_logs[0]

        self.assertEqual(hs_logs.count(), 1)
        self.assertEqual(log.event_type, 'signature_request_sent')
        self.assertEqual(log.data, HELLOSIGN_WEBHOOK_EVENT_DATA)

