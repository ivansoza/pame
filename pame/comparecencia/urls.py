from django.urls import path, include
from .views import homeComparecencia, listExtranjerosComparecencia, CrearComparecencia

urlpatterns = [
    path('', homeComparecencia, name="homeComparecencia"),
    path("extranjeros/", listExtranjerosComparecencia.as_view(), name="lisExtranjerosComparecencia"),
    path('crear/<str:nup_id>/', CrearComparecencia.as_view(), name='crear_comparecencia'),

    
]
