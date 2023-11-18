from django.contrib import admin
from .models import Tipos, Estatus, Estado, Estacion, Responsable,Salida, Estancia, Relacion, AutoridadesActuantes, Autoridades, RepresentantesLegales, \
    Oficina

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
admin.site.register(AutoridadesActuantes)
admin.site.register(Autoridades)

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