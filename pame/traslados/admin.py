from django.contrib import admin
from .models import Traslado, SolicitudTraslado, ExtranjeroTraslado, Alojamiento
# Register your models here.
admin.site.register(ExtranjeroTraslado)
admin.site.register(Alojamiento)

class SolicitudTrasladoAdmin(admin.ModelAdmin):
    list_display = ["extranjero", "estacion_origen","estacion_destino","estado","motivo","fecha_solicitud","fecha_aceptacion"]



class TrasladoAdmin(admin.ModelAdmin):
    list_display = ["nombreAutoridadEnvia","estacion_origen", "estacion_destino","fechaSolicitud","fecha_aceptacion"]
admin.site.register(SolicitudTraslado, SolicitudTrasladoAdmin)

admin.site.register(Traslado, TrasladoAdmin)
