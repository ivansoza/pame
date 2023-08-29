from django.urls import path, include

from .views import homeLLamadasTelefonicas, llamadasTelefonicas, ListLlamadas, crearLlamadas, ListLlamadasAC, crearLlamadasAC, crearLlamadas_AC

urlpatterns = [
    # path('', homeLLamadasTelefonicas, name="homeLLamadasTelefonicas"),
    # path('llamadas', llamadasTelefonicas.as_view(), name="llamadasTelefonicas"),
    # path('ver-llamadas-imn/<int:llamada_id>/', ListLlamadas.as_view(), name='ver_llamadasIMN'),
    # path('crear-llamada/<int:llamada_id>/', crearLlamadas.as_view(), name='crear_llamada'),
    path('ver-llamadas-ac/<int:llamada_id>/<int:puesta_id>/', ListLlamadasAC.as_view(), name='ver_llamadasAC'),
    path('crear-llamada-ac/<int:llamada_id>/<int:puesta_id>/', crearLlamadasAC.as_view(), name='crear_llamadaAC'),
    path('ver-llamadas-imn/<int:llamada_id>/<int:puesta_id>/', ListLlamadas.as_view(), name='ver_llamadasIMN'),
    path('crear-llamada/<int:llamada_id>/<int:puesta_id>/', crearLlamadas.as_view(), name='crear_llamada'),
    path('crear-llamada_ac/<int:llamada_id>/<int:puesta_id>/', crearLlamadas_AC.as_view(), name='crear_llamada_ac'),

]
