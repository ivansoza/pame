from django.urls import path, include

from .views import homeComparecencia

urlpatterns = [
    path('', homeComparecencia, name="homeComparecencia"),

    
]
