from django.urls import path, include

from .views import homeComedor

urlpatterns = [
    path('homeComedor/', homeComedor, name="homeComedor"),

    
]
