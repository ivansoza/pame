from django.urls import path, include

from .views import homeCocinaGeneral, homeCocinaResponsable

urlpatterns = [
    path('cocina-general/', homeCocinaGeneral, name="homeCocinaGeneral"),
    path('cocina-responsable/', homeCocinaResponsable, name="homeCocinaResponsable"),


]
