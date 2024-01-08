from django.urls import path, include

from .views import homeCocinaGeneral, homeCocinaResponsable, comedor,alimentos

urlpatterns = [
    path('cocina-general/', homeCocinaGeneral, name="homeCocinaGeneral"),
    #path('cocina-general/', MiVista.as_view(), name="homeCocinaGeneral"),
    path('cocina-responsable/', homeCocinaResponsable, name="homeCocinaResponsable"),
    path('comedor/', comedor.as_view(), name="comedor"),
    path('alimentos/', alimentos.as_view(), name="alimentos"),

]
