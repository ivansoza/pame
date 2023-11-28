from django.urls import path,include
from .views import listaExtranjertoAlegatos, creaAlegato, subirDocumentosAlegatos, listaDocumentosAlegatos, modlaes
from .views import generar_qr_firmas_alegato, firma_autoridad_actuante_alegato, firma_representante_legal_alegato, verificar_firmas, firma_testigo1_alegato, firma_testigo2_alojamiento
from .views import verificar_firma_autoridad_actuante_alegato, verificar_firma_representante_legal_alegato, estado_firmas_alegato, verificar_firma_testigo1_alegato, verificar_firma_testigo2_alegato, obtener_datos_alegato
from .views import listaExtranjertoNoFirma, creaConstanciaFirma, CrearConstanciaAjax, PresentaPruebas
from .views import generar_qr_firmas_constancia, firma_autoridad_actuante_constancia, firma_representante_legal_constancia, firma_testigo1_constancia, firma_testigo2_constancia
from .views import verificar_firma_autoridad_actuante_constancia, verificar_firma_representante_legal_constancia, verificar_firma_testigo1_constancia, verificar_firma_testigo2_constancia, estado_firmas_constancia, verificar_firmas1, obtener_datos_constancia
#-----------------------DESAHOGO------------------------------------
from . views import listaExtranjerosDesahogo
urlpatterns = [
    path("listaExtranjerosAlegatos/", listaExtranjertoAlegatos.as_view(), name="listaExtranjerosAlegatos"),
    path("crearAlegato/<int:pk>/", creaAlegato.as_view(), name="crearAlegato"),
    path('documentosAlegato/<int:alegato_id>/', subirDocumentosAlegatos.as_view(), name='documentosAlegato'),
    path('documentosAlegatos/<int:pk>/', listaDocumentosAlegatos.as_view(), name='documentosAlegatos'),
    path('modalAlegatos/<int:pk>/', modlaes.as_view(), name='modalAlegatos'),

#-----------------------------FIRMA-------------------------------------------------------
    path('generar_qr_alegato/<str:tipo_firma>/<int:alegato_id>/', generar_qr_firmas_alegato, name='generar_qr_firmas_alegato'),
    path('firma_autoridad_actuante_alegato/<int:alegato_id>/', firma_autoridad_actuante_alegato, name='firma_autoridad_actuante_alegato'),
    path('firma_testigo1_alegato/<int:alegato_id>/', firma_testigo1_alegato, name='firma_testigo1_alegato'),
    path('firma_representante_legal_alegato/<int:alegato_id>/', firma_representante_legal_alegato, name='firma_representante_legal_alegato'),
    path('firma_testigo2_alegato/<int:alegato_id>/', firma_testigo2_alojamiento, name='firma_testigo2_alegato'),


    path('verificar_firmas/<int:alegato_id>/', verificar_firmas, name='verificar_firmas'),


    path('verificar_firma/autoridadActuante_alegato/<int:alegato_id>/', verificar_firma_autoridad_actuante_alegato, name='verificar_firma_autoridad_actuante_alegato'),
    path('verificar_firma/representanteLegal_alegato/<int:alegato_id>/', verificar_firma_representante_legal_alegato, name='verificar_firma_representante_legal_alegato'),
    path('verificar_firma/testigo1_alegato/<int:alegato_id>/', verificar_firma_testigo1_alegato, name='verificar_firma_testigo1_alegato'),
    path('verificar_firma/testigo2_alegato/<int:alegato_id>/', verificar_firma_testigo2_alegato, name='verificar_firma_testigo2_alegato'),

    path('estado_firmas_alegato/<int:alegato_id>/', estado_firmas_alegato, name='estado_firmas_alegato'),
    path('datos_alegato/<int:alegato_id>/', obtener_datos_alegato, name='datos_alegato'),

    path('crear-constancia/<str:nup_id>/', CrearConstanciaAjax.as_view(), name='crear-constancia_ajax'),

#----------------------CONSTANCIA DE NO FIRMAS-------------------------------------------------
    path("listaExtranjerosFirma/", listaExtranjertoNoFirma.as_view(), name="listaExtranjerosFirma"),
    path("crearConstanciaNoFirma/<int:pk>/", creaConstanciaFirma.as_view(), name="crearConstanciaNoFirma"),
    path('generar_qr_constancia/<str:tipo_firma>/<int:constancia_id>/', generar_qr_firmas_constancia, name='generar_qr_firmas_alegato'),
    path('firma_autoridad_actuante_constancia/<int:constancia_id>/', firma_autoridad_actuante_constancia, name='firma_autoridad_actuante_constancia'),
    path('firma_representante_legal_constancia/<int:constancia_id>/', firma_representante_legal_constancia, name='firma_representante_legal_constancia'),
    path('firma_testigo1_constancia/<int:constancia_id>/', firma_testigo1_constancia, name='firma_testigo1_constancia'),
    path('firma_testigo2_constancia/<int:constancia_id>/', firma_testigo2_constancia, name='firma_testigo2_constancia'),
    path('verificar_firma/autoridadActuante_constancia/<int:constancia_id>/', verificar_firma_autoridad_actuante_constancia, name='verificar_firma_autoridad_actuante_constancia'),
    path('verificar_firma/representanteLegal_constancia/<int:constancia_id>/', verificar_firma_representante_legal_constancia, name='verificar_firma_representante_legal_constancia'),
    path('verificar_firma/testigo1_constancia/<int:constancia_id>/', verificar_firma_testigo1_constancia, name='verificar_firma_testigo1_constancia'),
    path('verificar_firma/testigo2_constancia/<int:constancia_id>/', verificar_firma_testigo2_constancia, name='verificar_firma_testigo2_constancia'),
    path('estado_firmas_constancia/<int:constancia_id>/', estado_firmas_constancia, name='estado_firmas_constancia'),
    path('verificar_firmas1/<int:constancia_id>/', verificar_firmas1, name='verificar_firmas1'),
    path('datos_constancia/<int:constancia_id>/', obtener_datos_constancia, name='datos_constancia'),


#---------------------------Presenta------------------------
    path('presenta/<int:pk>/', PresentaPruebas.as_view(), name='presenta'),


#-----------------------------
    path('listaDesahogo/', listaExtranjerosDesahogo.as_view(), name='listaDesahogo'),

]