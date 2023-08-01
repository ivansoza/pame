from django.urls import path, include

from .views import homePertenencias

urlpatterns = [
    path('', homePertenencias, name="homePertenencias"),

    
]
