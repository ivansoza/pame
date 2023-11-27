from django.urls import path, include
from .import views
from .views import defensoria,notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia,CrearNotificacionConsulado,firma_autoridad_actuante_notifi_consul,generar_qr_firma_notificacion_consular,verificar_firma_autoridad_actuante
from .views import generar_qr_firmas_noti,firma_autoridad_actuante_notificacion, verificar_firma_autoridad_actuante_notificacion, estado_firmas_notificacion, verificar_firmas_no

urlpatterns = [
    path('defensoria', defensoria.as_view(), name="defensoria"),
    path('defensores', views.defensores, name='defensores'),
    path('notificacion/<int:pk>/', notificar.as_view(), name='notificacion'),
    path('listdefensores/', tabladefensores.as_view(), name='listdefensores'),
    path('modal/', SubirArchivo.as_view(), name='modale'),
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

    path('generar_qr_notificaciones/<str:tipo_firma>/<int:notificacion_id>/', generar_qr_firmas_noti, name='generar_qr_firmas_notificaciones'),

    path('firma_autoridad_actuante_notificacion/<int:noti_id>/', firma_autoridad_actuante_notificacion, name='firma_autoridad_actuante_notificacion'),
    path('verificar_firma/autoridadActuante_notificacion/<int:noti_id>/', verificar_firma_autoridad_actuante_notificacion, name='verificar_firma_autoridad_actuante_notificacion'),
    path('estado_firmas_notificacion/<int:noti_id>/', estado_firmas_notificacion, name='estado_firmas_notificacion'),
    path('verificar_firmas_no/<int:noti_id>/', verificar_firmas_no, name='verificar_firmas_no'),

]
