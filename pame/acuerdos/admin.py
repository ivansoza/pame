from django.contrib import admin
from .models import TipoAcuerdo, Acuerdo, PDFGenerado, NotificacionesGlobales, Documentos

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
