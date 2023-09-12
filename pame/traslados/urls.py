from django.urls import path, include
from .views import ListTraslado, CrearPuestaTranslado
urlpatterns = [
  path('listTraslado/', ListTraslado.as_view(), name='listTraslado'),
  path('crear-traslado/', CrearPuestaTranslado.as_view(), name='crear-traslado'),


]