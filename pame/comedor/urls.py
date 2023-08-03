from django.urls import path, include

from .views import homeCocinaGeneral, homeCocinaResponsable

urlpatterns = [
    path('cocina-responsable/', homeCocinaGeneral, name="homeCocinaGeneral"),

    
]
