# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.timezone import utc
from hellosign import HelloSigner, HelloDoc
from hellosign import (HelloSignSignature,
                       HelloSignEmbeddedDocumentSignature,
                       HelloSignEmbeddedDocumentSigningUrl)

import time
from datetime import timedelta, datetime

from . import logger
from .models import HelloSignSigningUrl


class AuthenticationSettingsException(Exception):
    message = 'settings.HELLOSIGN_AUTHENTICATION tuple ("username", "password") has not been provided.'


class BaseHellSignHelper(object):
    hellosign_authentication = None

    def __init__(self, **kwargs):
        try:
            self.hellosign_authentication = settings.HELLOSIGN_AUTHENTICATION
            assert type(self.hellosign_authentication) == tuple
            assert len(self.hellosign_authentication) == 2
        except AttributeError:
            msg = 'settings.HELLOSIGN_AUTHENTICATION tuple ("username", "password") has not been provided.'
            logger.critical(msg)
            raise AuthenticationSettingsException(msg)


class HelloSignService(BaseHellSignHelper):
    """
    Service that allows us to send a document for signing
    """
    def __init__(self, document, invitees, **kwargs):
        self.document = document
        logger.info(u'Submitting document to HelloSign: "%s"' % document.name)

        # Dependency injected class for testing
        self.HelloSignSignatureClass = kwargs.get('HelloSignSignatureClass', HelloSignEmbeddedDocumentSignature)

        self.invitees = invitees
        self.title = kwargs.get('title', self.document.name)
        self.user = kwargs.get('user', None)
        self.subject = kwargs.get('subject', None)
        self.message = kwargs.get('message', None)

        super(HelloSignService, self).__init__(**kwargs)

    def send_for_signing(self, **kwargs):
        signature = self.HelloSignSignatureClass(title=self.title, subject=self.subject, message=self.message)

        # Add invitees
        for i in self.invitees:
            signature.add_signer(HelloSigner(name=i['name'], email=i['email']))

        signature.add_doc(HelloDoc(file_path=self.document.name))

        # Perform the submission
        result = signature.create(auth=self.hellosign_authentication, **kwargs)

        return result


class HelloSignSignerService(BaseHellSignHelper):
    """
    Service that returns various data for and about the signer
    """
    signer_email = None  # the current users email
    obj = None
    hellosign_request = None
    signatures = None
    signatures = []  # the current set of signatures for a request

    def __init__(self, obj, signer_email=None, **kwargs):
        self.signer_email = signer_email
        self.obj = obj
        self.hellosign_request = obj.hellosign # method on mixin to get latest HS response object
        self.signatures = obj.signatures[::]

        super(HelloSignSignerService, self).__init__(**kwargs)

        self.process()

    def embedded_signature_url(self, signature_id):
        service = HelloSignEmbeddedDocumentSigningUrl(signature_id=signature_id)
        return service.create(auth=self.hellosign_authentication)

    def process(self):
        """
        Get the embedded signature url and expiry from HS
        @TODO refactor @CODESMELL
        """
        for i, signer in enumerate(self.signatures):
            logger.debug(u'HelloSign get a signing_url for signer: %s' % signer)
            #
            # If we have NO email address specified then update all the signer dicts
            # if we have an email and the current signers email matches it then update
            # just that one
            #
            if self.signer_email is None or self.signer_email == signer.get('signer_email_address'):

                status_code = signer.get('status_code', None)
                expires_at = signer.get('expires_at', None)
                logger.debug('Get signing_url for status_code: %s, expires_at: %s' % (status_code, signer))

                #
                # If we are waiting on a signature or have no code
                #
                if status_code in ['awaiting_signature', None]:
                    logger.debug(u'signing_url status_code is valid and we can try get a signature')
                    #
                    # If we have no expries_at date (implies url has already been got)
                    # or if the expires at has expired
                    #
                    if expires_at is None or datetime.fromtimestamp(int(expires_at)) >= datetime.utcnow():
                        logger.debug(u'can get signature url, as current is None or has expired')

                        resp = self.embedded_signature_url(signature_id=signer.get('signature_id'))
                        signing_url_log = self.process_embedded_signature_url(signature=signer, response=resp)
                        #
                        # These are critical 
                        # the sign_url gets used in the search for the users sign_url
                        # in self.sign_url_for_signer
                        #
                        signer['sign_url'] = signing_url_log.sign_url
                        signer['expires_at'] = signing_url_log.expires_at

                    else:
                        logger.info('signing_url status_code is invalid has not expired: %s for : %s' % (expires_at, self.signatures[i]))
                        pass

    def process_embedded_signature_url(self, signature, response):
        """
        Process the HS response to an embeded signature url
        """
        if response.status_code not in [200,201]:
            resp_json = response.json()
            logger.critical('Could not record the signature url due to: %s, is_new: %s' % (response.status_code, resp_json))

        else:
            resp_json = response.json()
            resp_json = resp_json.get('embedded', {})

            signature_id = signature.get('signature_id')

            expires_at = datetime.fromtimestamp(resp_json.get('expires_at')).replace(tzinfo=utc)
            #
            # Create a SignUrl Object for the record
            #
            signing_url_log, is_new = HelloSignSigningUrl.objects.get_or_create(request=self.hellosign_request,
                                                                                signature_id=signature_id)
            signing_url_log.expires_at = expires_at
            signing_url_log.data = resp_json
            signing_url_log.save(update_fields=['expires_at', 'data'])

            logger.debug('Record the sign_url object: %s, is_new: %s' % (signing_url_log, is_new))
            return signing_url_log

    def sign_url_for_signer(self, email):
        """
        Loop over the provided signatures and look for the specific email
        """
        logger.debug(u'Finding sign_url_for_signer: %s' % email)

        for i, signer in enumerate(self.signatures):
            status_code = signer.get('status_code', None)
            logger.debug(u'Status code for sign_url_for_signer: %s' % status_code)

            if status_code in ['awaiting_signature', None]:
                logger.debug(u'Valid status code for sign_url_for_signer: %s' % status_code)

                if signer.get('signer_email_address') == email:

                    sign_url = signer.get('sign_url')
                    logger.debug('sign_url for: %s is %s' % (email, sign_url))

                    return sign_url
        return None

