from django.urls import path, include
<<<<<<< HEAD
#from .views import Puesta, PuestaAutoridadCompetente
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable, homePuestaAC,homePuestaINM, homePuestaVP
=======
from .views import Puesta, PuestaAutoridadCompetente, OficioAC
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable
>>>>>>> origin/jose

urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),
    path('seguridad-responsable/', homeSeguridadResponsable, name='homeSeguridadResponsable'),
    #path('autoridad-competente/',PuestaAutoridadCompetente.as_view(), name="addAutoridadCompetente"),
    #path('accion-migratoria/',puesta, name="addAccionMigratoria"),
    path('hospedaje/',addHospedaje, name="addHospedaje"),
    path('traslado/',addTraslado, name="addTraslado"),
<<<<<<< HEAD
    path('seguridad/puesta-ac/', homePuestaAC, name='homePuestaAC'),
    path('seguridad/puesta-inm/', homePuestaINM, name='homePuestaINM'),
    path('seguridad/puesta-vp/', homePuestaVP, name='homePuestaVP'),

    
    
    #path('accion-migratoria/', Puesta.as_view(), name="addAccionMigratoria")

=======
    path('accion-migratoria/', Puesta.as_view(), name="addAccionMigratoria"),
    path('crear/', OficioAC.as_view(), name="crear"),
>>>>>>> origin/jose


    
]
