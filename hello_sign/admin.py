from django.contrib import admin

from .models import HelloSignRequest, HelloSignLog, HelloSignSigningUrl


class HelloSignRequestAdmin(admin.ModelAdmin):
    list_display = ('source_object', 'signature_request_id', 'dateof',)
    search_fields = ('signature_request_id',)


class HelloSignLogAdmin(admin.ModelAdmin):
    list_display = ('request', 'event_type', 'dateof',)
    list_filter = ['event_type']
    search_fields = ('event_type',)


class HelloSignSigningUrlAdmin(admin.ModelAdmin):
    list_display = ('request', 'signature_id', 'has_been_viewed', 'expires_at', 'dateof',)
    list_filter = ['has_been_viewed']
    search_fields = ('request', 'signature_id',)


admin.site.register(HelloSignRequest, HelloSignRequestAdmin)
admin.site.register(HelloSignLog, HelloSignLogAdmin)
admin.site.register(HelloSignSigningUrl, HelloSignSigningUrlAdmin)

