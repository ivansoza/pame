from django.urls import path, include

from .views import inicioINMList, createPuestaINM, createExtranjeroINM, listarExtranjeros, EditarExtranjeroINM, DeleteExtranjeroINM,AgregarBiometricoINM, EditarBiometricoINM
from .views import inicioACList, createPuestaAC, createExtranjeroAC, listarExtranjerosAC,EditarExtranjeroAC,DeleteExtranjeroAC, AgregarBiometricoAC, EditarBiometricoAC
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable,homePuestaINM, homePuestaVP

urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),
    path('seguridad-responsable/', homeSeguridadResponsable, name='homeSeguridadResponsable'),
    path('hospedaje/',addHospedaje, name="addHospedaje"),
    path('traslado/',addTraslado, name="addTraslado"),
  
    # --------------- PUESTA INM  ---------------------
    path('puesta-inm/', inicioINMList.as_view(), name='homePuestaINM'),
    path('crear-puesta-inm/', createPuestaINM.as_view(), name='crearPuestaINM'),
    path('crear-extranjero-inm/<int:puesta_id>/', createExtranjeroINM.as_view(), name='crearExtranjeroINM'),
    path('listar-extranjero/<int:puesta_id>', listarExtranjeros.as_view(), name='listarExtranjeros'),
    path('editarExtranjeroINM/<int:pk>/', EditarExtranjeroINM.as_view(), name='editarExtranjeroINM'),
    path('eliminar-extranjero/<int:pk>/', DeleteExtranjeroINM.as_view(), name='eliminarExtranjeroINM'),
    path('agregar_biometricoINM/<int:extranjero_id>/', AgregarBiometricoINM.as_view(), name='agregar_biometricoINM'),
    path('editar_biometricoINM/<int:pk>/', EditarBiometricoINM.as_view(), name='editar_biometricoINM'),


    # --------------- PUESTA AC  ---------------------
    path('puesta-ac/', inicioACList.as_view(), name='homePuestaAC'),
    path('crear-puesta-ac/', createPuestaAC.as_view(), name='crearPuestaAC'),
    path('crear-extranjero-ac/<int:puesta_id>/', createExtranjeroAC.as_view(), name='crearExtranjeroAC'),
    path('listar-extranjero-ac/<int:puesta_id>', listarExtranjerosAC.as_view(), name='listarExtranjeroAC'),
    path('editarExtranjeroAC/<int:pk>/', EditarExtranjeroAC.as_view(), name='editarExtranjeroAC'),
    path('eliminar_extranjero-ac/<int:pk>/', DeleteExtranjeroAC.as_view(), name='eliminar_extranjeroAC'),
    path('agregar_biometricoAC/<int:extranjero_id>/', AgregarBiometricoAC.as_view(), name='agregar_biometricoAC'),
    path('editar_biometricoAC/<int:pk>/', EditarBiometricoAC.as_view(), name='editar_biometricoAC'),


# ------------------------- PUESTA VOLUNTAD PROPIA ----------------
    path('seguridad/puesta-vp/', homePuestaVP, name='homePuestaVP'),
   #Puesta AC

]

