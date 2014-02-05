from django.db import models

from ..mixins import ModelContentTypeMixin


class TestMonkeyModel(ModelContentTypeMixin, models.Model):
    slug = models.SlugField()