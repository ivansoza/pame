from django.urls import path, include

from .views import inicioINMList, createPuestaINM, createExtranjeroINM, listarExtranjeros, EditarExtranjeroINM, DeleteExtranjeroINM,AgregarBiometricoINM, EditarBiometricoINM,acompananteList, createExtranjeroAcomINM,AgregarAcompananteViewINM, DeleteAcompananteINM, DeleteAcompananteINM1, EditarExtranjeroINMProceso, ResumenViewINM
from .views import inicioACList, createPuestaAC, createExtranjeroAC, listarExtranjerosAC,EditarExtranjeroAC,DeleteExtranjeroAC, AgregarBiometricoAC, EditarBiometricoAC, createAcompananteAC, ListAcompanantesAC, AgregarAcompananteViewAC, DeleteAcompananteAC ,DeleteAcompananteAC1, EditarExtranjeroACProceso
from .views import homeSeguridadGeneral, addAutoridadCompetente, addHospedaje,addTraslado,homeSeguridadResponsable,homePuestaINM, homePuestaVP, createAcompananteAC, AgregarAcompananteViewVP,DeleteAcompananteVP,DeleteAcompananteVP1, EditarExtranjeroVPProceso
from .views import CalcularTamanoDiscoView, listarTraslado, AgregarRelacionGeneral, DeleteAcompananteGeneral
from .views import inicioVPList, createPuestaVP, listarExtranjerosVP, createExtranjeroVP, AgregarBiometricoVP, listarAcompanantesVP, EditarExtranjeroVP, DeleteExtranjeroVP,EditarBiometricoVP,createAcompananteVP, manejar_imagen, manejar_imagen2, manejar_imagen3
from .views import estadisticasPuestaINM, solicitar_traslado, TrasladoCreateView, procesar_traslado, listarAcompanantesEstacion, acompananteListGeneral
from .views import listarExtranjerosEstacion,sesionfinal,firma, ejemplo, qrs, verificar_firma, FirmaCreateView, firmE, firmExistente, AgregarBiometricoGeneral, EditarBiometricoGeneral, EditarExtranjeroGeneral, DeleteExtranjeroGeneral

from .views import compare_faces, UserFaceCreateView, search_face, guardar_firma
urlpatterns = [
    path('', homeSeguridadGeneral, name="homeSeguridadGeneral"),

    path('prueba', ejemplo, name="ejemplo"),

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
    path('crearAcompananteINM/<int:puesta_id>/<int:extranjero_principal_id>/', createExtranjeroAcomINM.as_view(), name='crearAcompananteINM'),
    path('agregar_acompananteINM/<int:extranjero_principal_id>/<int:extranjero_id>/', AgregarAcompananteViewINM.as_view(), name='agregar_acompananteINM'),
    path('DeleteAcompananteINM1/<int:pk>/', DeleteAcompananteINM1.as_view(), name='delete_acompananteINM1'),
    path('csalcular/<int:pk>/', CalcularTamanoDiscoView.as_view(), name='calcular'),
    path('editarExtranjeroINMproceso/<int:pk>/<int:puesta_id>/', EditarExtranjeroINMProceso.as_view(), name='editarExtranjeroINMproceso'),
    path('resumenINM/<int:pk>/', ResumenViewINM.as_view(), name='resumenINM'),
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
    path('editarExtranjeroACproceso/<int:pk>/<int:puesta_id>/', EditarExtranjeroACProceso.as_view(), name='editarExtranjeroACproceso'),


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
    path('editarExtranjeroVPproceso/<int:pk>/<int:puesta_id>/', EditarExtranjeroVPProceso.as_view(), name='editarExtranjeroVPproceso'),

#-----------------------------TRASLADOS---------------------
    path('traslado/<int:traslado_id>/<int:destino_id>/', listarTraslado.as_view(), name='traslado'),
    path('seguridad/solicitar_traslado/<int:traslado_id>/', solicitar_traslado, name='solicitar_traslado'),
    path('crear_traslado/<int:origen_id>/<int:destino_id>/', TrasladoCreateView.as_view(), name='crear_traslado'),
    path('procesar/traslado/', procesar_traslado, name='procesar_traslado'),
    
    

    path('manejar_imagen/', manejar_imagen, name='manejar_imagen'),
    path('manejar_imagen2/', manejar_imagen2, name='manejar_imagen2'),
    path('manejar_imagen3/', manejar_imagen3, name='manejar_imagen3'),
    path('qr/<int:extranjero_id>/', qrs.as_view(), name='qr'),


# Listar extranjeros de forma global por estacion 


    path('listar-extranjero-dd/', listarExtranjerosEstacion.as_view(), name='listarExtranjerosEstacion'),
    
    
    path('sesionfinal/', sesionfinal, name='sesionfinal'),
    
    
    path('firma/<int:extranjero_id>/', firma.as_view(), name='firma'),
    path('guardar_firma/<int:extranjero_id>/', guardar_firma, name='guardar_firma'),
    path('verificar_firma/<int:extranjero_id>/', verificar_firma, name='verificar_firma'),

        # firma
    path('crear_firma/<int:extranjero_id>/', FirmaCreateView.as_view(), name='crear_firma'),
    path('firma_exitosa/', firmE.as_view(), name='firma_exitosa'),
    path('firma_existente/', firmExistente.as_view(), name='firma_existente'),
    path('agregarBiometricosGenrales/<int:extranjero_id>/', AgregarBiometricoGeneral.as_view(), name='agregarBiometricosGenrales'),
    path('editarBiometricoGeneral/<int:pk>/', EditarBiometricoGeneral.as_view(), name='editarBiometricoGeneral'),
    path('editarExtranjeroGeneral/<int:pk>/', EditarExtranjeroGeneral.as_view(), name='editarExtranjeroGeneral'),
    path('eliminarExtranjeroGeneral/<int:pk>/', DeleteExtranjeroGeneral.as_view(), name='eliminarExtranjeroGeneral'),
    path('listar-acompanante-dd/', listarAcompanantesEstacion.as_view(), name='listarAcompanantesEstacion'),
    path('listAcompanantesss/<int:extranjero_id>/', acompananteListGeneral.as_view(),name='listAcompanantesss'),
    path('agregar_acompanantegeneral/<int:extranjero_principal_id>/<int:extranjero_id>/', AgregarRelacionGeneral.as_view(), name='agregar_acompanantegeneral'),
    path('DeleteAcompanantegenerales/<int:pk>/', DeleteAcompananteGeneral.as_view(), name='DeleteAcompanantegenerales'),

]

