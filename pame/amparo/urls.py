from django.urls import path, include

from .views import homeAmparo

urlpatterns = [
    path('', homeAmparo, name="homeAmparo"),

    
]
