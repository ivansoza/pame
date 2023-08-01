from django.urls import path, include

from .views import homeCertificadoMedico

urlpatterns = [
    path('', homeCertificadoMedico, name="homeCertificadoMedico"),

    
]
