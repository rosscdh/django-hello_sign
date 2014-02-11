# -*- coding: utf-8 -*-
from unittest import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.test import TestCase as DjangoTestCase

import re
import time
import json
import httpretty

from .models import TestGorillaModel
from .data import HELLOSIGN_WEBHOOK_EVENT_DATA, SIGNATURE_URL_REQUEST

from ..models import HelloSignRequest
from ..templatetags.hello_sign_tags import (STATUS_CODE_CHOICES,
                                           status_code_name,
                                           timestamp_to_date,
                                           signer_url_js,)

import datetime


def _SIGNATURE_URL_RESPONSE(signature_id, expires_at, token):
    signature_url_response = SIGNATURE_URL_REQUEST.copy()

    signature_url_response['embedded']['expires_at'] = expires_at
    signature_url_response['embedded']['sign_url'] = signature_url_response['embedded']['sign_url'].format(signature_id=signature_id,
                                                                                                           token=token)

    return json.dumps(signature_url_response)


class StatusCodeTest(TestCase):
    """
    Test the STATUS_CODE_CHOICES are set and of right types
    """
    subject = STATUS_CODE_CHOICES

    def test_status_codes(self):
        self.assertEqual(type(self.subject), dict)

        self.assertEqual(self.subject, {
            'awaiting_signature': 'Waiting for this User to sign',
            'signed': 'Has signed',
            'on_hold': 'Signature request has been put on hold'
        })


class StatusCodeNameTest(TestCase):
    """
    Test the status_code_name filter tag
    """
    valid = STATUS_CODE_CHOICES
    invalid = ['monkey', 'shark', 'government']

    def test_valid_names(self):
        for t in self.valid:
            resp = status_code_name(t)
            self.assertEqual(resp, STATUS_CODE_CHOICES[t])

    def test_invalid_names(self):
        for t in self.invalid:
            resp = status_code_name(t)
            self.assertEqual(resp, 'Unknown Status Code: %s' % t)


class TimestampToDateTest(TestCase):
    """
    Test the timestamp_to_date template filter
    """
    invalid = [None, '', 'fdafdas']

    def test_none_value(self):
        result = timestamp_to_date(None)
        self.assertEqual(result, None)

    def test_good_value(self):
        result = timestamp_to_date(1392037300)
        self.assertEqual(type(result), datetime.datetime)

    def test_invalid_value(self):
        for t in self.invalid:
            result = timestamp_to_date(t)
            self.assertEqual(result, None)


class SignerUrlJavascriptTest(DjangoTestCase):
    """
    Test the inclusion tag that shows the HelloSign Javascript
    for a specific user, which is then used to show the popup
    """
    subject = TestGorillaModel

    def setUp(self):
        self.lawyer = User.objects.create(email='test+lawyer@lawpal.com', first_name='Lawyer', last_name='Test', username='test-lawyer')
        self.user = User.objects.create(email='test+customer@lawpal.com', first_name='Customer', last_name='Test', username='test-customer')

        self.SIGNATURE_REQUEST_SENT = HELLOSIGN_WEBHOOK_EVENT_DATA.get('SIGNATURE_REQUEST_SENT').get('signature_request')
        self.signature_request_id = self.SIGNATURE_REQUEST_SENT.get('signature_request_id')

        self.signature_id = self.SIGNATURE_REQUEST_SENT.get('signatures')[1].get('signature_id')  # customer signature_id
        self.token = 'ab066813dea6612cf284992d764d05ff'

        self.obj = self.subject.objects.create(slug='silverback', data=self.SIGNATURE_REQUEST_SENT)
        self.hellosign_request = HelloSignRequest.objects.create(content_object_type=self.obj.get_content_type_object(),
                                                                 object_id=self.obj.pk,
                                                                 signature_request_id=self.signature_request_id,
                                                                 data=self.SIGNATURE_REQUEST_SENT)

    @override_settings(DEBUG=False, HELLOSIGN_CLIENT_ID=None)
    def test_signer_url_required_hs_client_id(self):
        delattr(settings, 'HELLOSIGN_CLIENT_ID')
        with self.assertRaises(AttributeError) as e:
            resp = signer_url_js(self.obj, self.user.email)

    @override_settings(DEBUG=False, HELLOSIGN_CLIENT_ID='12345678910-HS', HELLOSIGN_AUTHENTICATION=None)
    def test_signer_url_required_hs_authentication(self):
        delattr(settings, 'HELLOSIGN_AUTHENTICATION')
        with self.assertRaises(Exception) as e:
            resp = signer_url_js(self.obj, self.user.email)

    @httpretty.activate
    @override_settings(DEBUG=False, HELLOSIGN_CLIENT_ID='12345678910-HS', HELLOSIGN_AUTHENTICATION=('test', 'password'))
    def test_signer_url_js_valid(self):
        httpretty.register_uri(httpretty.GET, re.compile(r"^https://api.hellosign.com/v3/(.*)$"),
                               body=_SIGNATURE_URL_RESPONSE(signature_id=self.signature_id, expires_at=int(time.time()), token=self.token),
                               status=200)

        self.obj = self.subject.objects.get(pk=self.obj.pk)
        resp = signer_url_js(self.obj, self.user.email)
        self.assertEqual(resp, {'DEBUG': 'false', 'signer_url': u'https://www.hellosign.com/editor/embeddedSign?signature_id={signature_id}&token=ab066813dea6612cf284992d764d05ff'.format(signature_id=self.signature_id), 'HELLOSIGN_CLIENT_ID': '12345678910-HS'})

    @override_settings(DEBUG=True, HELLOSIGN_CLIENT_ID='12345678910-HS', HELLOSIGN_AUTHENTICATION=('test', 'password'))
    def test_signer_url_js_expired(self):
        """
        if no sig_url has been provided then return None
        """
        resp = signer_url_js(self.obj, self.user.email)
        self.assertEqual(resp, {'DEBUG': 'true', 'signer_url': None, 'HELLOSIGN_CLIENT_ID': '12345678910-HS'})
