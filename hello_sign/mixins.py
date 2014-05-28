# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from jsonfield import JSONField

from hellosign import HelloSignUnclaimedDraftDocumentSignature
from .services import HelloSignService, HelloSignSignerService
from .models import HelloSignRequest

from . import logger

import json
import datetime

HELLOSIGN_TEST_MODE = getattr(settings, 'HELLOSIGN_TEST_MODE', 1)


class OverrideModelMethodException(Exception):
    message = 'You must override this method'


class ModelContentTypeMixin(object):
    """
    Mixin to provide get_content_type_object of the model its mixed in with
    """
    def get_content_type_object(self):
        """
        Required Method for acessing the current models ContentType
        """
        return ContentType.objects.get(app_label=self._meta.app_label,
                                       model=self._meta.model_name)


class HelloSignModelMixin(ModelContentTypeMixin):
    data = JSONField(default={})  # required to store data

    def hellosign_requests(self):
        """
        QuerySet of HelloSignRequest objects
        relies on HelloSignRequest._meta to define order
        """
        return HelloSignRequest.objects.filter(object_id=self.pk,
                                               content_object_type=self.get_content_type_object())

    @property
    def hellosign(self):
        """
        The Latest HelloSign Request
        """
        return self.hellosign_requests().first()

    @property
    def signing_data(self):
        return getattr(self.hellosign, 'data', None)

    @property
    def signature_request_id(self):
        return getattr(self.hellosign, 'signature_request_id', None)

    def sign_url_for_email(self, signer_email):
        """
        Get the sign_url for a specific email address
        """
        service = HelloSignSignerService(obj=self, signer_email=signer_email)
        return service.sign_url_for_signer(email=signer_email)

    @property
    def signatures(self):
        return self.signing_data.get('signatures', [])

    @signatures.setter
    def signatures(self, value):
        """
        Setter to allow us to update the signatures details segment of the
        current json object
        """
        obj = self.hellosign  # most recent HSRequest object
        obj.data['signatures'] = value
        obj.save(update_fields=['data'])

        # and the local model
        self.data['signatures'] = value
        self.save(update_fields=['data'])

    def hs_subject(self):
        """
        Simple subject sent as part of the HelloSign request used by HS
        in communication and in their own web interface
        """
        return 'Signature Request for %s' % self

    def hs_message(self):
        """
        Descriptive message sent as part of the HelloSign request used by HS
        in communication and in their own web interface
        """
        return 'Please review and sign this document at your earliest convenience'

    def hs_signers(self):
        """
        Return a list of invitees to sign
        Order here is important as it ties in tightly with the HS signers
        unfortunately
        """
        raise OverrideModelMethodException('You must override hs_signers and return a dict {"name": name, "email": email}')

    def hs_document_title(self):
        """
        Method to set the document title, displayed in the HelloSign Interface
        """
        raise OverrideModelMethodException('You must override hs_document_title and return the title of the document to send to HelloSign')

    def hs_document(self):
        """
        Return the document to be senf for signing
        """
        raise OverrideModelMethodException('You must override hs_document and return the pdf/docx/doc file to send to HelloSign')

    def get_hs_service(self, **kwargs):
        """
        Return the HelloSign service instance with all required to send for
        signing
        """
        kwargs.update({
            'document': self.hs_document(),
            'title': self.hs_document_title(),
            'invitees': self.hs_signers(),
            'subject': self.hs_subject(),
            'message': self.hs_message(),
        })
        return HelloSignService(**kwargs)

    def create_unclaimed_draft(self, requester_email_address, **kwargs):
        """
        Create an unsigned draft that can be used to setup a document for signing
        """
        service = self.get_hs_service(HelloSignSignatureClass=HelloSignUnclaimedDraftDocumentSignature)  # override the HelloSignSignatureClass

        resp = service.create_unclaimed_draft(test_mode=HELLOSIGN_TEST_MODE,
                                              client_id=settings.HELLOSIGN_CLIENT_ID,
                                              requester_email_address=requester_email_address,
                                              **kwargs)

        return self.hs_process_result(resp=resp)

    def send_for_signing(self, **kwargs):
        """
        Primary method used to send a document for signing
        """
        service = self.get_hs_service()

        resp = service.send_for_signing(test_mode=HELLOSIGN_TEST_MODE,
                                        client_id=settings.HELLOSIGN_CLIENT_ID,
                                        **kwargs)

        return self.hs_process_result(resp=resp)

    def hs_process_result(self, resp):
        if type(resp) not in [dict]:
            if hasattr(resp, 'json') is False:
                raise Exception('resp needs to be a dict or a requests response object with .json() method')
            else:
                resp = resp.json()  # assume is a requests response object

        logger.debug('HelloSign response: %s' % resp)

        # post process the result
        resp = self.hs_post_process_result(resp=resp)

        self.hs_record_result(result=resp)

        return resp

    def hs_post_process_result(self, resp):
        date_sent = str(datetime.datetime.utcnow())
        #
        # Add the date because HelloSign does not provide a date
        #
        resp.update({
            'date_sent': date_sent
        })

        return resp

    def hs_record_result(self, result):
        # setup the hs request object
        signature_request = result.get('signature_request', {})
        signature_request_id = signature_request.get('signature_request_id') # get id

        if signature_request_id:
            hs_request_object, is_new = HelloSignRequest.objects.get_or_create(signature_request_id=signature_request_id,
                                                                               content_object_type=self.get_content_type_object(),
                                                                               object_id=self.pk)
            #
            # Update the request object data dict with the signature_request object
            #
            data = hs_request_object.data
            data.update(result)
            # save it back
            hs_request_object.data = data
            hs_request_object.save(update_fields=['data'])

            return hs_request_object
        return None
