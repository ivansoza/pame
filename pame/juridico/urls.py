from django.urls import path, include

from .views import homeJuridicoGeneral, homeJuridicoResponsable, homeJuridico

urlpatterns = [
    path("", homeJuridico, name="homeJuridico"),
    path('juridico-general', homeJuridicoGeneral, name="homeJuridicoGeneral"),
     path('juridico-responsable', homeJuridicoResponsable, name="homeJuridicoResponsable"),
    
]
