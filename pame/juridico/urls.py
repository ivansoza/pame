from django.urls import path, include

from .views import homeJuridicoGeneral, homeJuridicoResponsable, homeJuridico, manejar_imagen
from .views import notificacionDO, notificacionDOAC, notificacionDOVP, notificacionDOGeneral
urlpatterns = [
    path("", homeJuridico, name="homeJuridico"),
    path('juridico-general', homeJuridicoGeneral, name="homeJuridicoGeneral"),
    path('juridico-responsable', homeJuridicoResponsable, name="homeJuridicoResponsable"),
    path('manejar_imagen/', manejar_imagen, name='manejar_imagen'),
    path('notificacion_d_o/<int:extranjero_id>/<int:puesta_id>/', notificacionDO.as_view(), name="notificacion_d_o"),
    path('notificacionDOAC/<int:extranjero_id>/<int:puesta_id>/', notificacionDOAC.as_view(), name="notificacionDOAC"),
    path('notificacionDOVP/<int:extranjero_id>/<int:puesta_id>/', notificacionDOVP.as_view(), name="notificacionDOVP"),
    path('notificacionGeneralDO/<int:extranjero_id>/', notificacionDOGeneral.as_view(), name="notificacionGeneralDO"),

]
