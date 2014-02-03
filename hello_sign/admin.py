from django.contrib import admin

from .models import HelloSignRequest, HelloSignLog

admin.site.register([HelloSignRequest, HelloSignLog])
