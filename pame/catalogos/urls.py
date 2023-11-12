from django.urls import path,include

from . import views
from .views import crearAutoridad, listAutoridades,agregarAutoridadActuante,crearAutoridadActuante, quitarAutoridadActuante, listaTraductores, crearTraductor, editarTraductor, editarEstatusActuante, editarAutoridad, RepresentantesLegalesListView, RepresentanteLegalCreateView, RepresentanteLegalUpdateView, listExtranjerosRepresentantes
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
    path('representantes-legales/actualizar-estatus/<int:pk>/', RepresentanteLegalUpdateView.as_view(), name='representante-legal-update'),
    path('representantes-legales/extranjeros/', listExtranjerosRepresentantes.as_view(), name='representante-legal-extranjeros'),

]
