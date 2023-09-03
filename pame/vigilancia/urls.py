from django.urls import path, include

from .views import inicioINMList, createPuestaINM, createExtranjeroINM, listarExtranjeros, EditarExtranjeroINM, DeleteExtranjeroINM,AgregarBiometricoINM, EditarBiometricoINM,acompananteList, createExtranjeroAcomINM,AgregarAcompananteViewINM, DeleteAcompananteINM, DeleteAcompananteINM1
from .views import inicioACList, createPuestaAC, createExtranjeroAC, listarExtranjerosAC,EditarExtranjeroAC,DeleteExtranjeroAC, AgregarBiometricoAC, EditarBiometricoAC, createAcompananteAC, ListAcompanantesAC, AgregarAcompananteViewAC, DeleteAcompananteAC ,DeleteAcompananteAC1
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable,homePuestaINM, homePuestaVP, createAcompananteAC, AgregarAcompananteViewVP,DeleteAcompananteVP,DeleteAcompananteVP1
from .views import CalcularTamanoDiscoView
from .views import inicioVPList, createPuestaVP, listarExtranjerosVP, createExtranjeroVP, AgregarBiometricoVP, listarAcompanantesVP, EditarExtranjeroVP, DeleteExtranjeroVP,EditarBiometricoVP,createAcompananteVP
from .views import estadisticasPuestaINM
urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),
    path('seguridad-responsable/', homeSeguridadResponsable, name='homeSeguridadResponsable'),
    path('hospedaje/',addHospedaje, name="addHospedaje"),
    path('traslado/',addTraslado, name="addTraslado"),
    
  
    # --------------- PUESTA INM  ---------------------
    path('puesta-inm/', inicioINMList.as_view(), name='homePuestaINM'),
    path('estadisticas-inm/', estadisticasPuestaINM.as_view(), name='estadisticaINM'),

    path('crear-puesta-inm/', createPuestaINM.as_view(), name='crearPuestaINM'),
    path('crear-extranjero-inm/<int:puesta_id>/', createExtranjeroINM.as_view(), name='crearExtranjeroINM'),
    path('listar-extranjero/<int:puesta_id>', listarExtranjeros.as_view(), name='listarExtranjeros'),
    path('editarExtranjeroINM/<int:pk>/', EditarExtranjeroINM.as_view(), name='editarExtranjeroINM'),
    path('eliminar-extranjero/<int:pk>/', DeleteExtranjeroINM.as_view(), name='eliminarExtranjeroINM'),
    path('agregar_biometricoINM/<int:extranjero_id>/', AgregarBiometricoINM.as_view(), name='agregar_biometricoINM'),
    path('editar_biometricoINM/<int:pk>/', EditarBiometricoINM.as_view(), name='editar_biometricoINM'),
    path('listAcompanantesINM/<int:extranjero_id>/<int:puesta_id>/', acompananteList.as_view(),name='listAcompanantesINM'),
    path('crearAcompananteINM/<int:puesta_id>/<int:extranjero_principal_id>/', createExtranjeroAcomINM.as_view(), name='crearAcompananteINM'),
    path('agregar_acompananteINM/<int:extranjero_principal_id>/<int:extranjero_id>/', AgregarAcompananteViewINM.as_view(), name='agregar_acompananteINM'),
    path('DeleteAcompananteINM/<int:pk>/', DeleteAcompananteINM.as_view(), name='delete_acompananteINM'),
    path('DeleteAcompananteINM1/<int:pk>/', DeleteAcompananteINM1.as_view(), name='delete_acompananteINM1'),
    path('csalcular/<int:pk>/', CalcularTamanoDiscoView.as_view(), name='calcular'),







    # --------------- PUESTA AC  ---------------------
    path('puesta-ac/', inicioACList.as_view(), name='homePuestaAC'),
    path('crear-puesta-ac/', createPuestaAC.as_view(), name='crearPuestaAC'),
    path('crear-extranjero-ac/<int:puesta_id>/', createExtranjeroAC.as_view(), name='crearExtranjeroAC'),
    path('listar-extranjero-ac/<int:puesta_id>', listarExtranjerosAC.as_view(), name='listarExtranjeroAC'),
    path('editarExtranjeroAC/<int:pk>/', EditarExtranjeroAC.as_view(), name='editarExtranjeroAC'),
    path('eliminar_extranjero-ac/<int:pk>/', DeleteExtranjeroAC.as_view(), name='eliminar_extranjeroAC'),
    path('agregar_biometricoAC/<int:extranjero_id>/', AgregarBiometricoAC.as_view(), name='agregar_biometricoAC'),
    path('editar_biometricoAC/<int:pk>/', EditarBiometricoAC.as_view(), name='editar_biometricoAC'),
    # path('create-acompanantesAC/', createAcompananteAC.as_view(),name='createAcompananteAC'),
    path('list-acompanantes-ac/<int:extranjero_id>/<int:puesta_id>/', ListAcompanantesAC.as_view(), name='listAcompanantesAC'),
    path('agregar_acompanante-ac/<int:extranjero_principal_id>/<int:extranjero_id>/', AgregarAcompananteViewAC.as_view(), name='agregar_acompananteAC'),

    path('crear-acompanante-ac/<int:puesta_id>/<int:extranjero_principal_id>/', createAcompananteAC.as_view(), name='crearAcompananteAC'),
    path('DeleteAcompananteAC/<int:pk>/', DeleteAcompananteAC.as_view(), name='delete_acompananteAC'),
    path('DeleteAcompananteAC1/<int:pk>/', DeleteAcompananteAC1.as_view(), name='delete_acompananteAC1'),
    # path('agregar-relacion-ac/<int:extranjero_principal_id>/', CrearRelacionAcompananteAC.as_view(), name='agregar_relacion_ac'),
    # path('crear-relacion/<int:extranjero_id>/<int:relacion_id>/', CrearRelacionView.as_view(), name='crear_relacion'),


