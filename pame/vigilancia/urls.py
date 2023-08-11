from django.urls import path, include

from .views import inicioINMList, createPuestaINM, createExtranjeroINM, listarExtranjeros
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable,homePuestaINM, homePuestaVP

urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),
    path('seguridad-responsable/', homeSeguridadResponsable, name='homeSeguridadResponsable'),
    #path('autoridad-competente/',PuestaAutoridadCompetente.as_view(), name="addAutoridadCompetente"),
    #path('accion-migratoria/',puesta, name="addAccionMigratoria"),
    path('hospedaje/',addHospedaje, name="addHospedaje"),
    path('traslado/',addTraslado, name="addTraslado"),
  
    # path('seguridad/puesta-ac/', homePuestaAC, name='homePuestaAC'),
    path('seguridad/puesta-inm/', inicioINMList.as_view(), name='homePuestaINM'),
    path('seguridad/puesta-vp/', homePuestaVP, name='homePuestaVP'),
    path('seguridad/crear-puesta-inm/', createPuestaINM.as_view(), name='crearPuestaINM'),
    path('seguridad/crear-extranjero-inm/<int:puesta_id>/', createExtranjeroINM.as_view(), name='crearExtranjeroINM'),
    path('seguridad/listar-extranjero/<str:puesta_id>/', listarExtranjeros.as_view(), name='listarExtranjeros'),
    
    #path('accion-migratoria/', Puesta.as_view(), name="addAccionMigratoria")    
]
