from django.urls import path
from . import views
from .views import acuerdo_inicio, constancia_llamada, homeAcuerdo, pdf, acuerdoInicio_pdf, \
    derechoObligaciones_pdf, listRepositorio, DocumentosListView, lisExtranjerosInicio, lisExtranjerosComparecencia, lisExtranjerosPresentacion, listExtranjerosAcumulacion, \
    listExtranjerosConclusion,listExtranjerosRadicacion,listExtranjerosRecepcion, listExtranjerosRecepcion,listExtranjerosSeparacion,listExtranjerosTraslado, \
    listExtranjerosArticulo,listExtranjerosComar,listExtranjerosDeportacion,listExtranjerosLibre,listExtranjerosRetorno,RepositorioListView,mostrar_derechoObligaciones_pdf,AcuerdoInicioCreateView, registro_acuerdo_inicio,  \
    listExtranjerosConclusion,listExtranjerosRadicacion,listExtranjerosRecepcion, listExtranjerosRecepcion,listExtranjerosSeparacion,listExtranjerosTraslado, nombramientoRepresentante_pdf, \
    listExtranjerosArticulo,listExtranjerosComar,listExtranjerosDeportacion,listExtranjerosLibre,listExtranjerosRetorno,RepositorioListView,mostrar_derechoObligaciones_pdf, \
    notificacionRepresentacion_pdf,AcuerdoInicioCreateView, inventarioPV_pdf, listaLlamadas_pdf, constanciaEnseres_pdf, formatoEnseres_pdf, comparecencia_pdf, presentacion_pdf, \
    certificadoMedico_pdf, noLesiones_pdf, recetaMedica_pdf, recepcionDoc_pdf, noFirma_pdf, radicacion_pdf, separacionAlojados_pdf, acumulacionExpedientes_pdf, suspensionProvisional_pdf, \
    continuacionProcedimiento_pdf, egresoInstalacion_pdf, administrativo_pdf, conclusionProcedimiento_pdf, procedimientoAdministrativo_pdf, ampliacionAlojamiento_pdf, \
    notificacionConsulado_pdf, solicitudRefugio_pdf, notificacionFiscalia_pdf, resolucionDeportacion_pdf, guardar_comparecencia, mostrar_comparecencia_pdf, resolucionLibre_pdf, \
    acResolucionLibre_pdf, resolucionRegularizacion_pdf, oficioRegularizacion_pdf, resolucionComar_pdf, resolucionRetorno_pdf

