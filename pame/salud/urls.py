from django.urls import path, include

from .views import homeMedicoGeneral, homeMedicoResponsable
from .views import listaExtranjerosEstacion, certificadoMedico, perfilMedicoInterno
from .views import listarExtranjerosServicioExterno, CargaCertificadoMedico
urlpatterns = [
    path("", homeMedicoGeneral, name="menusalud"),
    path('medico-general/', homeMedicoGeneral, name="homeMedicoGeneral"),
    path('medico-responsable/', homeMedicoResponsable, name="homeMedicoResponsable"),
    path('listExtranjeroEstacion/', listaExtranjerosEstacion.as_view(), name="listExtranjeroEstacion"),
    path('certificadoMedicoExtranjero/<int:pk>/', certificadoMedico.as_view(), name='certificadoMedicoExtranjero'),
    path('listExtranjeroExterno/', listarExtranjerosServicioExterno.as_view(), name="listExtranjeroExterno"),
    path('certificadoMedicoExterno/<int:pk>/', CargaCertificadoMedico.as_view(), name='certificadoMedicoExterno'),
    path('perfilMedico/', perfilMedicoInterno.as_view(), name="perfilMedico"),


]
