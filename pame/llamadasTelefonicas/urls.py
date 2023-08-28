from django.urls import path, include

from .views import homeLLamadasTelefonicas, llamadasTelefonicas, ListLlamadas, crearLlamadas

urlpatterns = [
    # path('', homeLLamadasTelefonicas, name="homeLLamadasTelefonicas"),
    # path('llamadas', llamadasTelefonicas.as_view(), name="llamadasTelefonicas"),
    path('ver-llamadas-imn/<int:llamada_id>/', ListLlamadas.as_view(), name='ver_llamadasIMN'),
    path('crear-llamada/<int:llamada_id>/', crearLlamadas.as_view(), name='crear_llamada'),
]
