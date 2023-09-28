from django.urls import path

from .views import homeAcuerdoInicio

urlpatterns = [
    path("generar/", homeAcuerdoInicio, name="homeAcuerdoInicio"),
]
