# -*- coding: utf-8 -*-
from django import template
from django.conf import settings

from datetime import datetime

register = template.Library()

import logging
logger = logging.getLogger('django.request')

# STATUS_CODE_CHOICES = {
#     'signature_request_viewed': 'The SignatureRequest has been viewed.   SignatureRequest',
#     'signature_request_signed': 'A signer has completed all required fields on the SignatureRequest. SignatureRequest',
#     'signature_request_sent': 'The SignatureRequest has been sent successfully.    SignatureRequest',
#     'signature_request_all_signed': 'All signers have completed all required fields for the SignatureRequest and the final PDF is ready to be downloaded using signature_request/final_copy. SignatureRequest',
#     'signature_request_invalid': 'The signature request was marked as invalid',  # Undocumented at the time of this creation,
#     'file_error': 'We\'re unable to convert the file you provided.',
# }

STATUS_CODE_CHOICES = {
    'awaiting_signature': 'Waiting for this User to sign',
    'signed': 'Has signed',
    'on_hold': 'Signature request has been put on hold'
}

@register.filter(name='timestamp_to_date')
def timestamp_to_date(timestamp=None):
    if timestamp is not None and type(timestamp) in [int, float]:
        return datetime.fromtimestamp(timestamp)
    return None


@register.filter(name='status_code_name')
def status_code_name(status_code):
    return STATUS_CODE_CHOICES.get(status_code, 'Unknown Status Code: %s' % status_code)


@register.inclusion_tag('sign/hello_sign/signer_url.html')
def signer_url_js(obj, email):
    """
    get the signing url for a particular user email
    """
    return {
        'HELLOSIGN_CLIENT_ID': settings.HELLOSIGN_CLIENT_ID,
        'DEBUG': 'true' if settings.DEBUG is True else 'false',
        'signer_url': obj.signing_url(signer_email=email),
    }
signer_url_js.is_safe = True
