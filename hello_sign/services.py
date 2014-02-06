# -*- coding: utf-8 -*-
from django.conf import settings

from hellosign import HelloSignEmbeddedDocumentSignature
from hellosign import HelloSigner, HelloDoc

from . import logger


class HelloSignService(object):
    """
        Service that allows us to send a document for signing
    """
    def __init__(self, document, invitees, **kwargs):
        self.document = document
        logger.info('Submitting document to HelloSign: "%s"' % document.name)

        # Dependency injected class for testing
        self.HelloSignSignatureClass = kwargs.get('HelloSignSignatureClass', HelloSignEmbeddedDocumentSignature)

        self.invitees = invitees
        self.title = kwargs.get('title', self.document.name)
        self.user = kwargs.get('user', None)
        self.subject = kwargs.get('subject', None)
        self.message = kwargs.get('message', None)

        try:
            self.hellosign_authentication = settings.HELLOSIGN_AUTHENTICATION
        except AttributeError:
            logger.critical("No settings.HELLOSIGN_AUTH has been specified. Please provide them")

    def send_for_signing(self, **kwargs):
        signature = self.HelloSignSignatureClass(title=self.title, subject=self.subject, message=self.message)

        # Add invitees
        for i in self.invitees:
            signature.add_signer(HelloSigner(name=i['name'], email=i['email']))

        signature.add_doc(HelloDoc(file_path=self.document.name))

        # Perform the submission
        try:
            result = signature.create(auth=self.hellosign_authentication, **kwargs)
        except Exception as e:
            result = None
            logger.error('Could not submit %s to HelloSign: "%s"'%(self.document, e,))

        return result