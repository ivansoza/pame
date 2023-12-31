from django.urls import path,include

from . import views
from .views import crearAutoridad, listAutoridades,agregarAutoridadActuante,crearAutoridadActuante, quitarAutoridadActuante, listaTraductores, crearTraductor, editarTraductor, editarEstatusActuante, editarAutoridad, RepresentantesLegalesListView, RepresentanteLegalCreateView, RepresentanteLegalUpdateView, listExtranjerosRepresentantes,AsignacionRepresentanteCreateView, AsignacionRepresentanteUpdateView,AsignacionRepresentanteComparecenciaCreateView, RepresentanteLegalCreateViewComparecencia 
urlpatterns = [
    path("Responsable/",views.responsableCrear, name="addResponsable"),
    path("crearAutoridad/",crearAutoridad.as_view(), name="crearAutoridad"),
    path("listaAutoridad/",listAutoridades.as_view(), name="listaAutoridad"),
    path("agregaraAutoridadActuante/",agregarAutoridadActuante.as_view(), name="agregaraAutoridadActuante"),
    path("crearAutoridadActuante/<int:autoridad_id>/",crearAutoridadActuante.as_view(), name="crearAutoridadActuante"),
    path("eliminarAutoridadActuante/<int:pk>/s",quitarAutoridadActuante.as_view(), name="eliminarAutoridadActuante"),
    path("listaTraductores/",listaTraductores.as_view(), name="listaTraductores"),
    path("crearTraductores/",crearTraductor.as_view(), name="crearTraductores"),
    path("editarTraductor/<int:pk>/",editarTraductor.as_view(), name="editarTraductor"),
    path("editarActuante/<int:pk>/",editarEstatusActuante.as_view(), name="editarActuante"),
    path("editarAutoridad/<int:pk>/",editarAutoridad.as_view(), name="editarAutoridad"),

    #SECCION DE REPRESENTANTES LEGALES
    path('representantes-legales/', RepresentantesLegalesListView.as_view(), name='representantes-legales-list'),
    path('representantes-legales/nuevo/', RepresentanteLegalCreateView.as_view(), name='representante-legal-create'),
    path('representantes-legales/nuevo/comparecencia', RepresentanteLegalCreateViewComparecencia.as_view(), name='representante-legal-create-comparecencia'),
    path('representantes-legales/actualizar-estatus/<int:pk>/', RepresentanteLegalUpdateView.as_view(), name='representante-legal-update'),
    path('representantes-legales/extranjeros/', listExtranjerosRepresentantes.as_view(), name='representante-legal-extranjeros'),
    path('asignar-representante/<str:nup>/', AsignacionRepresentanteCreateView.as_view(), name='asignar-representante'),
    path('asignar-representante-comparecencia/<str:nup>/', AsignacionRepresentanteComparecenciaCreateView.as_view(), name='asignar-representante-comparecencia'),

    path('editar-representante/<int:id>/', AsignacionRepresentanteUpdateView.as_view(), name='editar-representante'),



    path('generar_qr/<int:autoridad_actuante_id>/', views.generar_qr_firma_autoridad_actuante, name='generar_qr_firma_autoridad_actuante'),

]
