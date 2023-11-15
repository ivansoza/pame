from django.urls import path, include

from .views import homeMedicoGeneral, homeMedicoResponsable, manejar_imagen
from .views import listaExtranjerosEstacion, certificadoMedico, perfilMedicoInterno, datosDelMedico, listaConsultasExtranjero, certificadoEgreso, documentosReferencia, verificar_firma
from .views import listarExtranjerosServicioExterno, CargaCertificadoMedico, consultaMedica, listaExtranjerosConsulta, constanciaLesiones, referencia, listaDocumentos, QrsMedico, FirmaCreateMedicoView
urlpatterns = [
    path("", homeMedicoGeneral, name="menusalud"),
    path('medico-general/', homeMedicoGeneral, name="homeMedicoGeneral"),
    path('medico-responsable/', homeMedicoResponsable, name="homeMedicoResponsable"),
    path('listExtranjeroEstacion/', listaExtranjerosEstacion.as_view(), name="listExtranjeroEstacion"),
    path('certificadoMedicoExtranjero/<int:pk>/', certificadoMedico.as_view(), name='certificadoMedicoExtranjero'),
    path('listExtranjeroExterno/', listarExtranjerosServicioExterno.as_view(), name="listExtranjeroExterno"),
    path('certificadoMedicoExterno/<int:pk>/', CargaCertificadoMedico.as_view(), name='certificadoMedicoExterno'),
    path('perfilMedico/', perfilMedicoInterno.as_view(), name="perfilMedico"),
    path('datosMedico/', datosDelMedico.as_view(), name="datosMedico"),
    path("manejar_imagen", manejar_imagen, name="manejar_imagen"),
    path('consulta/<int:pk>/', consultaMedica.as_view(), name='consulta'),
    path('listExtranjeroConsulta/', listaExtranjerosConsulta.as_view(), name="listExtranjeroConsulta"),
    path('listConsultas/<int:pk>/', listaConsultasExtranjero.as_view(), name='listConsultas'),
    path('constanciaLesiones/<int:pk>/', constanciaLesiones.as_view(), name='constanciaLesiones'),
    path('certificadoMedicoEgreso/<int:pk>/', certificadoEgreso.as_view(), name='certificadoMedicoEgreso'),
    path('referenciaMedica/<int:pk>/', referencia.as_view(), name='referenciaMedica'),
    path('documentosReferencia/<int:referencia_id>/', documentosReferencia.as_view(), name='documentosReferencia'),
    path('documentos/<int:consulta_id>/', listaDocumentos.as_view(), name='lista_documentos'),
    path('qrMedico/<int:pk>/', QrsMedico.as_view(), name='qrMedico'),
    path('verificar_firma1/<int:pk>/', verificar_firma, name='verificar_firma1'),
    path('crear_firma_Medico/<int:pk>/', FirmaCreateMedicoView.as_view(), name='crear_firma_Medico'),

]
