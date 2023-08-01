from django.urls import path, include

from .views import homeAcuerdoInicio

urlpatterns = [
    path("", homeAcuerdoInicio, name="homeAcuerdoInicio"),
    
]
