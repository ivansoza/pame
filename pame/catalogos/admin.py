from django.contrib import admin
from .models import Tipos, Estatus, Estado, Estacion, Responsable,Salida, Estancia, Relacion

admin.site.register(Tipos)

admin.site.register(Estatus)

admin.site.register(Estado)

admin.site.register(Estacion)

admin.site.register(Responsable)
admin.site.register(Salida)
admin.site.register(Estancia)
admin.site.register(Relacion)