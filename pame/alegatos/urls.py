from django.urls import path,include
from .views import listaExtranjertoAlegatos, creaAlegato, subirDocumentosAlegatos, listaDocumentosAlegatos, modlaes
from .views import generar_qr_firmas_alegato, firma_autoridad_actuante_alegato, firma_representante_legal_alegato, verificar_firmas, firma_testigo1_alegato, firma_testigo2_alojamiento
from .views import verificar_firma_autoridad_actuante_alegato, verificar_firma_representante_legal_alegato, estado_firmas_alegato, verificar_firma_testigo1_alegato, verificar_firma_testigo2_alegato
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

]