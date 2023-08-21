from django.urls import path, include
from .views import listPertenenciasINM, crearFolioInventarioINM
from .views import homePertenencias

urlpatterns = [
    path('', homePertenencias, name="homePertenencias"),
    path('list-pertenenciasINM/<int:extranjero_id>/<int:puesta_id>/', listPertenenciasINM.as_view(), name="listPertenenciasINM"),
    path('crear-folioInvenatrioINM/<int:extranjero_id>/', crearFolioInventarioINM.as_view(), name="crearInventarioINM"),
]
