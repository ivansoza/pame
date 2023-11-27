from django.contrib import admin

from .models import Defensorias,notificacionesAceptadas,Relacion,Qrfirma, NotificacionConsular, FirmaNotificacionConsular

admin.site.register(Defensorias)
admin.site.register(notificacionesAceptadas)
admin.site.register(Relacion)
admin.site.register(Qrfirma)
admin.site.register(NotificacionConsular)
admin.site.register(FirmaNotificacionConsular)


