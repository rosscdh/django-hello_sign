# -*- coding: utf-8 -*-
"""
HelloSign webhook Event
"""
from django.dispatch import Signal, receiver

hellosign_webhook_event_recieved = Signal(providing_args=['signature_request_id',
                                                          'event_type',
                                                          'data',
                                                          'hellosign_request',
                                                          'hellosign_log'])


@receiver(hellosign_webhook_event_recieved)
def on_signature_request_viewed_invalidate_signer_url(sender, hellosign_log, signature_request_id, hellosign_request, event_type, data, **kwargs):
    """
    Invalidate the signer url when we recieve  signature_request_viewed event
    """
    if event_type == 'signature_request_viewed':
        #
        # should be able to delete the HelloSignSigningUrl object for this
        # event; but there is nothing to bund the HS event object
        # with our HelloSignSigningUrl.signature_id and
        # HelloSignSigningUrl.request object
        #
        pass
