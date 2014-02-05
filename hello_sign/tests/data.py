# -*- coding: utf-8 -*-
import json

HELLOSIGN_200_RESPONSE = json.dumps({   u'signature_request': {   u'cc_email_addresses': [],
                              u'custom_fields': [],
                              u'details_url': u'https://www.hellosign.com/home/manage?locate=79d41104dcf47068457c813615516f92c4ee6d63',
                              u'has_error': False,
                              u'is_complete': False,
                              u'message': u'This is a test singing please delete',
                              u'original_title': u'Test Signing',
                              u'requester_email_address': u'founders@lawpal.com',
                              u'response_data': [],
                              u'signature_request_id': u'79d41104dcf47068457c813615516f92c4ee6d63',
                              u'signatures': [   {   u'last_reminded_at': None,
                                                     u'last_viewed_at': None,
                                                     u'order': None,
                                                     u'signature_id': u'4555c5f356f8bdebb3bc7204d78af8ae',
                                                     u'signed_at': None,
                                                     u'signer_email_address': u'ross+customer@lawpal.com',
                                                     u'signer_name': u'Ross Customer',
                                                     u'status_code': u'awaiting_signature'},
                                                 {   u'last_reminded_at': None,
                                                     u'last_viewed_at': None,
                                                     u'order': None,
                                                     u'signature_id': u'a9c0ca82240d920c4303e5b56e2ad191',
                                                     u'signed_at': None,
                                                     u'signer_email_address': u'ross+lawyer@lawpal.com',
                                                     u'signer_name': u'Ross Tech Lawyer',
                                                     u'status_code': u'awaiting_signature'}],
                              u'signing_redirect_url': None,
                              u'signing_url': u'https://www.hellosign.com/editor/sign?guid=79d41104dcf47068457c813615516f92c4ee6d63',
                              u'subject': u'Test Signing',
                              u'test_mode': True,
                              u'title': u'/var/folders/nb/w1bxhlbd7jscn56p6gksdbcm0000gn/T/tmp7Xf1UC.docx'}})


HELLOSIGN_WEBHOOK_EVENT_DATA = {
    "event": {
        "event_time": "1348177752", 
        "event_type": "signature_request_sent"
    }, 
    "signature_request": {
        "cc_email_addresses": [], 
        "custom_fields": [], 
        "details_url": "https://www.hellosign.com/home/manage?locate=1f8c510a38edbdf97eed524fba1c9a900feb56a4", 
        "has_error": False, 
        "is_complete": False, 
        "message": "Please sign this NDA and then we can discuss more. Let me know if you have any questions.", 
        "requester_email_address": "me@hellosign.com", 
        "response_data": [], 
        "signature_request_id": "1f8c510a38edbdf97eed524fba1c9a900feb56a4", 
        "signatures": [
            {
                "signature_id": "78caf2a1d01cd39cea2bc1cbb340dac3",
                "last_reminded_at": None, 
                "last_viewed_at": None, 
                "order": None, 
                "signed_at": None, 
                "signer_email_address": "jack@example.com", 
                "signer_name": "Jack", 
                "status_code": "awaiting_signature"
            }
        ], 
        "signing_url": "https://www.hellosign.com/editor/sign?guid=1f8c510a38edbdf97eed524fba1c9a900feb56a4", 
        "signing_redirect_url": None,
        "subject": "NDA with Acme Co.", 
        "title": "NDA with Acme Co."
    }
}

