from django.contrib import admin
from .models import Inventario, Pertenencias, Valores, EnseresBasicos, Pertenencia_aparatos, valoresefectivo
# Register your models here.

class InventarioAdmin(admin.ModelAdmin):
    list_display = ('foloInventario', 'unidadMigratoria', 'horaEntrega', 'archivo_validacion', 'extranjero_nombre')
    
    def archivo_validacion(self, obj):
        return obj.validacion.name if obj.validacion else 'No proporcionado'
    archivo_validacion.short_description = 'Documento de Validación'

    def extranjero_nombre(self, obj):
        return str(obj.noExtranjero)
    extranjero_nombre.short_description = 'No Extranjero'

admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Pertenencias)

admin.site.register(Valores)
admin.site.register(EnseresBasicos)
admin.site.register(Pertenencia_aparatos)
admin.site.register(valoresefectivo)