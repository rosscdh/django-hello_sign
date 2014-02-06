# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand, CommandError

import pprint
import requests
import urlparse

PPP = pprint.PrettyPrinter(indent=4)


class Command(BaseCommand):
    """
    Command to register your apps webhook callback_url with hellosign
    Manually:
    using https://github.com/jkbr/httpie
    http -a <email>:<password> -f POST https://api.hellosign.com/v3/account callback_url=https://2b2dea03.ngrok.com/sign/hellosign/event/
    """
    args = '<callback_url>'
    help = "Register or update the callback_url for your environment at hellosign"
    endpoint = 'https://api.hellosign.com/v3/account'
    service = requests

    def handle(self, *args, **options):
        url = reverse('sign:hellosign_webhook_event')
        self.site = Site.objects.get(pk=settings.SITE_ID)
        self.callback_url = urlparse.urljoin(self.site.domain, url)

        try:
            self.callback_url = args[0]
        except IndexError:
            #
            # Allow default to be used
            #
            PPP.pprint('Using default webhook_url sign:hellosign_webhook_event: %s' % self.callback_url)

        resp = self.service.post(self.endpoint, auth=settings.HELLOSIGN_AUTHENTICATION, data={'callback_url': self.callback_url})

        print('Status Code: %s' % resp.status_code)
        PPP.pprint(resp.json())
