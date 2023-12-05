from django.urls import path, include
from .views import editarDefensoria, crearRelacionAjax
from .views import listExtranjerosDefensoria,notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia, createDEfensoria,CrearNotificacionConsulado,firma_autoridad_actuante_notifi_consul,generar_qr_firma_notificacion_consular,verificar_firma_autoridad_actuante, CrearNotificacionComar, CrearNotificacionFiscalia,\
generar_qr_firma_notificacion_comar, generar_qr_firma_notificacion_fiscalia, firma_autoridad_actuante_notifi_fiscalia, firma_autoridad_actuante_notifi_comar ,verificar_firma_autoridad_actuante_comar, verificar_firma_autoridad_actuante_fiscalia

from .views import notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia,CrearNotificacionConsulado,firma_autoridad_actuante_notifi_consul,generar_qr_firma_notificacion_consular,verificar_firma_autoridad_actuante
from .views import generar_qr_firmas_noti,firma_autoridad_actuante_notificacion, verificar_firma_autoridad_actuante_notificacion, estado_firmas_notificacion, verificar_firmas_no, selectDefensoria
from . views import generar_qr_firmas_defensoria, firma_autoridad_actuante_defensoria, estado_firmas_defensoria, verificar_firmas_defensoria, obtener_datos_defensoria, verificar_firma_autoridad_actuante_defensoria, DocumentoRespuestaDefensoriaCreateView
urlpatterns = [
    path('defensoria/', listExtranjerosDefensoria.as_view(), name="defensoria"),
    # path('defensores', views.defensores, name='defensores'),
    path('notificacion/<int:pk>/', notificar.as_view(), name='notificacion'),
    path('listdefensores/', tabladefensores.as_view(), name='listdefensores'),
    path('modal/', SubirArchivo.as_view(), name='modale'),
    # path('firma/', firma,name='firma'),
    path('listnotificacion/<int:extranjero_id>/<int:defensoria_id>/', modalnotificar.as_view(), name='listnotificacion'),
    # Notificaciones
    path("comar/", listExtranjerosComar.as_view(), name="listExtranjerosComar"),

    # consulado
    path("consulado/", listExtranjerosConsulado.as_view(), name="listExtranjerosConsulado"),
    path('crear-notificacion-consular/<str:nup_id>/', CrearNotificacionConsulado.as_view(), name='crear_notificacion-consular'),
    
    path('generar_qr/<str:tipo_firma>/<int:consulado_id>/', generar_qr_firma_notificacion_consular, name='generar_qr_firmas_notifi_consular'),
    path('firma_autoridad_actuante/<int:consulado_id>/', firma_autoridad_actuante_notifi_consul, name='firma_autoridad_actuante_notifi_consul'),
    path('verificar_firma/autoridadActuante/<int:consulado_id>/', verificar_firma_autoridad_actuante, name='verificar_firma_autoridad_actuante_consular'),



    # fin de consulado
    path("fiscalia/", listExtranjerosFiscalia.as_view(), name="listExtranjerosFiscalia"),


    path('crear-notificacion-comar/<str:nup_id>/', CrearNotificacionComar.as_view(), name='crear_notificacion-comar'),
    path('crear-notificacion-fiscalia/<str:nup_id>/', CrearNotificacionFiscalia.as_view(), name='crear_notificacion-fiscalia'),
    path('generar_qr-comar/<str:tipo_firma>/<int:comar_id>/', generar_qr_firma_notificacion_comar, name='generar_qr_firma_notificacion_comar'),
    path('generar_qr-fiscalia/<str:tipo_firma>/<int:fiscalia_id>/', generar_qr_firma_notificacion_fiscalia, name='generar_qr_firma_notificacion_fiscalia'),

    path('firma_autoridad_actuante-comar/<int:comar_id>/', firma_autoridad_actuante_notifi_comar, name='firma_autoridad_actuante_notifi_comar'),
    path('firma_autoridad_actuante-fiscalia/<int:fiscalia_id>/', firma_autoridad_actuante_notifi_fiscalia, name='firma_autoridad_actuante_notifi_fiscalia'),

    path('verificar_firma-comar/autoridadActuante/<int:comar_id>/', verificar_firma_autoridad_actuante_comar, name='verificar_firma_autoridad_actuante_comar'),
    path('verificar_firma-fiscalia/autoridadActuante/<int:fiscalia_id>/', verificar_firma_autoridad_actuante_fiscalia, name='verificar_firma_autoridad_actuante_fiscalia'),
    path('generar_qr_notificaciones/<str:tipo_firma>/<int:notificacion_id>/', generar_qr_firmas_noti, name='generar_qr_firmas_notificaciones'),

    path('firma_autoridad_actuante_notificacion/<int:noti_id>/', firma_autoridad_actuante_notificacion, name='firma_autoridad_actuante_notificacion'),
    path('verificar_firma/autoridadActuante_notificacion/<int:noti_id>/', verificar_firma_autoridad_actuante_notificacion, name='verificar_firma_autoridad_actuante_notificacion'),
    path('estado_firmas_notificacion/<int:noti_id>/', estado_firmas_notificacion, name='estado_firmas_notificacion'),
    path('verificar_firmas_no/<int:noti_id>/', verificar_firmas_no, name='verificar_firmas_no'),
    path("crearDefensoria/", createDEfensoria.as_view(), name="crearDefensoria"),
    path("editarDefensoria/<int:pk>", editarDefensoria.as_view(), name="editarDefensoria"),







#-----------------------Defensoria (modulo: seleccion y notificacion)------------
    path('seleccionarDefensoria/<int:pk>/', selectDefensoria.as_view(), name='seleccionarDefensoria'),
    path('crearNotificacion/<str:nup_id>/<int:defensoria_id>/', crearRelacionAjax.as_view(), name='crearNotificacion'),
    path('generar_qr_defensoria/<str:tipo_firma>/<int:constancia_id>/', generar_qr_firmas_defensoria, name='generar_qr_firmas_defensoria'),
    path('firma_autoridad_actuante_defensoria/<int:constancia_id>/', firma_autoridad_actuante_defensoria, name='firma_autoridad_actuante_defensoria'),
    path('verificar_firma/autoridadActuante_defensoria/<int:constancia_id>/', verificar_firma_autoridad_actuante_defensoria, name='verificar_firma_autoridad_actuante_defensoria'),
    path('estado_firmas_defensoria/<int:constancia_id>/', estado_firmas_defensoria, name='estado_firmas_defensoria'),
    path('verificar_firmas_defensoria/<int:constancia_id>/', verificar_firmas_defensoria, name='verificar_firmas_defensoria'),
    path('datos_defensoria/<int:constancia_id>/', obtener_datos_defensoria, name='datos_defensoria'),
    path('respuesta/defensoria/<int:extranjero_defensoria_id>/<str:nup_id>/', DocumentoRespuestaDefensoriaCreateView.as_view(), name='respuestaDefensoria'),


]
