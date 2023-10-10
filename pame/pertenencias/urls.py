from django.urls import path, include
from .views import CrearInventarioViewINM, ListaPertenenciasViewINM, CrearPertenenciasViewINM, ListaPertenenciasValorViewINM, CrearPertenenciasValoresViewINM, DeletePertenenciasINM, DeletePertenenciasIValorNM, EditarPertenenciasViewINM, UpdatePertenenciasValorINM, ListaEnseresViewINM, CrearEnseresINM, EditarEnseresViewINM, DeleteEnseresINM,CrearEnseresModaINM, CrearPertenenciasElectronicasViewINM,DeletePertenenciaselectronicasINM,EditarPertenenciaselectronicasViewINM, CrearvaloresefectivoViewINM, eliminarvaloresefectivoINM, editarvaloresefectivoINM,CrearvaloresjoyasViewINM, eliminarvaloresjoyasINM,editarvaloresjoyasINM,CrearvaloresdocumentosViewINM,eliminarvaloresdocumentosINM,editarvaloresdocumentosINM
from .views import CrearInventarioViewAC, ListaPertenenciasViewAC, CrearPertenenciasViewAC, ListaPertenenciasValorViewAC, CrearPertenenciasValoresViewAC, DeletePertenenciasAC, EditarPertenenciasViewAC, DeletePertenenciasValoresAC, UpdatePertenenciasValorAC, ListaEnseresViewAC,EditarEnseresViewAC, DeleteEnseresAC,CrearEnseresModaAC, CrearEnseresAC,CrearPertenenciasElectronicasViewAC,DeletePertenenciaselectronicasAC,EditarPertenenciaselectronicasViewAC,CrearvaloresefectivoViewAC,eliminarvaloresefectivoAC,editarvaloresefectivoAC,CrearvaloresjoyasViewAC,eliminarvaloresjoyasAC,editarvaloresjoyasAC,CrearvaloresdocumentosViewAC,eliminarvaloresdocumentosAC,editarvaloresdocumentosAC
from .views import CrearInventarioViewVP,ListaPertenenciasViewVP,CrearPertenenciasViewVP,DeletePertenenciasVP, EditarPertenenciasViewVP, ListaPertenenciasValorViewVP, CrearPertenenciasValoresViewVP, DeletePertenenciasValorVP, UpdatePertenenciasValorVP, ListaEnseresViewUP, CrearEnseresVP, CrearEnseresModalVP, DeleteEnseresVP, EditarEnseresViewVP
from .views import homePertenencias, manejar_imagen

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
    
    #pertenencias electronicas
    path('crear-pertenenciaselectronicas-inm/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasElectronicasViewINM.as_view(), name='crear_pertenenciaselectronicasINM'),
    path('eliminar-pertenenciaselectronicas-inm/<int:pk>/',DeletePertenenciaselectronicasINM.as_view(), name='eliminar_pertenenciaselectronicasINM'),
    path('editar_pertenenciaselectronicas-inm/<int:pk>/', EditarPertenenciaselectronicasViewINM.as_view(), name='editar_pertenenciaselectronicasINM'),

    #valores efectivo
    path('crearvaloresefectivo-inm/<int:inventario_id>/<int:puesta_id>/', CrearvaloresefectivoViewINM.as_view(), name='crear_pertenenciasefectivoINM'),
    path('eliminar-valoresefectivo-inm/<int:pk>/',eliminarvaloresefectivoINM.as_view(), name='eliminar_pertenenciasefectivoINM'),
    path('editar-valoresefectivo-inm/<int:pk>/', editarvaloresefectivoINM.as_view(), name='editar_pertenenciasefectivoINM'),

    
    #valores alhajas
    path('crear-valoresjoyas-inm/<int:inventario_id>/<int:puesta_id>/', CrearvaloresjoyasViewINM.as_view(), name='Crear_valoresjoyasViewINM'),
    path('eliminar-valoresjoyas-inm/<int:pk>/',eliminarvaloresjoyasINM.as_view(), name='eliminar_valoresjoyasINM'),
    path('editar_valoresjoyas-inm/<int:pk>/', editarvaloresjoyasINM.as_view(), name='editar_valoresjoyasINM'),


    # # documentos del extranjero
    path('crear-pertenenciasdocumentos-inm/<int:inventario_id>/<int:puesta_id>/', CrearvaloresdocumentosViewINM.as_view(), name='crear_pertenenciasdocumentosINM'),
    path('eliminar-pertenenciasdocumentos-inm/<int:pk>/',eliminarvaloresdocumentosINM.as_view(), name='eliminar_pertenenciasdocumentosINM'),
    path('editar_pertenenciasdocumentos-inm/<int:pk>/', editarvaloresdocumentosINM.as_view(), name='editar_valoresdocumentosINM'),

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

    path('listar-ensere-ac/<int:extranjero_id>/<int:puesta_id>/', ListaEnseresViewAC.as_view(), name='listarEnseresAC'),
    path('crear-enseres-ac/<int:extranjero_id>/<int:puesta_id>/', CrearEnseresAC.as_view(), name='crearEnseresAC'),
    path('editar-enseres-ac/<int:pk>/', EditarEnseresViewAC.as_view(), name='editarEnseresAC'),
    path('eliminar-enseres-ac/<int:pk>/', DeleteEnseresAC.as_view(), name='eliminarEnseresAC'),
    path('crear-enseres-ac1/<int:extranjero_id>/<int:puesta_id>/', CrearEnseresModaAC.as_view(), name='crearEnseresModaAC'),
    
        #pertenencias electronicas
    path('crear-pertenenciaselectronicas-ac/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasElectronicasViewAC.as_view(), name='crear_pertenenciaselectronicasAC'),
    path('eliminar-pertenenciaselectronicas-ac/<int:pk>/',DeletePertenenciaselectronicasAC.as_view(), name='eliminar_pertenenciaselectronicasAC'),
    path('editar_pertenenciaselectronicas-ac/<int:pk>/', EditarPertenenciaselectronicasViewAC.as_view(), name='editar_pertenenciaselectronicasAC'),

    #valores efectivo
    path('crearvaloresefectivo-ac/<int:inventario_id>/<int:puesta_id>/', CrearvaloresefectivoViewAC.as_view(), name='crear_pertenenciasefectivoAC'),
    path('eliminar-valoresefectivo-ac/<int:pk>/',eliminarvaloresefectivoAC.as_view(), name='eliminar_pertenenciasefectivoAC'),
    path('editar-valoresefectivo-ac/<int:pk>/', editarvaloresefectivoAC.as_view(), name='editar_pertenenciasefectivoAC'),

    
    #valores alhajas
    path('crear-valoresjoyas-ac/<int:inventario_id>/<int:puesta_id>/', CrearvaloresjoyasViewAC.as_view(), name='Crear_valoresjoyasViewAC'),
    path('eliminar-valoresjoyas-ac/<int:pk>/',eliminarvaloresjoyasAC.as_view(), name='eliminar_valoresjoyasAC'),
    path('editar_valoresjoyas-ac/<int:pk>/', editarvaloresjoyasAC.as_view(), name='editar_valoresjoyasAC'),


    # # documentos del extranjero
    path('crear-pertenenciasdocumentos-ac/<int:inventario_id>/<int:puesta_id>/', CrearvaloresdocumentosViewAC.as_view(), name='crear_pertenenciasdocumentosAC'),
    path('eliminar-pertenenciasdocumentos-ac/<int:pk>/',eliminarvaloresdocumentosAC.as_view(), name='eliminar_pertenenciasdocumentosAC'),
    path('editar_pertenenciasdocumentos-ac/<int:pk>/', editarvaloresdocumentosAC.as_view(), name='editar_valoresdocumentosAC'),


#-----------------------------VP---------------------------
    path('crear-inventario-vp/<int:extranjero_id>/<int:puesta_id>/', CrearInventarioViewVP.as_view(), name='crear_inventarioVP'),
    path('ver-pertenencias-vp/<int:inventario_id>/<int:puesta_id>/', ListaPertenenciasViewVP.as_view(), name='ver_pertenenciasVP'),
    path('crear-pertenencias-vp/<int:inventario_id>/<int:puesta_id>/', CrearPertenenciasViewVP.as_view(), name='crear_pertenenciasVP'),
    path('eliminar-pertenencias-vp/<int:pk>/', DeletePertenenciasVP.as_view(), name='eliminar_pertenenciasVP'),
    path('editar_pertenencias-vp/<int:pk>/', EditarPertenenciasViewVP.as_view(), name='editar_pertenenciasVP'),
    path('ver-pertenencias-valor-vp/<int:inventario_id>/<int:puesta_id>/',ListaPertenenciasValorViewVP.as_view(), name='ver_pertenencias_valor_vp'),
    path('crear-pertenencias-valor-vp/<int:inventario_id>/<int:puesta_id>/',CrearPertenenciasValoresViewVP.as_view(), name='crear_pertenencias_valor_vp'),
    path('eliminar-pertenencias-valor-vp/<int:pk>/',DeletePertenenciasValorVP.as_view(), name='eliminar_pertenencias_valor_vp'),
    path('editar-pertenencias-valor-vo/<int:pk>/',UpdatePertenenciasValorVP.as_view(), name='editar_pertenencias_valor_vp'),
    path('listar-ensere-vp/<int:extranjero_id>/<int:puesta_id>/', ListaEnseresViewUP.as_view(), name='listar_enseres_vp'),
    path('crear-enseres-vp/<int:extranjero_id>/<int:puesta_id>/', CrearEnseresVP.as_view(), name='crear_enseres_vp'),
    path('crear-enseres-vp1/<int:extranjero_id>/<int:puesta_id>/', CrearEnseresModalVP.as_view(), name='crearEnseresModalVP'),
    path('eliminar-enseres-vp/<int:pk>/', DeleteEnseresVP.as_view(), name='eliminarEnseresVP'),
    path('editar-enseres-vp/<int:pk>/', EditarEnseresViewVP.as_view(), name='editarEnseresVP'),


    path('manejar_imagen/', manejar_imagen, name='manejar_imagen'),


]
