from django.db import models

from jsonfield import JSONField

from ..mixins import ModelContentTypeMixin, HelloSignModelMixin


class TestMonkeyModel(ModelContentTypeMixin, models.Model):
    slug = models.SlugField()


class TestGorillaModel(HelloSignModelMixin, models.Model):
    slug = models.SlugField()
    data = JSONField(default={})