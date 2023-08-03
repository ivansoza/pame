from django.urls import path, include

from .views import homeActuaciones

urlpatterns = [
    path("", homeActuaciones, name="homeActuaciones"),
    
    
]
