from django.urls import path, include

from .views import homeLLamadasTelefonicas

urlpatterns = [
    path('', homeLLamadasTelefonicas, name="homeLLamadasTelefonicas"),

    
]
