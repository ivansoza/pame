from django.urls import path,include
from .views import PuestaListView, PuestaCreateView, ExtranjeroCreateView, ExtranjeroListView,ExtranjeroUpdateView, ExtranjeroDeleteView

from . import views

urlpatterns = [
    path("Responsable/",views.responsableCrear, name="addResponsable"),
    path("PuestaPrueba/list",PuestaListView.as_view(), name="lista_puestas"),
    path('PuestaPrueba/crear_puesta/', PuestaCreateView.as_view(), name='crear_puesta'),
    
    path('PuestaPrueba/agregar_extranjero/<int:puesta_id>/', ExtranjeroCreateView.as_view(), name='agregar_extranjero'),
    path('PuestaPrueba/lista_extranjeros/<int:puesta_id>/', ExtranjeroListView.as_view(), name='lista_extranjeros'),
    path('PuestaPrueba/editar_extranjero/<int:pk>/', ExtranjeroUpdateView.as_view(), name='editar_extranjero'),
    path('eliminar_extranjero/<int:pk>/', views.ExtranjeroDeleteView.as_view(), name='eliminar_extranjero'),

   

]
