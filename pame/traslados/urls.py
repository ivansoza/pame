from django.urls import path, include
from .views import ListTraslado, listarEstaciones, TrasladoCreateView, ListTrasladoDestino
urlpatterns = [
    
  #ORIGEN --------------------------
  path('listar-puestas-traslado/', ListTraslado.as_view(), name='listTraslado'),
  path('seleccionar-traslado/', listarEstaciones.as_view(), name='listEstaciones'),
  path('crear-traslado/<int:origen_id>/<int:destino_id>/', TrasladoCreateView.as_view(), name='crearTraslado'),



#DESTINO-----------------------------
  path('traslados-recibidos/', ListTrasladoDestino.as_view(), name='traslados_recibidos'),



]