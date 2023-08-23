from django.urls import path, include
from .views import listPertenenciasINM, crearFolioInventarioINM, crearPertenenciaINM, CrearInventarioView, ListaPertenenciasView, CrearPertenenciasView
from .views import CrearInventarioViewAC, ListaPertenenciasViewAC, CrearPertenenciasViewAC

from .views import homePertenencias

urlpatterns = [
    path('', homePertenencias, name="homePertenencias"),
    path('list-pertenenciasINM/<int:extranjero_id>/<int:puesta_id>/', listPertenenciasINM.as_view(), name="listPertenenciasINM"),
    path('crear-folioInvenatrioINM/<int:extranjero_id>/', crearFolioInventarioINM.as_view(), name="crearInventarioINM"),
    path('crear-pertenenciaINM/<int:extranjero_id>/', crearPertenenciaINM.as_view(), name="crearPertenenciaINM"),


    path('crear-inventario-inm/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioView.as_view(), name='crear_inventarioINM'),
    path('ver-pertenencias-inm/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasView.as_view(), name='ver_pertenenciasINM'),
    path('crear-pertenencias-inm/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasView.as_view(), name='crear_pertenenciasINM'),


#----------------------------AC-------------------------
    path('crear-inventario-ac/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioViewAC.as_view(), name='crear_inventarioAC'),
    path('ver-pertenencias-ac/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasViewAC.as_view(), name='ver_pertenenciasAC'),
    path('crear-pertenencias-ac/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasViewAC.as_view(), name='crear_pertenenciasAC'),

]
