from django.urls import path, include
from .views import ListTraslado, listarEstaciones, TrasladoCreateView, ListTrasladoDestino, ListaExtranjerosTraslado, DeleteExtranjeroPuestaTraslado, ListaExtranjerosTrasladoDestino, cambiarStatus, cambiarStatusExtranjero, seguimientoPuesta, seguimientoPuestaDestino, cambiarStatusOrigen, cambiarStatusOrigenDestino,ActualizarTrasladoView,CambioEstacionView
from . import views
from .views import estadisticasEnvio, extranjeroTrasladadoList
from .views import estadisticasEnvio, eliminar_traslado
urlpatterns = [
    
  #ORIGEN --------------------------
  path('listar-puestas-traslado/', ListTraslado.as_view(), name='listTraslado'),
  path('seleccionar-traslado/', listarEstaciones.as_view(), name='listEstaciones'),
  path('crear-traslado/<int:origen_id>/<int:destino_id>/', TrasladoCreateView.as_view(), name='crearTraslado'),
  path('lista-extranjeros/<int:traslado_id>/', ListaExtranjerosTraslado.as_view(), name='listaExtranjerosTraslado'),
  path('eliminar-extranjeros/<int:pk>/', DeleteExtranjeroPuestaTraslado.as_view(), name='eliminarExtranjerosTraslado'),
  path('seguimiento-puesta/<int:pk>/', seguimientoPuesta.as_view(), name='seguimientoPuesta'),
  path('editar-status-puesta/<int:pk>/', cambiarStatusOrigen.as_view(), name='cambiarStatusOrigen'),
  path('editar-status-puesta-destino/<int:pk>/', cambiarStatusOrigenDestino.as_view(), name='cambiarStatusOrigenDestino'),


#DESTINO-----------------------------
  path('traslados-recibidos/', ListTrasladoDestino.as_view(), name='traslados_recibidos'),
  path('lista-extranjeros-destino/<int:traslado_id>/', ListaExtranjerosTrasladoDestino.as_view(), name='listaExtranjerosTrasladoDestino'),
  path('editar-status/<int:pk>/', cambiarStatus.as_view(), name='editar-status'),
  path('editar-status-extranjero/<int:pk>/', cambiarStatusExtranjero.as_view(), name='editar-status-extranjero'),
  path('seguimiento-puesta-destino/<int:pk>/', seguimientoPuestaDestino.as_view(), name='seguimientoPuestaDestino'),
  path('estadistica/<int:traslado_id>/', estadisticasEnvio.as_view(), name='estadistica'),


# Documentos PDF
  path('reporte-ac/<int:extranjero_id>/', views.documento_ac, name='reporteAC'),
  path('generar/<int:extranjero_id>', views.generate_pdf, name='generar_pdf'),
  path('mi-vista/', views.mi_vista, name='mi_vista'),


  # cambio de estacion

  path('actualizar_traslado/<int:traslado_id>/', ActualizarTrasladoView.as_view(), name='actualizar_traslado'),
  path('cambio_estacion/<int:pk>/', CambioEstacionView.as_view(), name='cambio_estacion'),
  path('listTrasladados/', extranjeroTrasladadoList.as_view(), name='listTrasladados'),

# eliminar traslado
  path('eliminar_traslado/<int:pk>/', views.eliminar_traslado, name='eliminar_traslado'),

]

