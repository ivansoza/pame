from django.urls import path, include

from .views import homeMedicoGeneral, homeMedicoResponsable

urlpatterns = [
    path("", homeMedicoGeneral, name="menusalud"),
    path('medico-general/', homeMedicoGeneral, name="homeMedicoGeneral"),
    path('medico-responsable/', homeMedicoResponsable, name="homeMedicoResponsable"),
]
