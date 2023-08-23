from django.urls import path, include
from .views import CrearInventarioViewINM, ListaPertenenciasViewINM, CrearPertenenciasViewINM
from .views import CrearInventarioViewAC, ListaPertenenciasViewAC, CrearPertenenciasViewAC

from .views import homePertenencias

urlpatterns = [
    path('', homePertenencias, name="homePertenencias"),
#----------------------------INM-------------------------

    path('crear-inventario-inm/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioViewINM.as_view(), name='crear_inventarioINM'),
    path('ver-pertenencias-inm/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasViewINM.as_view(), name='ver_pertenenciasINM'),
    path('crear-pertenencias-inm/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasViewINM.as_view(), name='crear_pertenenciasINM'),
#----------------------------AC-------------------------
    path('crear-inventario-ac/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioViewAC.as_view(), name='crear_inventarioAC'),
    path('ver-pertenencias-ac/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasViewAC.as_view(), name='ver_pertenenciasAC'),
    path('crear-pertenencias-ac/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasViewAC.as_view(), name='crear_pertenenciasAC'),

]
