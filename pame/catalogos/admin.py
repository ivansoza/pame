from django.contrib import admin
from .models import Tipos, Estatus, Estado, Estacion, Responsable,Salida, Estancia, Relacion, AutoridadesActuantes, Autoridades, RepresentantesLegales, \
    Oficina, FirmaAutoridad
from .models import Consulado
from vigilancia.models import Nacionalidad  # Asegúrate de que la importación esté correctamente ubicada
from django.utils.html import format_html




from vigilancia.models import NoProceso
admin.site.register(Tipos)

admin.site.register(Estatus)

admin.site.register(Estado)

class EstacionAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'nombre', 'oficina_display')

    def oficina_display(self, obj):
        # Devuelve el nombre de la oficina a la que pertenece la estación
        return f"{obj.oficina.nombre} {obj.estado.estado}" if obj.oficina else ''

    oficina_display.short_description = 'Oficina y Estado'  # Define el encabezado en la interfaz de administración

admin.site.register(Estacion, EstacionAdmin)

admin.site.register(Responsable)
admin.site.register(Salida)
admin.site.register(Estancia)
admin.site.register(Relacion)
class AutoridadesActuantesAdmin(admin.ModelAdmin):
    list_display = ('autoridad', 'estacion', 'estatus', 'cargo', 'fechaInicio', 'fechaFin', 'firma_button')

    def firma_button(self, obj):
        # Verifica si existe una firma asociada
        tiene_firma = FirmaAutoridad.objects.filter(autoridad=obj.autoridad).exists()
        if tiene_firma:
            # Botón en verde si la firma existe
            return format_html('<button style="background-color: green; color: white;">Firmado</button>')
        else:
            # Botón en rojo si no existe firma, incluyendo el ID
            return format_html('<button type="button" class="btn btn-danger" data-toggle="modal" data-target="#qrModal">Sin Firma</button>')

    firma_button.short_description = 'Firma'

# Registrar el modelo con la clase de administración personalizada
admin.site.register(AutoridadesActuantes, AutoridadesActuantesAdmin)

@admin.register(RepresentantesLegales)
class RepresentantesLegalesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'email', 'estatus', 'cedula', 'defensoria', 'estacion')
    list_filter = ('estatus', 'estacion',)
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'cedula',)
    ordering = ('nombre', 'apellido_paterno',)
    fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'email', 'estatus', 'cedula', 'defensoria', 'estacion')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Filtrar por estación si el usuario no es superusuario
        if not request.user.is_superuser:
            user_estacion = request.user.estacion
            return qs.filter(estacion=user_estacion)
        return qs

@admin.register(Oficina)
class OficinasAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'nombre', 'estado')




class ConsuladoAdmin(admin.ModelAdmin):
    list_display = ('pais', 'ciudad', 'calle', 'colonia',  'estado', 'codigo_postal')
    list_filter = ('pais', 'estado', 'ciudad')


admin.site.register(Consulado, ConsuladoAdmin)
