# -*- coding: utf-8 -*-
from django.conf import settings
from hellosign import HelloSigner, HelloDoc
from hellosign import (HelloSignSignature,
                       HelloSignEmbeddedDocumentSignature,
                       HelloSignEmbeddedDocumentSigningUrl)

import time
from datetime import timedelta, datetime

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
        result = signature.create(auth=self.hellosign_authentication, **kwargs)

        return result


class HelloSignSignerService(object):
    """
    Service that returns various data for and about the signer
    """
    signer_email = None  # the current users email
    signatures = []  # the current set of signatures for a request

    def __init__(self, signatures, signer_email=None):
        self.signer_email = signer_email
        self.signatures = signatures

        try:
            self.hellosign_authentication = settings.HELLOSIGN_AUTHENTICATION

        except AttributeError:
            msg = 'No settings.HELLOSIGN_AUTHENTICATION tuple (username:password) has been specified. Please provide them'
            logger.critical(msg)
            raise Exception(msg)

        self.process()

    def embedded_signature_url(self, signature_id):
        service = HelloSignEmbeddedDocumentSigningUrl(signature_id=signature_id)
        return service.create(auth=self.hellosign_authentication)

    def process(self):
        """
        Get the embedded signature url and expiry from HS
        """
        for i, signer in enumerate(self.signatures):
            #
            # If we have NO email address specified then update all the signer dicts
            # if we have an email and the current signers email matches it then update
            # just that one
            #
            logger.debug('HelloSign get a signing_url for signer: %s' % signer)
            if self.signer_email is None or self.signer_email == signer.get('signer_email_address'):

                status_code = signer.get('status_code', None)
                expires_at = signer.get('expires_at', None)
                logger.debug('Get signing_url for status_code: %s, expires_at: %s' % (status_code, signer))

                #
                # If we are waiting on a signature or have no code
                #
                if status_code in ['awaiting_signature', None]:
                    logger.debug('signing_url status_code is valid and we can try get a signature')
                    #
                    # If we have no expries_at date (implies url has already been got)
                    # or if the expires at has expired
                    #
                    if expires_at is None or datetime.fromtimestamp(int(expires_at)) >= datetime.utcnow():
                        logger.debug('can get signature url, as current is None or has expired')

                        resp = self.embedded_signature_url(signature_id=signer.get('signature_id'))

                        try:
                            resp_json = resp.json()['embedded']

                            signer['sign_url'] = resp_json.get('sign_url')
                            signer['expires_at'] = resp_json.get('expires_at')

                            self.signatures[i] = signer

                        except Exception as e:
                            logger.critical('Could not retrieve signer signature url: %s' % e)

                    else:
                        logger.info('signing_url status_code is invalid has not expired: %s for : %s' % (expires_at, self.signatures[i]))


    def sign_url_for_signer(self, email):
        for i, signer in enumerate(self.signatures):

            status_code = signer.get('status_code', None)

            if status_code in ['awaiting_signature', None]:

                if signer.get('signer_email_address') == email:
                    return signer.get('sign_url')
        return None

