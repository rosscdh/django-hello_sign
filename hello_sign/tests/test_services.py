# -*- coding: utf-8 -*-
from unittest import TestCase
from django.conf import settings
from django.test.utils import override_settings


from ..services import (BaseHellSignHelper,
                        HelloSignService,
                        HelloSignSignerService,)
from ..services import AuthenticationSettingsException


class BaseHellSignHelperTest(TestCase):
    subject = BaseHellSignHelper

    def test_tuple_exception_raised_when_not_specified_in_settings(self):
        delattr(settings, 'HELLOSIGN_AUTHENTICATION')
        with self.assertRaises(AuthenticationSettingsException):
            self.subject()


# class HelloSignServiceTest(TestCase):
#     subject = HelloSignService


# class HelloSignSignerServiceTest(TestCase):
#     subject = HelloSignSignerService