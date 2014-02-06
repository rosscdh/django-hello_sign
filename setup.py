# -*- coding: utf-8 -*-
import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-hellosign",
    version = "0.1.5",
    author = "Ross Crawford-d'Heureuse",
    author_email = "ross@lawpal.com",
    description = ("Django app for integrating with HelloSign"),
    license = "MIT",
    keywords = "django hellosign app",
    url = "https://github.com/rosscdh/django-hellosign",
    packages=['hello_sign'],
    long_description=read('README.md'),
    install_requires = [
        'hellosign',
    ],
    dependency_links=[
        'git+ssh://git@github.com/rosscdh/HelloSignApi.git@0.1.0#egg=HelloSignApi-v0.1.0-beta'
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)