from asyncio import format_helpers
from django.contrib import admin
from .models import TipoAcuerdo, Acuerdo, PDFGenerado, NotificacionesGlobales, Documentos, TiposDoc, ClasificaDoc
from .models import Repositorio, NoProceso, Extranjero
from vigilancia.models import NoProceso, Extranjero
class RepositorioAdmin(admin.ModelAdmin):
    list_display = ('nup', 'fechaGeneracion', 'delTipo', 'delaEstacion', 'delResponsable', 'archivo_link')
    list_filter = ('delaEstacion', 'delTipo')
    search_fields = ('nup__nup', 'delResponsable')
    ordering = ('-fechaGeneracion', 'nup')

    def archivo_link(self, obj):
        if obj.archivo:
            return '<a href="{}">Descargar</a>'.format(obj.archivo.url)
        return "Sin archivo"
    archivo_link.short_description = 'Archivo'

admin.site.register(Repositorio, RepositorioAdmin)



admin.site.register(TiposDoc)
admin.site.register(ClasificaDoc)


admin.site.register(TipoAcuerdo)

admin.site.register(Acuerdo)

admin.site.register(PDFGenerado)

class NotificacionesGlobalesAdmin(admin.ModelAdmin):
    list_display = ('tipo_notificacion', 'fecha_hora')
    search_fields = ('tipo_notificacion', )
    list_filter = ('fecha_hora', )
    ordering = ('-fecha_hora', )

admin.site.register(NotificacionesGlobales, NotificacionesGlobalesAdmin)


class DocumentsAdmin(admin.ModelAdmin):
    list_display=("nup", "acuerdo_inicio","oficio_llamada","oficio_derechos_obligaciones")

admin.site.register(Documentos, DocumentsAdmin)
