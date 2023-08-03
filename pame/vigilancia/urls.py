from django.urls import path, include
from .views import Puesta
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable

urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),
    path('seguridad-responsable/', homeSeguridadResponsable, name='homeSeguridadResponsable'),
    path('autoridad-competente/',addAutoridadCompetente, name="addAutoridadCompetente"),
    #path('accion-migratoria/',puesta, name="addAccionMigratoria"),
    path('hospedaje/',addHospedaje, name="addHospedaje"),
    path('traslado/',addTraslado, name="addTraslado"),
    path('accion-migratoria/', Puesta.as_view(), name="addAccionMigratoria")



    
]
