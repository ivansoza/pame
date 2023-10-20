from django.urls import path

from .views import acuerdo_inicio, generate_pdf, constancia_llamada, homeAcuerdo


urlpatterns = [
    path("plantilla", homeAcuerdo),
    path("deinicio/", acuerdo_inicio.as_view(), name="homeAcuerdoInicio"),
    path('generar/<int:extranjero_id>', generate_pdf, name='generarPdf'),
    path('constancia_llamadas/<int:extranjero_id>', constancia_llamada, name='constanciaLlamadas'),
]
