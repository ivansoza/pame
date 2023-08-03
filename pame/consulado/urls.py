from django.urls import path, include

from .views import homeConsulado

urlpatterns = [
    path('', homeConsulado, name="homeConsulado"),

    
]
