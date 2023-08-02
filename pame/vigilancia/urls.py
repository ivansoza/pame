from django.urls import path, include

from .views import homeSeguridadGeneral, addAutoridadCompetente, addAccionMigratoria, addHospedaje,addTraslado

urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),
    path('autoridad-competente/',addAutoridadCompetente, name="addAutoridadCompetente"),
    path('accion-migratoria/',addAccionMigratoria, name="addAccionMigratoria"),
    path('hospedaje/',addHospedaje, name="addHospedaje"),
    path('traslado/',addTraslado, name="addTraslado"),



    
]