from .views import FirmaTestigoUnoCreateView, FirmaTestigoDosCreateView, check_firma_testigo_uno, check_firma_testigo_dos
urlpatterns = [
    # urls prueba documentos pdf 
    path("plantilla", homeAcuerdo),
    path("pdf", pdf),
    # urls pame 
    path("deinicio/", acuerdo_inicio.as_view(), name="homeAcuerdoInicio"),
    path("repositorio/", listRepositorio.as_view(), name="repositorio"),
    path('documentos/<str:nup>/', RepositorioListView.as_view(), name="ver_documentos"),

    path('constancia_llamadas/<int:extranjero_id>', constancia_llamada, name='constanciaLlamadas'),

    # pdf
    path('derechosObligaciones/<int:extranjero_id>', derechoObligaciones_pdf, name='derechosObligaciones'),
    path('mostrar-derechos-obligaciones/<int:extranjero_id>', mostrar_derechoObligaciones_pdf, name='mostrarderechosObligaciones'),
    path('inicioPDF/<str:nup_id>/', acuerdoInicio_pdf, name='inicioPDF'),
    path('nombramientoRepresentante', nombramientoRepresentante_pdf, name='representantePDF'),
    path('notificacionRepresentacion', notificacionRepresentacion_pdf, name='representacionPDF'),
    path('inventariopv', inventarioPV_pdf, name='inventarioPDF'),
    path('listaLlamadas/<int:extranjero_id>', listaLlamadas_pdf, name='listaLlamadasPDF'),
    path('constancia-enseres/<str:nup_id>/', constanciaEnseres_pdf, name='enseresPDF'),
    path('formato-enseres/<str:nup_id>/<str:enseres_id>/', formatoEnseres_pdf, name='fenseresPDF'),
    path('ver-comparecencia/', comparecencia_pdf, name='comparecenciaPDF'),
    path('acpresentacion', presentacion_pdf, name='presentacionPDF'),
    path('certificado-medico', certificadoMedico_pdf, name='certificadoPDF'),
    path('no-lesiones', noLesiones_pdf, name='nolesionesPDF'),
    path('recetaMedica/<str:nup_id>/<str:ex_id>/', recetaMedica_pdf, name='recetaPDF'),
    path('recepcion-documentos', recepcionDoc_pdf, name='recepcionDocPDF'),
    path('no-firma', noFirma_pdf, name='noFirmaPDF'),
    path('ac-radicacion', radicacion_pdf, name='radicacionPDF'),
    path('separacion-alojados', separacionAlojados_pdf, name='separacionPDF'),
    path('acumulacion-expedientes', acumulacionExpedientes_pdf, name='acumulacionPDF'),
    path('suspension-provisional', suspensionProvisional_pdf, name='suspensionPDF'),
    path('continuacion-procedimiento', continuacionProcedimiento_pdf, name='continuacionPDF'),
    path('egreso-instalacion', egresoInstalacion_pdf, name='egresoPDF'),
    path('acadministrativo', administrativo_pdf, name='administrativoPDF'),
    path('conclusion-procedimiento', conclusionProcedimiento_pdf, name='conclusionPDF'),
    path('procedimiento-administrativo', procedimientoAdministrativo_pdf, name='procedimientoPDF'),
    path('ampliacion-alojamiento', ampliacionAlojamiento_pdf, name='ampliacionPDF'),
    path('notificacion-consulado', notificacionConsulado_pdf, name='consuladoPDF'),
    path('solicitud-refugio', solicitudRefugio_pdf, name='ComarPDF'),
    path('notificacion-fiscalia', notificacionFiscalia_pdf, name='fiscaliaPDF'),
    path('resolucion-deportacion', resolucionDeportacion_pdf, name='deportacionPDF'),
    path('resolucion-libretransito', resolucionLibre_pdf, name='librePDF'),
    path('acuerdo-libretransito', acResolucionLibre_pdf, name='aclibrePDF'),
    path('resolucion-regularizacion', resolucionRegularizacion_pdf, name='regularizacionPDF'),
    path('oficio-regularizacion', oficioRegularizacion_pdf, name='oregularizacionPDF'),
    path('resolucion-comar', resolucionComar_pdf, name='rcomarPDF'),
    path('resolucion-retorno', resolucionRetorno_pdf, name='retornoPDF'),

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



    path('crearAcuerdoInicio/<str:proceso_id>/', AcuerdoInicioCreateView.as_view(), name='crearAcuerdoInicio'),



    path('registro_acuerdo_inicio/<str:proceso_id>/', views.registro_acuerdo_inicio, name='registro_acuerdo_inicio'),
    path('generar_qr/<str:testigo>/<int:acuerdo_id>/', views.generar_qr_acuerdos, name='generar_qr_acuerdos'),

    path('check_firma_testigo_uno/<int:acuerdo_id>/', check_firma_testigo_uno, name='check_firma_testigo_uno'),
    path('check_firma_testigo_dos/<int:acuerdo_id>/', check_firma_testigo_dos, name='check_firma_testigo_dos'),

    path('firma_testigo_uno/<int:acuerdo_id>/', views.firma_testigo_uno, name='firma_testigo_uno'),
    path('firma_testigo_dos/<int:acuerdo_id>/', views.firma_testigo_dos, name='firma_testigo_dos'),
    
    path('comparecencia/guardar/<int:comparecencia_id>/', guardar_comparecencia, name='guardar_comparecencia'),
    path('mostrar-comparecencia/<int:comparecencia_id>/', mostrar_comparecencia_pdf, name='guardar_comparecencia'),

]
