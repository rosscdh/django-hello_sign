# -*- coding: utf-8 -*-
import os
from setuptools import setup

setup(
    name = "django-hello_sign",
    version = "0.1.6",
    author = "Ross Crawford-d'Heureuse",
    author_email = "ross@lawpal.com",
    description = ("Django app for integrating with HelloSign"),
    license = "MIT",
    keywords = "django hellosign app",
    url = "https://github.com/rosscdh/django-hello_sign",
    packages=['hello_sign'],
    install_requires = [
        'hellosign',  # must refer to package version explicitly **required**
    ]
)
