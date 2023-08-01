from django.urls import path, include

from .views import homeConsultaMedica

urlpatterns = [
    path('homeConsultaMedica/', homeConsultaMedica, name="homeConsultaMedica"),

    
]
