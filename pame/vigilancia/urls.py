from django.urls import path, include

from .views import inicioINMList, createPuestaINM, createExtranjeroINM, inicioACList, createPuestaAC, createExtranjeroAC, DeleteExtranjeroINM
from .views import inicioINMList, createPuestaINM, createExtranjeroINM, listarExtranjeros, listarExtranjerosAC, EditarExtranjeroINM, EditarExtranjeroAC
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
   #Puesta AC
    path('puesta-ac/', inicioACList.as_view(), name='homePuestaAC'),
    path('crear-puesta-ac/', createPuestaAC.as_view(), name='crearPuestaAC'),
    path('crear-extranjero-ac/<int:puesta_id>/', createExtranjeroAC.as_view(), name='createExtranjeroAC'),


    
    path('seguridad/listar-extranjero/<int:puesta_id>/', listarExtranjeros.as_view(), name='listarExtranjeros'),
    path('seguridad/listar-extranjeroAC/<int:puesta_id>/', listarExtranjerosAC.as_view(), name='listarExtranjerosAC'),
    path('editarExtranjeroAC/<int:pk>/', EditarExtranjeroAC.as_view(), name='editarExtranjeroAC'),
     path('editarExtranjeroINM/<int:pk>/', EditarExtranjeroINM.as_view(), name='editarExtranjeroINM'),
    path('eliminar-extranjero/<int:pk>/', DeleteExtranjeroINM.as_view(), name='eliminarExtranjeroINM'),
    path('seguridad/listar-extranjero/<int:puesta_id>', listarExtranjeros.as_view(), name='listarExtranjeros'),
    path('seguridad/listar-extranjeroAC/<str:puesta_id>/', listarExtranjerosAC.as_view(), name='listarExtranjerosAC'),
    path('editarExtranjeroINM/<int:puesta_id>/<int:pk>/', EditarExtranjeroINM.as_view(), name='editarExtranjeroINM'),
    
    #path('accion-migratoria/', Puesta.as_view(), name="addAccionMigratoria")    
]
