from django.contrib import admin
from .models import Tipos, Estatus, Estado, Estacion, Responsable, Extranjero , Puesta
# Register your models here.
admin.site.register(Tipos)
admin.site.register(Estatus)
admin.site.register(Estado)
admin.site.register(Estacion)
admin.site.register(Responsable)
admin.site.register(Extranjero)
admin.site.register(Puesta)