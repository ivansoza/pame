from django.urls import path, include
from .views import CrearInventarioViewINM, ListaPertenenciasViewINM, CrearPertenenciasViewINM, ListaPertenenciasValorViewINM, CrearPertenenciasValoresViewINM, DeletePertenenciasINM, DeletePertenenciasIValorNM, EditarPertenenciasViewINM, UpdatePertenenciasValorINM, ListaEnseresViewINM, CrearEnseresINM, EditarEnseresViewINM, DeleteEnseresINM,CrearEnseresModaINM
from .views import CrearInventarioViewAC, ListaPertenenciasViewAC, CrearPertenenciasViewAC, ListaPertenenciasValorViewAC, CrearPertenenciasValoresViewAC, DeletePertenenciasAC, EditarPertenenciasViewAC, DeletePertenenciasValoresAC, UpdatePertenenciasValorAC

from .views import homePertenencias

urlpatterns = [
    path('', homePertenencias, name="homePertenencias"),
#----------------------------INM-------------------------

    path('crear-inventario-inm/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioViewINM.as_view(), name='crear_inventarioINM'),
    path('ver-pertenencias-inm/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasViewINM.as_view(), name='ver_pertenenciasINM'),
    path('crear-pertenencias-inm/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasViewINM.as_view(), name='crear_pertenenciasINM'),
    path('ver-pertenencias-valor-inm/<int:inventario_id>/<int:puesta_id>/',ListaPertenenciasValorViewINM.as_view(), name='ver_pertenencias_valorINM'),
    path('crear-pertenencias-valor-inm/<int:inventario_id>/<int:puesta_id>/',CrearPertenenciasValoresViewINM.as_view(), name='crear_pertenencias_valorINM'),
    path('eliminar-pertenencias-inm/<int:pk>/',DeletePertenenciasINM.as_view(), name='eliminar_pertenenciasINM'),
    path('eliminar-pertenencias-valor-inm/<int:pk>/',DeletePertenenciasIValorNM.as_view(), name='eliminar_pertenencias_valorINM'),
    path('editar_pertenencias-inm/<int:pk>/', EditarPertenenciasViewINM.as_view(), name='editar_pertenenciasINM'),
    path('editar-pertenencias-valor-inm/<int:pk>/',UpdatePertenenciasValorINM.as_view(), name='editar_pertenencias_valorINM'),
    path('listar-ensere-inm/<int:extranjero_id>/<int:puesta_id>/', ListaEnseresViewINM.as_view(), name='listarEnseresINM'),
    path('crear-enseres-inm/<int:extranjero_id>/<int:puesta_id>/', CrearEnseresINM.as_view(), name='crearEnseresINM'),
    path('editar-enseres-inm/<int:pk>/', EditarEnseresViewINM.as_view(), name='editarEnseresINM'),
    path('eliminar-enseres-inm/<int:pk>/', DeleteEnseresINM.as_view(), name='eliminarEnseresINM'),
    path('crear-enseres-inm1/<int:extranjero_id>/<int:puesta_id>/', CrearEnseresModaINM.as_view(), name='crearEnseresModaINM'),


#----------------------------AC-------------------------
    path('crear-inventario-ac/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioViewAC.as_view(), name='crear_inventarioAC'),
    path('ver-pertenencias-ac/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasViewAC.as_view(), name='ver_pertenenciasAC'),
    path('crear-pertenencias-ac/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasViewAC.as_view(), name='crear_pertenenciasAC'),
    path('ver-pertenencias-valor-ac/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasValorViewAC.as_view(), name='ver_pertenencias_valorAC'),
    path('crear-pertenencias-valor-ac/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasValoresViewAC.as_view(), name='crear_pertenencias_valorAC'),
    path('eliminar-pertenencias-ac/<int:pk>/', DeletePertenenciasAC.as_view(), name='eliminar_pertenenciasAC'),
    path('eliminar-pertenencias-valor-ac/<int:pk>/',DeletePertenenciasValoresAC.as_view(), name="eliminar_pertenencias_valorAC"),
    path('editar_pertenencias-ac/<int:pk>/', EditarPertenenciasViewAC.as_view(), name='editar_pertenenciasAC'),
    path('editar-pertenencias-valor-ac/<int:pk>/',UpdatePertenenciasValorAC.as_view(), name="editar_pertenencias_valorAC"),

]