# ------------------------- PUESTA VOLUNTAD PROPIA ----------------


    path('seguridad/puesta-vp/', homePuestaVP, name='homePuestaVP'),
    path('puesta-vp/', inicioVPList.as_view(), name='homePuestasVP'),
    path('crear-puesta-vp/', createPuestaVP.as_view(), name='crearPuestaVP'),
    path('crear-extranjero-vp/<int:puesta_id>/', createExtranjeroVP.as_view(), name='crearExtranjeroVP'),
    path('listar-extranjero-vp/<int:puesta_id>', listarExtranjerosVP.as_view(), name='listarExtranjerosVP'),
    path('editar-extranjero-vp/<int:pk>/', EditarExtranjeroVP.as_view(), name='editar-extranjero-vp'),
    path('eliminar-extranjero-vp/<int:pk>/', DeleteExtranjeroVP.as_view(), name='eliminar-extranjero-vp'),
    path('agregar-biometrico-vp/<int:extranjero_id>/', AgregarBiometricoVP.as_view(), name='agregar_biometricoVP'),
    path('listar-acompanantes-vp/<int:extranjero_id>/<int:puesta_id>/', listarAcompanantesVP.as_view(),name='listAcompanantesVP'),
    path('editar_biometrico-vp/<int:pk>/', EditarBiometricoVP.as_view(), name='editar_biometricoVP'),
    path('crear-acompanante-vp/<int:puesta_id>/<int:extranjero_principal_id>/', createAcompananteVP.as_view(), name='createAcompananteVP'),
    path('agregar_acompanante-VP/<int:extranjero_principal_id>/<int:extranjero_id>/', AgregarAcompananteViewVP.as_view(), name='agregar_acompananteVP'),
    path('DeleteAcompanante-vp/<int:pk>/', DeleteAcompananteVP.as_view(), name='delete_acompananteVP'),
    path('DeleteAcompanante-vp1/<int:pk>/', DeleteAcompananteVP1.as_view(), name='delete_acompananteVP1'),


]

