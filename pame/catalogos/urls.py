from django.urls import path,include
from . import views

urlpatterns = [
    path("Responsable/",views.responsableCrear, name="addResponsable"),
   

]
