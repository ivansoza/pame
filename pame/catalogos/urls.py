from django.urls import path,include

from . import views
from .views import crearAutoridad, listAutoridades,agregarAutoridadActuante,crearAutoridadActuante, quitarAutoridadActuante
urlpatterns = [
    path("Responsable/",views.responsableCrear, name="addResponsable"),
    path("crearAutoridad/",crearAutoridad.as_view(), name="crearAutoridad"),
    path("listaAutoridad/",listAutoridades.as_view(), name="listaAutoridad"),
    path("agregaraAutoridadActuante/",agregarAutoridadActuante.as_view(), name="agregaraAutoridadActuante"),
    path("crearAutoridadActuante/<int:autoridad_id>/",crearAutoridadActuante.as_view(), name="crearAutoridadActuante"),
    path("eliminarAutoridadActuante/<int:pk>/s",quitarAutoridadActuante.as_view(), name="eliminarAutoridadActuante"),

]
