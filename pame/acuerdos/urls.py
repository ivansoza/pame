from django.urls import path

from .views import acuerdo_inicio, constancia_llamada, homeAcuerdo, pdf, acuerdoInicio_pdf, \
derechoObligaciones_pdf


urlpatterns = [
    # urls prueba documentos pdf 
    path("plantilla", homeAcuerdo),
    path("pdf", pdf),
    # urls pame 
    path("deinicio/", acuerdo_inicio.as_view(), name="homeAcuerdoInicio"),
    path('acuerdoInicioPDF/<int:extranjero_id>', acuerdoInicio_pdf, name='acuerdoInicioPDF'),
    path('constancia_llamadas/<int:extranjero_id>', constancia_llamada, name='constanciaLlamadas'),
    path('derechosObligaciones/<int:extranjero_id>', derechoObligaciones_pdf, name='derechosObligaciones')
]
