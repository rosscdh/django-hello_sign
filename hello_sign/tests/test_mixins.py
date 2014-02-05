# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType

import inspect
import unittest

from ..mixins import ModelContentTypeMixin, HelloSignModelMixin

from .models import TestMonkeyModel


class ModelContentTypeMixinTest(unittest.TestCase):
    subject = ModelContentTypeMixin
    test_object = TestMonkeyModel

    def test_subject_has_content_type_object_method(self):
        self.assertTrue('get_content_type_object' in dir(self.subject))
        self.assertTrue('get_content_type_object' in dir(self.test_object))

    def test_subject_content_type_object_type(self):
        obj = self.test_object.objects.create(slug='test-monkey')
        self.assertEqual(type(obj.get_content_type_object()), ContentType)


class HelloSignModelMixinTest(unittest.TestCase):
    subject = HelloSignModelMixin
