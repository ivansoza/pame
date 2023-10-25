from django.urls import path
from . import views
from .views import acuerdo_inicio, constancia_llamada, homeAcuerdo, pdf, acuerdoInicio_pdf, \
derechoObligaciones_pdf, listRepositorio, DocumentosListView, lisExtranjerosInicio, lisExtranjerosComparecencia, lisExtranjerosPresentacion, listExtranjerosAcumulacion, \
listExtranjerosConclusion,listExtranjerosRadicacion,listExtranjerosRecepcion, listExtranjerosRecepcion,listExtranjerosSeparacion,listExtranjerosTraslado, \
 listExtranjerosArticulo,listExtranjerosComar,listExtranjerosDeportacion,listExtranjerosLibre,listExtranjerosRetorno,RepositorioListView

urlpatterns = [
    # urls prueba documentos pdf 
    path("plantilla", homeAcuerdo),
    path("pdf", pdf),
    # urls pame 
    path("deinicio/", acuerdo_inicio.as_view(), name="homeAcuerdoInicio"),
    path("repositorio/", listRepositorio.as_view(), name="repositorio"),
    path('documentos/<str:nup>/', RepositorioListView.as_view(), name="ver_documentos"),

    path('inicioPDF/<int:extranjero_id>', acuerdoInicio_pdf, name='inicioPDF'),
    path('constancia_llamadas/<int:extranjero_id>', constancia_llamada, name='constanciaLlamadas'),

    # pdf
    path('derechosObligaciones/<int:extranjero_id>', derechoObligaciones_pdf, name='derechosObligaciones'),


    # acuerdos
    path("inicio/", lisExtranjerosInicio.as_view(), name="lisExtranjerosInicio"),
    path("comparecencia/", lisExtranjerosComparecencia.as_view(), name="lisExtranjerosComparecencia"),
    path("presentacion/", lisExtranjerosPresentacion.as_view(), name="lisExtranjerosPresentacion"),

    # especiales
    path("acumulacion/", listExtranjerosAcumulacion.as_view(), name="listExtranjerosAcumulacion"),
    path("conclusion/", listExtranjerosConclusion.as_view(), name="listExtranjerosConclusion"),
    path("radicacion/", listExtranjerosRadicacion.as_view(), name="listExtranjerosRadicacion"),
    path("recepcion/", listExtranjerosRecepcion.as_view(), name="listExtranjerosRecepcion"),
    path("separacion/", listExtranjerosSeparacion.as_view(), name="listExtranjerosSeparacion"),
    path("traslado/", listExtranjerosTraslado.as_view(), name="listExtranjerosTraslado"),
    # resoluciones

    path("articulo/", listExtranjerosArticulo.as_view(), name="listExtranjerosArticulo"),
    path("comar/", listExtranjerosComar.as_view(), name="listExtranjerosComar"),
    path("deportacion/", listExtranjerosDeportacion.as_view(), name="listExtranjerosDeportacion"),
    path("libre/", listExtranjerosLibre.as_view(), name="listExtranjerosLibre"),
    path("retorno/", listExtranjerosRetorno.as_view(), name="listExtranjerosRetorno"),

]
