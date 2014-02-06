# -*- coding: utf-8 -*-
from django.views.generic import CreateView
from django.shortcuts import render, get_object_or_404

from . import logger

from .models import HelloSignRequest, HelloSignLog
from .models import hellosign_webhook_event_recieved

import json


class HelloSignWebhookEventHandler(CreateView):
    """
    View to handle the HelloSign webhook events

    as per: http://www.hellosign.com/api/gettingStarted "Handling callbacks"

    NOTE: Your endpoint will need to return a 200 HTTP code and a response body
    containing the following text: Hello API Event Received. Otherwise,
    the callback will be considered a failure and will be retried later.
    """
    model = HelloSignLog
    # response needs to return "Hello API Event Received"
    template_name = 'sign/hellosign/webhook_create_event.html'

    def extract_json_data(self, body):
        logger.debug('Post from HelloSign: %s' % body)

        try:
            data = json.loads(body)

            if 'event' not in data:
                raise Exception('No event key found in HelloSign Post body')

            if 'signature_request' not in data:
                raise Exception('No signature_request key found in HelloSign Post body')

        except Exception as e:
            logger.critical('Could not extract json from request.body in HelloSignWebhookEventHandler: %s' % e)
            raise e

        return data

    def post(self, request, *args, **kwargs):
        data = self.extract_json_data(body=request.body)  # extract json
        event_type = data['event'].get('event_type')
        signature_request_id = data['signature_request'].get('signature_request_id')

        logger.info('recieved webhook event: %s from HelloSign signature_request_id: %s' % (event_type, signature_request_id))

        # get the request object which must exist as its created when the object is sent for signing
        hellosign_request = get_object_or_404(HelloSignRequest, signature_request_id=signature_request_id)

        # create log object
        self.object = self.model.objects.create(request=hellosign_request,
                                                event_type=event_type,
                                                data=data)

        logger.info('Issuing hellosign_webhook_event_recieved signal')
        hellosign_webhook_event_recieved.send(sender=self,
                                              signature_request_id=signature_request_id,
                                              event_type=event_type,
                                              data=data,
                                              hellosign_request=hellosign_request,
                                              hellosign_log=self.object)


        return render(request, self.template_name)
