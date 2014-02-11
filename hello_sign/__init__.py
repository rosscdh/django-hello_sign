# -*- coding: utf-8 -*-
__version_info__ = ('0', '1', '5')
__version__ = '.'.join(__version_info__)

from django.conf import settings

import logging
logger = logging.getLogger('django.request')


HELLOSIGN_AUTHENTICATION = getattr(settings, 'HELLOSIGN_AUTHENTICATION', None)
HELLOSIGN_API_KEY = getattr(settings, 'HELLOSIGN_API_KEY', None)
HELLOSIGN_CLIENT_ID = getattr(settings, 'HELLOSIGN_CLIENT_ID', None)
HELLOSIGN_CLIENT_SECRET = getattr(settings, 'HELLOSIGN_CLIENT_SECRET', None)

assert HELLOSIGN_AUTHENTICATION is not None, 'You must define a settings.HELLOSIGN_AUTHENTICATION see: http://www.hellosign.com/api/reference#EventHashVerification *NB* ensure you are logged in as your primary account'
assert HELLOSIGN_API_KEY is not None, 'You must define a settings.HELLOSIGN_API_KEY see: http://www.hellosign.com/home/myAccount/current_tab/integrations'
assert HELLOSIGN_CLIENT_ID is not None, 'You must define a settings.HELLOSIGN_CLIENT_ID see: http://www.hellosign.com/home/myAccount/current_tab/integrations'
assert HELLOSIGN_CLIENT_SECRET is not None, 'You must define a settings.HELLOSIGN_CLIENT_SECRET see: http://www.hellosign.com/home/myAccount/current_tab/integrations'