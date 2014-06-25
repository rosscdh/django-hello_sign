# -*- coding: utf-8 -*-
from django.conf import settings
from django.views.generic import CreateView
from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404

import hashlib, hmac

from . import logger

from .models import HelloSignRequest, HelloSignLog
from .signals import hellosign_webhook_event_recieved

import json
import logging
logger = logging.getLogger('django.request')


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
    template_name = 'sign/hello_sign/webhook_create_event.html'

    def validate_callback(self, event_data):
        # expected result
        event_hash = event_data['event'].get('event_hash')
        # comparison
        event_type = event_data['event'].get('event_type')
        event_time = event_data['event'].get('event_time')

        assert event_hash == unicode(hmac.new(settings.HELLOSIGN_API_KEY, (event_time + event_type), hashlib.sha256).hexdigest()), 'event_hash does not match see: https://www.hellosign.com/api/eventsAndCallbacksWalkthrough#EventHash'
        # if event_hash != unicode(hmac.new(settings.HELLOSIGN_API_KEY, (event_time + event_type), hashlib.sha256).hexdigest()):
        #     raise Exception('event_hash does not match see: https://www.hellosign.com/api/eventsAndCallbacksWalkthrough#EventHash')


    def extract_json_data(self, body):
        logger.debug(u'Post from HelloSign: %s' % body)

        try:
            data = json.loads(body)

            if 'event' not in data:
                raise Exception('No event key found in HelloSign Post body')

            if 'signature_request' not in data:
                logger.info('No signature_request key found in HelloSign Post body')

        except Exception as e:
            logger.critical(u'Could not extract json from request.body in HelloSignWebhookEventHandler: %s' % e)
            raise e

        return data

    def post(self, request, *args, **kwargs):
        """
        NB: HelloSign sends a post object with key "json" that is set to an actual
        string of JSON
        """
        data = self.extract_json_data(body=request.POST.get('json'))  # extract json

        signature_request_id = data.get('signature_request', {}).get('signature_request_id', None)

        event_type = data['event'].get('event_type')

        if signature_request_id is None:
            logger.error('Hellosign signature_request_id: %s is None' % signature_request_id)

        else:
            # validate callback
            try:
                self.validate_callback(event_data=data)

            except Exception as e:
                return HttpResponseBadRequest('HelloSign webhook exception: %s' % e)

            logger.info('recieved webhook event: %s from HelloSign signature_request_id: %s' % (event_type, signature_request_id))

            # get the request object which must exist as its created when the object is sent for signing
            hellosign_request = get_object_or_404(HelloSignRequest, signature_request_id=signature_request_id)

            # create log object
            self.object = self.model.objects.create(request=hellosign_request,
                                                    event_type=event_type,
                                                    data=data)

            logger.info(u'Issuing hellosign_webhook_event_recieved signal')
            hellosign_webhook_event_recieved.send(sender=self,
                                                  signature_request_id=signature_request_id,
                                                  event_type=event_type,
                                                  data=data,
                                                  hellosign_request=hellosign_request,
                                                  hellosign_log=self.object)

        return render(request, self.template_name)
