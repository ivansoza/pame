from django.contrib import admin

from .models import Defensorias,notificacionesAceptadas,Relacion

admin.site.register(Defensorias)
admin.site.register(notificacionesAceptadas)
admin.site.register(Relacion)

