from django.db import models

from jsonfield import JSONField
from tempfile import NamedTemporaryFile

from ..mixins import ModelContentTypeMixin, HelloSignModelMixin


class TestMonkeyModel(ModelContentTypeMixin, models.Model):
    """
    model used to test that the exceptions for hs_document_title and hs_document
    are NOT raised when they are overriden
    """
    slug = models.SlugField()

    def hs_document_title(self):
        return 'I am a Monkey'

    def hs_document(self):
        return NamedTemporaryFile(suffix='.pdf')


class TestGorillaModel(HelloSignModelMixin, models.Model):
    """
    model used to test if the exceptions for hs_document_title and hs_document
    are raised when they are not overriden
    """
    slug = models.SlugField()
    data = JSONField(default={})

