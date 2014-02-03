# -*- coding: utf-8 -*-
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