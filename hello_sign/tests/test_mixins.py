# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType

import inspect
import unittest

from ..mixins import ModelContentTypeMixin, HelloSignModelMixin
from ..mixins import OverrideModelMethodException

from .models import TestMonkeyModel, TestGorillaModel


class ModelContentTypeMixinTest(unittest.TestCase):
    subject = ModelContentTypeMixin
    test_object = TestMonkeyModel

    def test_subject_has_content_type_object_method(self):
        self.assertTrue('get_content_type_object' in dir(self.subject))
        self.assertTrue('get_content_type_object' in dir(self.test_object))

    def test_subject_content_type_object_type(self):
        obj = self.test_object.objects.create(slug='test-monkey')
        self.assertEqual(type(obj.get_content_type_object()), ContentType)


class ModelContentExceptionsRaisedTest(unittest.TestCase):
    subject = None
    test_object = TestGorillaModel

    def setUp(self):
        super(ModelContentExceptionsRaisedTest, self).setUp()
        self.subject = self.test_object.objects.create(slug='test-me-gorrilla')

    def test_model_raises_exception_when_hs_document_title(self):
        with self.assertRaises(OverrideModelMethodException):
            self.subject.hs_document_title()

    def test_model_raises_exception_when_hs_document(self):
        with self.assertRaises(OverrideModelMethodException):
            self.subject.hs_document()


class ModelContentExceptionsNotRaisedTest(unittest.TestCase):
    subject = None
    test_object = TestMonkeyModel

    def setUp(self):
        super(ModelContentExceptionsNotRaisedTest, self).setUp()
        self.subject = self.test_object.objects.create(slug='test-me-monkey')

    def test_model_raises_no_exception_when_hs_document_title(self):
        self.assertEqual(self.subject.hs_document_title(), 'I am a Monkey')

    def test_model_raises_no_exception_when_hs_document(self):
        filename = self.subject.hs_document()
        self.assertEqual(filename.name[-4:], '.pdf')


class HelloSignModelMixinTest(unittest.TestCase):
    subject = HelloSignModelMixin

