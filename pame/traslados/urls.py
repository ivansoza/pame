from django.urls import path, include
from .views import ListTraslado, listarEstaciones, TrasladoCreateView, ListTrasladoDestino, ListaExtranjerosTraslado
urlpatterns = [
    
  #ORIGEN --------------------------
  path('listar-puestas-traslado/', ListTraslado.as_view(), name='listTraslado'),
  path('seleccionar-traslado/', listarEstaciones.as_view(), name='listEstaciones'),
  path('crear-traslado/<int:origen_id>/<int:destino_id>/', TrasladoCreateView.as_view(), name='crearTraslado'),
  path('lista-extranjeros/<int:traslado_id>/', ListaExtranjerosTraslado.as_view(), name='listaExtranjerosTraslado'),


#DESTINO-----------------------------
  path('traslados-recibidos/', ListTrasladoDestino.as_view(), name='traslados_recibidos'),



]