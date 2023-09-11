from django.urls import path, include
from .views import ListTraslado
urlpatterns = [
  path('listTraslado/', ListTraslado.as_view(), name='listTraslado'),

]