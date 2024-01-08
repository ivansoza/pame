from django.urls import path, include
from .views import editarDefensoria, crearRelacionAjax, firma_autoridad_actuante_nom_ext, firma_extranjero_nom_ext, firma_representante_legal_nom_ext, firma_testigo1_nom_ext, firma_testigo2_nom_ext, firma_traductor_nom_ext, generar_qr_firmas_nombramiento_Externo, verificar_firma_autoridad_actuante_nom_ext, verificar_firma_extranjero_nom_ext, verificar_firma_representante_legal_nom_ext, verificar_firma_testigo1_nom_ext, verificar_firma_testigo2_nom_ext, verificar_firma_traductor_nom_ext
from .views import listExtranjerosDefensoria,notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia, createDEfensoria,CrearNotificacionConsulado,firma_autoridad_actuante_notifi_consul,generar_qr_firma_notificacion_consular,verificar_firma_autoridad_actuante, CrearNotificacionComar, CrearNotificacionFiscalia,\
generar_qr_firma_notificacion_comar, generar_qr_firma_notificacion_fiscalia, firma_autoridad_actuante_notifi_fiscalia, firma_autoridad_actuante_notifi_comar ,verificar_firma_autoridad_actuante_comar, verificar_firma_autoridad_actuante_fiscalia

from .views import notificar,tabladefensores,SubirArchivo,modalnotificar, listExtranjerosComar, listExtranjerosConsulado, listExtranjerosFiscalia,CrearNotificacionConsulado,firma_autoridad_actuante_notifi_consul,generar_qr_firma_notificacion_consular,verificar_firma_autoridad_actuante
from .views import generar_qr_firmas_noti,firma_autoridad_actuante_notificacion, verificar_firma_autoridad_actuante_notificacion, estado_firmas_notificacion, verificar_firmas_no, selectDefensoria
from . views import generar_qr_firmas_defensoria, firma_autoridad_actuante_defensoria, estado_firmas_defensoria, verificar_firmas_defensoria, obtener_datos_defensoria, verificar_firma_autoridad_actuante_defensoria, DocumentoRespuestaDefensoriaCreateView, CrearNombramientoExterno,obtener_datos_nombramiento_externo,CrearNombramientoInterno
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
    path('generar_qr_defensoria/<str:tipo_firma>/<int:defensoria_id>/', generar_qr_firmas_defensoria, name='generar_qr_firmas_defensoria'),
    path('firma_autoridad_actuante_defensoria/<int:defensoria_id>/', firma_autoridad_actuante_defensoria, name='firma_autoridad_actuante_defensoria'),
    path('verificar_firma/autoridadActuante_defensoria/<int:defensoria_id>/', verificar_firma_autoridad_actuante_defensoria, name='verificar_firma_autoridad_actuante_defensoria'),
    path('estado_firmas_defensoria/<int:defensoria_id>/', estado_firmas_defensoria, name='estado_firmas_defensoria'),
    path('verificar_firmas_defensoria/<int:defensoria_id>/', verificar_firmas_defensoria, name='verificar_firmas_defensoria'),
    path('datos_defensoria/<int:defensoria_id>/', obtener_datos_defensoria, name='datos_defensoria'),
    path('respuesta/defensoria/<int:extranjero_defensoria_id>/<str:nup_id>/', DocumentoRespuestaDefensoriaCreateView.as_view(), name='respuestaDefensoria'),


    # Generar nombramiento
    path('crear-nombramiento/<str:nup_id>/', CrearNombramientoInterno.as_view(), name='CrearNombramiento'),
    path('crear-nombramiento-externo/<str:nup_id>/', CrearNombramientoExterno.as_view(), name='CrearNombramientoExterno'),

    path('firma_autoridad_actuante_nombramiento_ext/<int:nombramiento_externo_id>/', firma_autoridad_actuante_nom_ext, name='firma_autoridad_actuante'),
    path('firma_representante_legal_nombramiento_ext/<int:nombramiento_externo_id>/', firma_representante_legal_nom_ext, name='firma_representante_legal'),
    path('firma_traductor_nombramiento_ext/<int:nombramiento_externo_id>/', firma_traductor_nom_ext, name='firma_traductor'),
    path('firma_extranjero_nombramiento_ext/<int:nombramiento_externo_id>/', firma_extranjero_nom_ext, name='firma_extranjero'),
    path('firma_testigo1_nombramiento_ext/<int:nombramiento_externo_id>/', firma_testigo1_nom_ext, name='firma_testigo1'),
    path('firma_testigo2_nombramiento_ext/<int:nombramiento_externo_id>/', firma_testigo2_nom_ext, name='firma_testigo2'),
    path('generar_qr_nomb_ext/<str:tipo_firma>/<int:nombramiento_externo_id>/', generar_qr_firmas_nombramiento_Externo, name='generar_qr_firmas'),
    path('verificar_firma_nom_ext/autoridadActuante/<int:nombramiento_externo_id>/', verificar_firma_autoridad_actuante_nom_ext, name='verificar_firma_autoridad_actuante'),
    path('verificar_firma_nom_ext/representanteLegal/<int:nombramiento_externo_id>/', verificar_firma_representante_legal_nom_ext, name='verificar_firma_representante_legal'),
    path('verificar_firma_nom_ext/traductor/<int:nombramiento_externo_id>/', verificar_firma_traductor_nom_ext, name='verificar_firma_traductor'),
    path('verificar_firma_nom_ext/extranjero/<int:nombramiento_externo_id>/', verificar_firma_extranjero_nom_ext, name='verificar_firma_extranjero'),
    path('verificar_firma_nom_ext/testigo1/<int:nombramiento_externo_id>/', verificar_firma_testigo1_nom_ext, name='verificar_firma_testigo1'),
    path('verificar_firma_nom_ext/testigo2/<int:nombramiento_externo_id>/', verificar_firma_testigo2_nom_ext, name='verificar_firma_testigo2'),
    path('datos_nombramiento_externo/<int:nombramiento_externo_id>/', obtener_datos_nombramiento_externo, name='obtener_datos_nombramiento_externo'),

]

