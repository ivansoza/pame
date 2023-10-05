from django.urls import path

from .views import acuerdo_inicio, generate_pdf

urlpatterns = [
    path("deinicio/", acuerdo_inicio.as_view(), name="homeAcuerdoInicio"),
    path('generar/<int:extranjero_id>', generate_pdf, name='generarPdf'),

]
