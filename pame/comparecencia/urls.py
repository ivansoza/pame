from django.urls import path, include
from .views import homeComparecencia, listExtranjerosComparecencia, CrearComparecencia, CrearComparecenciaAjax, generar_qr_firmas, firma_autoridad_actuante, firma_representante_legal,firma_traductor, firma_extranjero, firma_testigo1, firma_testigo2, firmExistente, verificar_firma_autoridad_actuante,verificar_firma_extranjero,verificar_firma_representante_legal,verificar_firma_testigo1,verificar_firma_testigo2,verificar_firma_traductor

urlpatterns = [
    path('', homeComparecencia, name="homeComparecencia"),
    path("extranjeros/", listExtranjerosComparecencia.as_view(), name="lisExtranjerosComparecencia"),
    path('crear/<str:nup_id>/', CrearComparecencia.as_view(), name='crear_comparecencia'),
    path('crear-comparecencia/<str:nup_id>/', CrearComparecenciaAjax.as_view(), name='crear_comparecencia_ajax'),
    path('generar_qr/<str:tipo_firma>/<int:comparecencia_id>/', generar_qr_firmas, name='generar_qr_firmas'),


    path('firma_autoridad_actuante/<int:comparecencia_id>/', firma_autoridad_actuante, name='firma_autoridad_actuante'),
    path('firma_representante_legal/<int:comparecencia_id>/', firma_representante_legal, name='firma_representante_legal'),
    path('firma_traductor/<int:comparecencia_id>/', firma_traductor, name='firma_traductor'),
    path('firma_extranjero/<int:comparecencia_id>/', firma_extranjero, name='firma_extranjero'),
    path('firma_testigo1/<int:comparecencia_id>/', firma_testigo1, name='firma_testigo1'),
    path('firma_testigo2/<int:comparecencia_id>/', firma_testigo2, name='firma_testigo2'),
    path('firma_existente/', firmExistente.as_view(), name='firma_existente_acuerdos'),
    path('verificar_firma/autoridadActuante/<int:comparecencia_id>/', verificar_firma_autoridad_actuante, name='verificar_firma_autoridad_actuante'),
    path('verificar_firma/representanteLegal/<int:comparecencia_id>/', verificar_firma_representante_legal, name='verificar_firma_representante_legal'),
    path('verificar_firma/traductor/<int:comparecencia_id>/', verificar_firma_traductor, name='verificar_firma_traductor'),
    path('verificar_firma/extranjero/<int:comparecencia_id>/', verificar_firma_extranjero, name='verificar_firma_extranjero'),
    path('verificar_firma/testigo1/<int:comparecencia_id>/', verificar_firma_testigo1, name='verificar_firma_testigo1'),
    path('verificar_firma/testigo2/<int:comparecencia_id>/', verificar_firma_testigo2, name='verificar_firma_testigo2'),


]
