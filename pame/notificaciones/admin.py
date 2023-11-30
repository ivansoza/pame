from django.contrib import admin

from .models import Defensorias,notificacionesAceptadas,Relacion,Qrfirma, NotificacionConsular, FirmaNotificacionConsular, FirmaNotificacionComar, FirmaNotificacionFiscalia, NotificacionConsular, NotificacionConsular, NotificacionCOMAR,NotificacionFiscalia

admin.site.register(Defensorias)
admin.site.register(notificacionesAceptadas)
admin.site.register(Relacion)
admin.site.register(Qrfirma)
admin.site.register(NotificacionConsular)
admin.site.register(FirmaNotificacionConsular)
admin.site.register(FirmaNotificacionComar)
admin.site.register(FirmaNotificacionFiscalia)
admin.site.register(NotificacionCOMAR)
admin.site.register(NotificacionFiscalia)


