from django.contrib import admin

from .models import HelloSignRequest, HelloSignLog


class HelloSignRequestAdmin(admin.ModelAdmin):
    list_display = ('source_object', 'signature_request_id', 'dateof',)
    search_fields = ('signature_request_id',)


class HelloSignLogAdmin(admin.ModelAdmin):
    list_display = ('request', 'event_type', 'dateof',)
    list_filter = ['event_type']
    search_fields = ('event_type',)


admin.site.register(HelloSignRequest, HelloSignRequestAdmin)
admin.site.register(HelloSignLog, HelloSignLogAdmin)
