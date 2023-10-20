from django.contrib import admin

# Register your models here.
from .models import NotificacionDerechos


class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('fechaAceptacion', 'get_extranjero', 'estacion', 'estatus_notificacion')
    search_fields = ('no_proceso__extranjero__nombreExtranjero', 'no_proceso__nup')
    list_filter = ('fechaAceptacion', 'estacion', 'estatus_notificacion')

    def get_extranjero(self, obj):
        return obj.no_proceso.extranjero.nombreExtranjero
    get_extranjero.short_description = 'Extranjero Asociado'

admin.site.register(NotificacionDerechos, NotificacionAdmin)