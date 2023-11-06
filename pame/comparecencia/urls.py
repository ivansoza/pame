from django.urls import path, include
from .views import homeComparecencia, listExtranjerosComparecencia

urlpatterns = [
    path('', homeComparecencia, name="homeComparecencia"),
    path("extranjeros/", listExtranjerosComparecencia.as_view(), name="lisExtranjerosComparecencia"),

    
]
