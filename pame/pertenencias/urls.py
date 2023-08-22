from django.urls import path, include
from .views import listPertenenciasINM, crearFolioInventarioINM, crearPertenenciaINM, CrearInventarioView, ListaPertenenciasView, CrearPertenenciasView
from .views import homePertenencias

urlpatterns = [
    path('', homePertenencias, name="homePertenencias"),
    path('list-pertenenciasINM/<int:extranjero_id>/<int:puesta_id>/', listPertenenciasINM.as_view(), name="listPertenenciasINM"),
    path('crear-folioInvenatrioINM/<int:extranjero_id>/', crearFolioInventarioINM.as_view(), name="crearInventarioINM"),
    path('crear-pertenenciaINM/<int:extranjero_id>/', crearPertenenciaINM.as_view(), name="crearPertenenciaINM"),


    path('crear-inventario/<int:extranjero_id>/', CrearInventarioView.as_view(), name='crear_inventarioINM'),
    path('ver-pertenencias/<int:inventario_id>/', ListaPertenenciasView.as_view(), name='ver_pertenenciasINM'),
    path('crear-pertenencias/<int:inventario_id>/', CrearPertenenciasView.as_view(), name='crear_pertenenciasINM'),

]
