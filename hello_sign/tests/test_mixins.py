# -*- coding: utf-8 -*-
from django.db import models

import inspect
import unittest

from ..mixins import HelloSignModelMixin


class HelloSignModelMixinTest(unittest.TestCase):
    subject = HelloSignModelMixin
