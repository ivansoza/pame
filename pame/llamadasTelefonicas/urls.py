from django.urls import path, include

from .views import homeLLamadasTelefonicas, llamadasTelefonicas, ListLlamadas, crearLlamadas, ListLlamadasAC, crearLlamadasAC, crearLlamadas_AC, notificacionLlamadaINM, notificacionLlamadaAC, notificacionLlamadaVP, ListLlamadasVP, crearLlamadasVP
from .views import validarNotificacion, validarNotificacionAC, validarNotificacionVP, manejar_imagen
from .views import ListLlamadasGenerales, notificacionLlamadaGenerales, validarNotificacionGenerales, crearLlamadasGenerales
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
    path('notificar-llamada-inm/<int:llamada_id>/<int:puesta_id>/', notificacionLlamadaINM.as_view(), name='notificar-llamada-inm'),    
    path('notificar-llamada-ac/<int:llamada_id>/<int:puesta_id>/', notificacionLlamadaAC.as_view(), name='notificar-llamada-ac'),
    path('notificar-llamada-vp/<int:llamada_id>/<int:puesta_id>/', notificacionLlamadaVP.as_view(), name='notificar-llamada-vp'),
    path('ver-llamadas-vp/<int:llamada_id>/<int:puesta_id>/', ListLlamadasVP.as_view(), name='ver_llamadas_vp'),
    path('crear-llamada_vp/<int:llamada_id>/<int:puesta_id>/', crearLlamadasVP.as_view(), name='crear_llamada_vp'),
    path('validar-notificacion/<int:llamada_id>/<int:puesta_id>/', validarNotificacion.as_view(), name='validar_notificacion'),
    path('validar-notificacion-AC/<int:llamada_id>/<int:puesta_id>/', validarNotificacionAC.as_view(), name='validar-notificacion-ac'),
    path('validar-notificacion-VP/<int:llamada_id>/<int:puesta_id>/', validarNotificacionVP.as_view(), name='validar-notificacion-vp'),
    path('manejar_imagen/', manejar_imagen, name='manejar_imagen'),



    # Generales 
    path('ver-llamadas/<int:llamada_id>/', ListLlamadasGenerales.as_view(), name='listLLamadasGen'),
    path('notificar-llamada/<int:llamada_id>/', notificacionLlamadaGenerales.as_view(), name='notificarLlamadaGen'),    
    path('validar-notificacion-gen/<int:llamada_id>/', validarNotificacionGenerales.as_view(), name='validar_notificacionGen'),
    path('crear-llamada-gen/<int:llamada_id>/', crearLlamadasGenerales.as_view(), name='crear_llamadaGen'),

]
