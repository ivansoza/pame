from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest, Http404
from django.template.loader import render_to_string, get_template
from django.views.generic import ListView, CreateView
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery, Exists
from django.urls import reverse, reverse_lazy
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.storage import default_storage
from django.contrib.auth import get_user_model

import os
import locale
import base64
import io
from datetime import datetime
from io import BytesIO

import qrcode
from weasyprint import HTML

from comparecencia.models import Comparecencia, FirmaComparecencia
from vigilancia.models import Extranjero, Firma, NoProceso,HuellaTemp, descripcion
from llamadasTelefonicas.models import Notificacion, LlamadasTelefonicas
from acuerdos.models import Documentos, ClasificaDoc, TiposDoc, Repositorio, TipoAcuerdo, Acuerdo
from pertenencias.models import (
    EnseresBasicos, Pertenencias, Pertenencia_aparatos, valoresefectivo, valoresjoyas,
    documentospertenencias
)
from catalogos.models import AutoridadesActuantes, RepresentantesLegales, Traductores, Consulado, Estacion, Comar, Fiscalia
from salud.models import Consulta, CertificadoMedico, FirmaMedico, constanciaNoLesiones, CertificadoMedicoEgreso
from notificaciones.models import NotificacionConsular, FirmaNotificacionConsular, NotificacionCOMAR, NotificacionFiscalia, FirmaNotificacionFiscalia, FirmaNotificacionComar, ExtranjeroDefensoria

from .forms import AcuerdoInicioForm, FirmaTestigoDosForm, FirmaTestigoUnoForm
from .models import FirmaAcuerdo
from notificaciones.models import firmasDefenso
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

# ----- Vista de Prueba para visualizar las plantillas en html -----
def homeAcuerdo(request):
    return render(request,"documentos/Derechos.html")

# ----- Vista de prueba para visualizar los pdf -----
def pdf(request):
    # Tu lógica para obtener los datos y generar el contexto
    context = {
        # ...
    }
    
    # Renderiza la plantilla HTML
    html_template = get_template('documentos/acuerdoLibre.html')
    html_string = html_template.render(context)
    
    # Convierte la plantilla HTML a PDF con WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="docPrueba.pdf"'
    
    html = HTML(string=html_string)
    html.write_pdf(response)
    
    return response

# ----- Lista Extranjeros para ver o generar Acuerdo de Inicio -----
class acuerdo_inicio(LoginRequiredMixin,ListView):
    template_name = 'acuerdoInicio.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get(self, request):
        extranjeros = Extranjero.objects.filter(estatus='Activo')
        # extranjeros = Extranjero.objects.all() # Obtiene todos los extranjeros 
        
        # Calcular si el PDF existe para cada extranjero
        pdf_existencia = [(extranjero, pdf_exist(extranjero.id)) for extranjero in extranjeros]

        # Ordenar la lista en función de pdf_exists (False primero)
        extranjeros_ordenados = sorted(pdf_existencia, key=lambda x: x[1])

        context = {
            'navbar': 'acuerdos', # Sección de acuerdos 
            'seccion': 'presentacion', # Sección de Inicio de acuerdos
            'acuerdo': 'inicio',
            'extranjeros': [extranjero for extranjero, _ in extranjeros_ordenados],
            'extranjeros_pdf': pdf_existencia
            }
        return render(request, self.template_name, context)

class listRepositorio(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjeros.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context

class DocumentosListView(LoginRequiredMixin,ListView):
    model = Documentos
    template_name = 'verAllAcuerdos.html'  # El nombre de tu template para mostrar los documentos
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        nup_value = self.kwargs.get('nup')
        return Documentos.objects.filter(nup__nup=nup_value)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context
        
class RepositorioListView(LoginRequiredMixin,ListView):
    model = Repositorio
    template_name = 'verAllAcuerdos.html'  # El nombre de tu template para mostrar los documentos
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        nup_value = self.kwargs.get('nup')
        return Repositorio.objects.filter(nup__nup=nup_value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nup_value = self.kwargs.get('nup')
            
        try:
            no_proceso_instance = NoProceso.objects.get(nup=nup_value)
            apellido_materno = no_proceso_instance.extranjero.apellidoMaternoExtranjero
            if apellido_materno:  # Si hay apellido materno
                extranjero_name = f"{no_proceso_instance.extranjero.nombreExtranjero} {no_proceso_instance.extranjero.apellidoPaternoExtranjero} {apellido_materno}"
            else:  # Si no hay apellido materno
                extranjero_name = f"{no_proceso_instance.extranjero.nombreExtranjero} {no_proceso_instance.extranjero.apellidoPaternoExtranjero}"
            
            context['nombre_extranjero'] = extranjero_name
        except NoProceso.DoesNotExist:
            context['nombre_extranjero'] = "Desconocido"
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context


def servir_pdf(request, repositorio_id):
    try:
        repo = Repositorio.objects.get(id=repositorio_id)
        file_path = repo.archivo.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    except Repositorio.DoesNotExist:
        raise Http404
    
# ----- Comprueba si el acuerdo de inicio existe en la carpeta 
def pdf_exist(extranjero_id):
    nombre_pdf = f"AcuerdoInicio_{extranjero_id}.pdf"
    ubicacion_pdf = os.path.join("pame/media/files", nombre_pdf)
    exists = os.path.exists(ubicacion_pdf)

    return exists

# ----- Funcion para cambiar los numeros del dia a palabra
def numero_a_palabra(numero):
    palabras = [
        'cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez',
        'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve',
        'veinte', 'veintiuno', 'veintidós', 'veintitrés', 'veinticuatro', 'veinticinco', 'veintiséis',
        'veintisiete', 'veintiocho', 'veintinueve', 'treinta', 'treinta y uno'
    ]
    return palabras[numero]

# ----- Funcion para cambiar de numero a palabra los meses
def mes_a_palabra(mes):
    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    return meses[mes - 1]  # Restamos 1 porque los meses se cuentan desde 1 enero a 12 diciembre 

# ----- Genera el documento PDF acuerdo de inicio y lo guarda en la ubicacion especificada 
def acuerdoInicio_pdf(request, nup_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero
    acuerdo = get_object_or_404(Acuerdo, nup=no_proceso)  # Aquí pasamos el objeto no_proceso directamente
    nombre = extranjero.nombreExtranjero
    apellidop = extranjero.apellidoPaternoExtranjero
    apellidom = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    nombreac = extranjero.deLaEstacion.responsable.nombre
    apellidopac = extranjero.deLaEstacion.responsable.apellidoPat
    apellidomac = extranjero.deLaEstacion.responsable.apellidoMat
    lugar = extranjero.deLaEstacion.estado
    estacion = extranjero.deLaEstacion.nombre
    dia = extranjero.fechaRegistro.day
    mes = extranjero.fechaRegistro.month
    anio = extranjero.fechaRegistro.year

    dia_texto = numero_a_palabra(dia)
    mes_texto = mes_a_palabra(mes)

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'nombre': nombre,
        'apellidop': apellidop,
        'apellidom': apellidom,
        'nacionalidad': nacionalidad,
        'nombreac' : nombreac,
        'apellidopac': apellidopac,
        'apellidomac': apellidomac,
        'lugar': lugar,
        'estacion' : estacion,
        'dia': dia_texto,
        'mes': mes_texto,
        'anio': anio,
        'acuerdo': acuerdo,

    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acuerdoInicio.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de nombramiento de representante legal
def nombramientoRepresentante_pdf(request):
    # extranjero = Extranjero.objects.get(id=extranjero_id)

    #consultas 

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/nombramientoRepresentante.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Notificacion de representacion
def notificacionRepresentacion_pdf(request, nup_id):
    # extranjero = Extranjero.objects.get(id=extranjero_id)
    usuario_actual = request.user
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero
    defensoria = get_object_or_404(ExtranjeroDefensoria, nup=no_proceso)  # Aquí pasamos el objeto no_proceso directamente
    oficio = defensoria
    defen = defensoria.defensoria

    firma = firmasDefenso.objects.filter(defensoria=defensoria).first()
    firma_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url) if firma and firma.firmaAutoridadActuante else None

    #consultas 
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'oficio': oficio,
        'extranjero':extranjero,
        'defensoria': defen,
        "defenso":defensoria,
        "firma":firma,
        "firma_url":firma_url,


    }

    # Obtener la plantilla HTML
    template = get_template('documentos/notificacionRepresentacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificaciones")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Notificacion a Defensoría", delaClasificacion=clasificacion)

    nombre_pdf = f"Notificacion_Defensoría.pdf"
    no_proceso = defensoria.nup
    # no_proceso.notificacion_consular = True  # Descomenta y ajusta si es necesario
    no_proceso.save()
    repo = Repositorio(
        nup=defensoria.nup,
        delTipo=tipo_doc,
        delaEstacion=usuario_actual.estancia,
        delResponsable=usuario_actual.get_full_name(),
    )
    repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
    repo.save()
    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF de Inventario de pertenencias y valores
def inventarioPV_pdf(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = Extranjero.objects.get(id=ex_id)

    pertenencias = Pertenencias.objects.filter(
        delInventario__noExtranjero__id=extranjero.id,
        delInventario__nup__nup=no_proceso.nup,
    )

    aparatos = Pertenencia_aparatos.objects.filter(
        delInventario__noExtranjero__id=extranjero.id,
        delInventario__nup__nup=no_proceso.nup
    )

    efectivos = valoresefectivo.objects.filter(
        delInventario__noExtranjero__id=extranjero.id,
        delInventario__nup__nup=no_proceso.nup
    )

    alhajas = valoresjoyas.objects.filter(
        delInventario__noExtranjero__id=extranjero.id,
        delInventario__nup__nup=no_proceso.nup
    )

    documentos = documentospertenencias.objects.filter(
        delInventario__noExtranjero__id=extranjero.id,
        delInventario__nup__nup=no_proceso.nup
    )

    # Obtenemos la autoridad actuante 
    try:
        # Intenta obtener al Director
        autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Director', estatus='Activo')
    except ObjectDoesNotExist:
        try:
            # Si no existe el Director, intenta obtener al Subdirector
            autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Subdirector', estatus='Activo')
        except ObjectDoesNotExist:
            try:
                # Si no existe el Subdirector, intenta obtener al Jefe de Seguridad
                autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Jefe de Seguridad', estatus='Activo')
            except ObjectDoesNotExist:
                # Manejar el caso en que ninguno de los cargos exista
                autoridad = ""

    #consultas
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre
    pertenencia = pertenencias
    aparato = aparatos
    efectivo = efectivos
    alhaja = alhajas
    documento = documentos
    foto = extranjero.biometrico
    foto_url = f"{settings.BASE_URL}{foto.fotografiaExtranjero.url}"
    firma_ex = extranjero.firma 
    firmaex_url = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'oficina': oficina,
        'estacion': estacion,
        'ex': extranjero,
        'pert': pertenencia,
        'apa': aparato,
        'efe': efectivo,
        'al': alhaja,
        'doc': documento,
        'foto': foto_url,
        'firmaex': firmaex_url,
        'autoridad': autoridad
    } 

    # Obtener la plantilla HTML
    template = get_template('documentos/inventarioPV.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF de Lista de llamadas "Constancia de llamadas"
def listaLlamadas_pdf(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = Extranjero.objects.get(id=ex_id)
    
    llamadas = LlamadasTelefonicas.objects.filter(
        noExtranjero=extranjero,
        nup=no_proceso
    )

    #consultas
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre
    nombre = extranjero.nombreExtranjero 
    paterno = extranjero.apellidoPaternoExtranjero
    materno = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    ingreso = extranjero.fechaRegistro
    firma = extranjero.firma
    firma_url = f"{settings.BASE_URL}{firma.firma_imagen.url}"

    fechas_llamadas = [llamada.fechaHoraLlamada.strftime('%d/%m/%y') for llamada in llamadas]

    

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'oficina':oficina,
        'estacion': estacion,
        'nombreEx': nombre,
        'paterno': paterno,
        'materno': materno,
        'nacionalidad': nacionalidad,
        'ingreso': ingreso,
        'fechas_llamadas': fechas_llamadas,
        'firma': firma_url
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/listaLlamadas.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Constancia de entrega de enseres basicos de aseo personal
def constanciaEnseres_pdf(request, nup_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero

    #consultas 
    nombre = extranjero.nombreExtranjero
    paterno = extranjero.apellidoPaternoExtranjero
    materno = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    ingreso = extranjero.fechaRegistro
    firma_ex = extranjero.firma
    firma = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre

    fechas_enseres = [enseres.fechaEntrega.strftime('%d/%m/%y') for enseres in extranjero.enseresbasicos_set.all()]

    # Obtenemos la autoridad actuante "Que superviso el bien servicio"
    # Debe ser solo Director o Subdirector
    try:
        # Intenta obtener al Director
        autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Director', estatus='Activo')
    except ObjectDoesNotExist:
        try:
            # Si no existe el Director, intenta obtener al Subdirector
            autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Subdirector', estatus='Activo')
        except ObjectDoesNotExist:
            autoridad = ""

    # Obtenemos la autoridad actuante "Que proporciono el bien servicio"
    # Cualquier cargo menos Director o Subdirector
    try:
        autoridad2 = AutoridadesActuantes.objects.exclude(cargo__in=['Director', 'Subdirector']).filter(estacion=extranjero.deLaEstacion, estatus='Activo').first()
    except ObjectDoesNotExist:
        autoridad2 = []


    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'nombre': nombre,
        'paterno': paterno,
        'materno': materno,
        'nacionalidad': nacionalidad,
        'ingreso': ingreso,
        'fechas_enseres': fechas_enseres,
        'firma': firma,
        'oficina':oficina,
        'estacion': estacion, 
        'autoridad':autoridad,
        'autoridad2': autoridad2
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/constanciaEnseres.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de formato de enseres basicos 
def formatoEnseres_pdf(request, nup_id, enseres_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero
    enseres_asignados = EnseresBasicos.objects.filter(noExtranjero=extranjero, nup=no_proceso, id=enseres_id)

    
    # Convierte los enseres a una cadena legible para mostrar en el PDF
    enseres_asignados_str = ', '.join(enseres_asignados[0].enseres) if enseres_asignados else ''

    # Obtiene los enseres extras 
    enseres_extras = enseres_asignados[0].enseresExtras if enseres_asignados else ''

    # Obtenemos la autoridad actuante 
    try:
        # Intenta obtener al Director
        autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Director', estatus='Activo')
    except ObjectDoesNotExist:
        try:
            # Si no existe el Director, intenta obtener al Subdirector
            autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Subdirector', estatus='Activo')
        except ObjectDoesNotExist:
            try:
                # Si no existe el Subdirector, intenta obtener al Jefe de Seguridad
                autoridad = AutoridadesActuantes.objects.get(estacion=extranjero.deLaEstacion, cargo='Jefe de Seguridad', estatus='Activo')
            except ObjectDoesNotExist:
                # Manejar el caso en que ninguno de los cargos exista
                autoridad = None

    #consultas 
    nombre = extranjero.nombreExtranjero
    paterno = extranjero.apellidoPaternoExtranjero
    materno = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    ingreso = extranjero.fechaRegistro
    firma_ex = extranjero.firma
    firmaex_url = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre

    fechas_enseres = [enseres.fechaEntrega.strftime('%d/%m/%y') for enseres in extranjero.enseresbasicos_set.all()]

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'nombre': nombre,
        'paterno': paterno,
        'materno': materno,
        'nacionalidad': nacionalidad,
        'ingreso': ingreso,
        'fechas_enseres': fechas_enseres,
        'firma': firmaex_url,
        'enseres_asignados': enseres_asignados_str,
        'enseres_extras': enseres_extras,
        'oficina': oficina,
        'estacion': estacion,
        'autoridad': autoridad
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/formatoEnseres.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de comparecencia  


# ----- Genera el documento PDF, de Presentacion   
def presentacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/presentacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response


# ----- Genera el documento PDF, de Presentacion   
def filiacion_pdf(request, nup_id):
    usuario_actual = request.user

    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero 

    huellas = HuellaTemp.objects.using('huella_base').filter(dni=extranjero.id).values()
    descri = descripcion.objects.get(delExtranjero=extranjero.id)
    foto = extranjero.biometrico
    foto_url = f"{settings.BASE_URL}{foto.fotografiaExtranjero.url}"
    firma_ex = extranjero.firma
    firmaex_url = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"
    huella_images = [None] * 10

    # Recorrer los dedos del 1 al 10
    for dedo in range(1, 11):
        # Obtener la huella correspondiente al dedo actual
        huella = huellas.filter(ndedo=dedo).first()
        
        # Verificar si la huella existe y tiene una imagen
        if huella and huella['imagen']:
            # Almacenar la imagen en la lista en la posición correspondiente al dedo
            huella_images[dedo - 1] = huella['imagen']

    # Ahora, puedes acceder a las imágenes de cada dedo en la lista huella_images:
    imagen_1_huella = huella_images[0]
    imagen_2_huella = huella_images[1]
    imagen_3_huella = huella_images[2]
    imagen_4_huella = huella_images[3]
    imagen_5_huella = huella_images[4]
    imagen_6_huella = huella_images[5]
    imagen_7_huella = huella_images[6]
    imagen_8_huella = huella_images[7]
    imagen_9_huella = huella_images[8]
    imagen_10_huella = huella_images[9]

    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'extranjero':extranjero,
        'huella':huellas,
        'foto':foto_url,
        'firmaex':firmaex_url,
        'huella_2':imagen_2_huella,
        'huella_1':imagen_1_huella,
        'huella_3':imagen_3_huella,
        'huella_4':imagen_4_huella,
        'huella_5':imagen_5_huella,
        'huella_6':imagen_6_huella,
        'huella_7':imagen_7_huella,
        'huella_8':imagen_8_huella,
        'huella_9':imagen_9_huella,
        'huella_10':imagen_10_huella,
        'descripcion':descri,
       
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/filiacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()

    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Inicio")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Media Filiación", delaClasificacion=clasificacion)
   
    nombre_pdf = f"04_Media_filiación.pdf"
    no_proceso = extranjero.nup

    no_proceso.save()


    repo = Repositorio(
        nup=no_proceso.nup,
        delTipo=tipo_doc,
        delaEstacion=usuario_actual.estancia,
        delResponsable=usuario_actual.get_full_name(),
    )
    repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
    repo.save()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Certificado Medico 
def certificadoMedico_pdf(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = Extranjero.objects.get(id=ex_id)
    
    # Obtener informacion del centificado medico
    certificado = CertificadoMedico.objects.get(
        extranjero=extranjero,
        nup=no_proceso
    )

    #consultas
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre
    ex = extranjero
    cert = certificado 
    foto = extranjero.biometrico
    foto_url = f"{settings.BASE_URL}{foto.fotografiaExtranjero.url}"
    firma_ex = extranjero.firma
    firmaex_url = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"
    dr = certificado.delMedico
    firma_dr = FirmaMedico.objects.filter(medico=dr.usuario).first()
    firma_dr_url = f"{settings.BASE_URL}{firma_dr.firma_imagen.url}"

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'oficina': oficina,
        'estacion': estacion,
        'ex':ex,
        'cer':cert,
        'foto':foto_url,
        'dr':dr, 
        'firmadr':firma_dr_url,
        'firmaex':firmaex_url
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/certificadoMedico.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Certificado Medico 
def certificadoMedicoEgreso_pdf(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = Extranjero.objects.get(id=ex_id)
    
    # Obtener informacion del centificado medico
    certificado = CertificadoMedicoEgreso.objects.get(
        extranjero=extranjero,
        nup=no_proceso
    )

    #consultas
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre
    ex = extranjero
    cert = certificado 
    foto = extranjero.biometrico
    foto_url = f"{settings.BASE_URL}{foto.fotografiaExtranjero.url}"
    firma_ex = extranjero.firma
    firmaex_url = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"
    dr = certificado.delMedico
    firma_dr = FirmaMedico.objects.filter(medico=dr.usuario).first()
    firma_dr_url = f"{settings.BASE_URL}{firma_dr.firma_imagen.url}"

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'oficina': oficina,
        'estacion': estacion,
        'ex':ex,
        'cer':cert,
        'foto':foto_url,
        'dr':dr, 
        'firmadr':firma_dr_url,
        'firmaex':firmaex_url
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/certificadoMedicoEg.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Constancia de no lesiones
def noLesiones_pdf(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = Extranjero.objects.get(id=ex_id)

    # Obtener informacion del certificado no lesiones
    lesiones = constanciaNoLesiones.objects.get(
        extranjero=extranjero,
        nup=no_proceso
    )
    
    #consultas 
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion
    ex = extranjero
    les = lesiones
    firma_ex = extranjero.firma
    firma_ex_url = f"{settings.BASE_URL}{firma_ex.firma_imagen.url}"

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'oficina': oficina,
        'estacion': estacion,
        'ex':ex,
        'les':les,
        'firma_ex':firma_ex_url
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/noLesiones.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de receta medica 
def recetaMedica_pdf(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero

    # Consultar la información de la consulta
    consulta = Consulta.objects.get(
        extranjero=extranjero, 
        nup=no_proceso, 
        id=ex_id)
    
    #consultas 
    medico = consulta.delMedico
    ex = consulta.extranjero
    receta = consulta
    tratamiento = consulta.tratamiento
    estacion = consulta.extranjero.deLaEstacion.nombre
    oficina = consulta.extranjero.deLaEstacion.oficina
    firma = extranjero.firma
    firma_url = f"{settings.BASE_URL}{firma.firma_imagen.url}"

    # Dividir el tratamiento por comas y pasar la lista a la plantilla
    tratamiento_lista = tratamiento.split(',')

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'medico': medico,
        'extranjero': ex,
        'receta': receta, 
        'tratamiento': tratamiento_lista,
        'estacion': estacion,
        'oficina': oficina,
        'firma': firma_url
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/recetaMedica.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Recepcion de documentos
def recepcionDoc_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/recepcionDoc.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de constancia de no firma 
def noFirma_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/noFirma.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de radicacion 
def radicacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/radicacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de separacion de alojados
def separacionAlojados_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/separacionAlojados.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de acumulacion de expedientes
def acumulacionExpedientes_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acumulacionExpedientes.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de suspension provisional del procedimiento
def suspensionProvisional_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/suspensionProvisional.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de continuacion del procedimiento 
def continuacionProcedimiento_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/continuacionProcedimiento.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de egreso de instalacion migratoria
def egresoInstalacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/egresoInstalacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo administrativo
def administrativo_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/administrativo.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo conclusion de procedimiento 
def conclusionProcedimiento_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/conclusionProcedimiento.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de procedimiento administrativo migratorio
def procedimientoAdministrativo_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/procedimientoAdministrativo.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de ampliacion de alojamiento por factor de riesgo
def ampliacionAlojamiento_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/ampliacionAlojamiento.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de notificacion consular
def notificacionConsulado_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/notificacionConsular.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response


def notificacionConsulado_pdf(request):
    # DEFINES LOS GET QUE SE CAPTURAN EN EL FORMS
    delaEstacion = request.POST.get('delaEstacion', '')
    nup = request.POST.get('nup', '')
    numeroOficio = request.POST.get('numeroOficio', '')
    delConsulado = request.POST.get('delConsulado', '')
    accion = request.POST.get('accion', '')
    delaAutoridad = request.POST.get('delaAutoridad', '')


    no_proceso = get_object_or_404(NoProceso, nup=nup)
    extranjero = no_proceso.extranjero
    autoridad_actuante = None
    if delaAutoridad:
        autoridad_actuante = get_object_or_404(AutoridadesActuantes, pk=delaAutoridad)

    consulado = None
    if delConsulado:  
        consulado = get_object_or_404(Consulado, pk=delConsulado)

    context = {
        'consulado': consulado,
        'nup': nup,
        'numeroOficio': numeroOficio,
        'delConsulado': delConsulado,
        'accion': accion,
        'autoridad_actuante': autoridad_actuante,
        'extranjero': extranjero,  # Agregando el objeto extranjero al contexto

    }

    # Obtener la plantilla HTML
    template = get_template('documentos/notificacionConsular.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de solicitud de refugio


# ----- Genera el documento PDF, de Acuerdo de resolucion definitiva
def resolucionDeportacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionDeportacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de resolucion libre de transito
def resolucionLibre_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionLibre.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de libre de transito
def acResolucionLibre_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acuerdoLibre.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de la resolucion de regularizacion art 133
def resolucionRegularizacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionRegularizacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de oficio de regularizacion art 133
def oficioRegularizacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/oficioRegularizacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de resolucion de regularizacion comar
def resolucionComar_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionComar.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de resolucion de retorno asistido
def resolucionRetorno_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionRetorno.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Anexo 6 (Documento provisional)
def documentoProvisional_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/documentoProvisional.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de razones humanitarias
@login_required(login_url="/permisoDenegado/") 
def razonesHumanitarias_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/razonesHumanitarias.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de resolucion definitiva
def resolucionDeportacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionDeportacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de resolucion libre de transito
def resolucionLibre_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionLibre.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de libre de transito
def acResolucionLibre_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acuerdoLibre.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de la resolucion de regularizacion art 133
def resolucionRegularizacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionRegularizacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de oficio de regularizacion art 133
def oficioRegularizacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/oficioRegularizacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de resolucion de regularizacion comar
def resolucionComar_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionComar.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de resolucion de retorno asistido
def resolucionRetorno_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/resolucionRetorno.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Anexo 6 (Documento provisional)
def documentoProvisional_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/documentoProvisional.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de razones humanitarias
@login_required(login_url="/permisoDenegado/") 
def razonesHumanitarias_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/razonesHumanitarias.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF derechos y obligaciones y lo guarda en la ubicacion especificada 
def mostrar_derechoObligaciones_pdf(request, extranjero_id):
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)
    nombre_pdf = f"DerechosObligaciones_{extranjero.id}.pdf"

    nombre = extranjero
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre
    
    # Crear el contenido del PDF
    html_context = {'contexto': 'variables',
                     'nombre':nombre,
                     'oficina': oficina,
                     'estacion': estacion
                     }  # Añade las variables que necesitas aquí
    html_content = render_to_string('documentos/derechosObligaciones.html', html_context)
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()

    # Generar la respuesta con el contenido del PDF
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
    
    return response

def guardar_derechoObligaciones_pdf(extranjero_id, usuario):
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)
    nombre_pdf = f"DerechosObligaciones_{extranjero.id}.pdf"
    ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificación")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Derechos y Obligaciones", delaClasificacion=clasificacion)
    estacion = usuario.estancia

    documento_existente = Repositorio.objects.filter(delTipo=tipo_doc, delaEstacion=estacion, nup=ultimo_no_proceso).first()

    if not documento_existente:
        html_context = {'contexto': 'variables'}
        html_content = render_to_string('documentos/derechosObligaciones.html', html_context)
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()
        nombre_completo = usuario.get_full_name()
        repo = Repositorio(
                    nup=ultimo_no_proceso,
                    delTipo=tipo_doc,
                    delaEstacion=estacion,
                    delResponsable=nombre_completo,
                )
        repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
        repo.save()
        
# ----- Genera el documento PDF derechos y obligaciones
def derechoObligaciones_pdf(request, extranjero_id):
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)
    nombre_pdf = f"DerechosObligaciones_{extranjero.id}.pdf"
    ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificación")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Derechos y Obligaciones", delaClasificacion=clasificacion)
    usuario_actual = request.user
    estacion = usuario_actual.estancia


    documento_existente = Repositorio.objects.filter(delTipo=tipo_doc, delaEstacion=estacion, nup=ultimo_no_proceso).first()

    if documento_existente:
        # Si ya existe, simplemente renderizamos el documento guardado
        pdf_bytes = documento_existente.archivo.read()
    else:
        html_context = {'contexto': 'variables'}
        html_content = render_to_string('documentos/derechosObligaciones.html', html_context)
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()
        nombre_completo = usuario_actual.get_full_name()
        repo = Repositorio(
                    nup=ultimo_no_proceso,
                    delTipo=tipo_doc,
                    delaEstacion=estacion,
                    delResponsable=nombre_completo,  # Asignamos el nombre completo
                )
        repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
        repo.save()


    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
    return response

# ----- Genera el documento PDF sin guardarlo en directorio 
def generate_pdfsinguardar(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Obtener el nombre del archivo PDF
    nombre_pdf = f"AcuerdoUno_{extranjero.id}.pdf"

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acuerdoTraslado.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
    
    return response

# ----- Genera el documento PDF de contancia de llamanda sin guardar
def constancia_llamada(request, nup_id, ex_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = Extranjero.objects.get(id=ex_id)
    
    notificacion = Notificacion.objects.get(
        delExtranjero=extranjero,  # Filtrar por el id del extranjero
        nup=no_proceso,
    )

    #consultas
    oficina = extranjero.deLaEstacion.oficina
    estacion = extranjero.deLaEstacion.nombre
    desea = notificacion.deseaLlamar
    motivo = notificacion.motivoNoLlamada
    fecha = notificacion.fechaHoraNotificacion
    firma = extranjero.firma
    firma_url = f"{settings.BASE_URL}{firma.firma_imagen.url}"

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'ex': extranjero,
        'oficina': oficina,
        'estacion': estacion,
        'desea':desea,
        'motivo':motivo, 
        'fecha':fecha,
        'firma':firma_url
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/constanciaLlamada.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF de la constancia de llamada 
# Esta vista no sirce fue reemplazada
@login_required(login_url="/permisoDenegado/")
def constancia_llamada_nofunciona(request, extranjero_id=None):
    
    try:
        extranjero = Extranjero.objects.get(id=extranjero_id)
    except Extranjero.DoesNotExist:
        return HttpResponseNotFound("No se encontró Extranjero con el ID proporcionado.")
    
    try:
        locale.setlocale(locale.LC_TIME, 'es_MX.UTF-8')
    except locale.Error:
        pass  # Ignora el error si la localización no está disponible
    fecha = datetime.now().strftime('%d de %B de %Y')

    notificaciones = Notificacion.objects.filter(delExtranjero=extranjero.id)


    if notificaciones.exists():

        notificacion = notificaciones.latest('nup')
        id = extranjero.pk
        nombre = extranjero.nombreExtranjero
        apellidop = extranjero.apellidoPaternoExtranjero
        apellidom = extranjero.apellidoMaternoExtranjero
        nacionalidad = extranjero.nacionalidad
        deseaLlamar = notificacion.deseaLlamar
        motivo = notificacion.motivoNoLlamada
        fecha = notificacion.fechaHoraNotificacion
        firma = extranjero.firma
        firma_url = f"{settings.BASE_URL}{extranjero.firma.firma_imagen.url}"
        nombre_pdf = f"Constancia_llamadas.pdf"
        oficina = extranjero.deLaEstacion.oficina
        estacion = extranjero.deLaEstacion.nombre
        
        html_context = {
            'id':id,
            'fecha': fecha,
            'motivo': motivo,
            'desea': deseaLlamar,
            'contexto': 'variables',
            'nombre': nombre,
            'apellidop': apellidop,
            'apellidom': apellidom,
            'nacionalidad': nacionalidad,
            'fecha': fecha,
            'firma':firma_url,
            'oficina': oficina,
            'estacion': estacion
        }
        
        html_content = render_to_string('documentos/constanciaLlamada.html', html_context)
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()

        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificación")
        tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="ConstanciaLlamada", delaClasificacion=clasificacion)
        usuario_actual = request.user
        estacion = usuario_actual.estancia
        nombre_completo = usuario_actual.get_full_name()

        repo = Repositorio(
                nup=ultimo_no_proceso,
                delTipo=tipo_doc,
                delaEstacion=estacion,
                delResponsable=nombre_completo,  # Asignamos el nombre completo
            )
        repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
        repo.save()
        # Si se ha proporcionado un request, devolver una respuesta HTTP
        if request:
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
            return response



    
def mostrar_comparecencia_pdf(request, comparecencia_id):
    try:
        comparecencia = Comparecencia.objects.get(id=comparecencia_id)
    except Comparecencia.DoesNotExist:
        return HttpResponseNotFound("No se encontró Comparecencia con el ID proporcionado.")

    # Obtener la instancia de FirmaComparecencia asociada
    firma = FirmaComparecencia.objects.filter(comparecencia=comparecencia).first()
   # Construir la URL completa para la imagen de la firma
    firma_urls = {
        'firma_autoridad_actuante_url': request.build_absolute_uri(firma.firmaAutoridadActuante.url) if firma and firma.firmaAutoridadActuante else None,
        'firma_representante_legal_url': request.build_absolute_uri(firma.firmaRepresentanteLegal.url) if firma and firma.firmaRepresentanteLegal else None,
        'firma_traductor_url': request.build_absolute_uri(firma.firmaTraductor.url) if firma and firma.firmaTraductor else None,
        'firma_extranjero_url': request.build_absolute_uri(firma.firmaExtranjero.url) if firma and firma.firmaExtranjero else None,
        'firma_testigo1_url': request.build_absolute_uri(firma.firmaTestigo1.url) if firma and firma.firmaTestigo1 else None,
        'firma_testigo2_url': request.build_absolute_uri(firma.firmaTestigo2.url) if firma and firma.firmaTestigo2 else None,
    }
    context = {
        'comparecencia': comparecencia,
        'firma': firma,
        **firma_urls,

    }

    template = get_template('documentos/comparecencia_guardar.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()

    nombre_pdf = f"Comparecencia_{comparecencia_id}.pdf"
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
    return response

def comparecencia_pdf(request):
    if request.method == 'POST':
        nup = request.POST.get('nup', '')
        autoridad_actuante_id = request.POST.get('autoridadActuante', '')
        traductor_id = request.POST.get('traductor', '')

        autoridad_actuante = None
        if autoridad_actuante_id:
            autoridad_actuante = get_object_or_404(AutoridadesActuantes, pk=autoridad_actuante_id)

        traductor = None
        if traductor_id:
            traductor = get_object_or_404(Traductores, pk=traductor_id)

        no_proceso = get_object_or_404(NoProceso, nup=nup)
        extranjero = no_proceso.extranjero
        estado_civil = request.POST.get('estadoCivil', '')
        escolaridad = request.POST.get('escolaridad', '')
        ocupacion = request.POST.get('ocupacion', '')
        nacionalidad = request.POST.get('nacionalidad', '')
        domicilio_pais = request.POST.get('DomicilioPais', '')
        lugar_origen = request.POST.get('lugarOrigen', '')
        domicilio_mexico = request.POST.get('domicilioEnMexico', '')
        representante_legal_id = request.POST.get('representanteLegal', '')

        representante_legal = None
        if representante_legal_id:
            representante_legal = get_object_or_404(RepresentantesLegales, pk=representante_legal_id)
            
        cedula_representante_legal= request.POST.get('cedulaRepresentanteLegal','')
        narrativa= request.POST.get('declaracion','')
        autoridad= request.POST.get('autoridadActuante','')
        testigo1= request.POST.get('testigo1','')
        testigo2= request.POST.get('testigo2','')
        context = {
            'nup': nup,
            'extranjero': extranjero,  # Agregando el objeto extranjero al contexto
            'estado_civil': estado_civil,
            'escolaridad': escolaridad,
            'ocupacion': ocupacion,
            'nacionalidad': nacionalidad,
            'domicilio_pais': domicilio_pais,
            'lugar_origen': lugar_origen,
            'domicilio_mexico': domicilio_mexico,
            'representante_legal':representante_legal,
            'cedula_representante_legal':cedula_representante_legal,
            'narrativa':narrativa,
            'autoridad':autoridad,
            'testigo1':testigo1,
            'testigo2':testigo2,
            'traductor':traductor,
            'autoridad_actuante': autoridad_actuante,  # Agregando el objeto AutoridadesActuantes al contexto
            'traductor':traductor,
            'representante_legal': representante_legal,

        }

        template = get_template('documentos/comparecencia.html')
        html_content = template.render(context)
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()

        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="comparecencia.pdf"'
        return response
    else:
       
        pass


def obtener_datos_comparecencia(comparecencia_id):
    try:
        comparecencia = Comparecencia.objects.get(id=comparecencia_id)
        firma = FirmaComparecencia.objects.filter(comparecencia=comparecencia).first()
        return comparecencia, firma
    except Comparecencia.DoesNotExist:
        return None, None

def renderizar_pdf_comparecencia(context):
    template = get_template('documentos/comparecencia_guardar.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    return html.write_pdf()

def guardar_pdf_repositorio(pdf_bytes, comparecencia, usuario_actual):
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Acuerdos Inicio")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Comparecencia", delaClasificacion=clasificacion)
    nombre_pdf = f"Comparecencia_{comparecencia.id}.pdf"
    no_proceso = comparecencia.nup
    no_proceso.comparecencia = True
    no_proceso.save()
       
    repo = Repositorio(
        nup=comparecencia.nup,
        delTipo=tipo_doc,
        delaEstacion=usuario_actual.estancia,
        delResponsable=usuario_actual.get_full_name(),
    )
    repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
    repo.save()
    return repo 


def guardar_comparecencia(request, comparecencia_id):
    comparecencia, firma = obtener_datos_comparecencia(comparecencia_id)
    if not comparecencia:
        return JsonResponse({'status': 'error', 'message': 'Comparecencia no encontrada.'}, status=404)

    try:
        # Preparar contexto con las URLs de las firmas y otros datos necesarios
        firma_urls = {
            'firma_autoridad_actuante_url': request.build_absolute_uri(firma.firmaAutoridadActuante.url) if firma and firma.firmaAutoridadActuante else None,
            'firma_representante_legal_url': request.build_absolute_uri(firma.firmaRepresentanteLegal.url) if firma and firma.firmaRepresentanteLegal else None,
            'firma_traductor_url': request.build_absolute_uri(firma.firmaTraductor.url) if firma and firma.firmaTraductor else None,
            'firma_extranjero_url': request.build_absolute_uri(firma.firmaExtranjero.url) if firma and firma.firmaExtranjero else None,
            'firma_testigo1_url': request.build_absolute_uri(firma.firmaTestigo1.url) if firma and firma.firmaTestigo1 else None,
            'firma_testigo2_url': request.build_absolute_uri(firma.firmaTestigo2.url) if firma and firma.firmaTestigo2 else None
        }
        context = {
            'comparecencia': comparecencia,
            'firma': firma,
            **firma_urls,
        }

        pdf_bytes = renderizar_pdf_comparecencia(context)
        guardar_pdf_repositorio(pdf_bytes, comparecencia, request.user)
        repo = guardar_pdf_repositorio(pdf_bytes, comparecencia, request.user)

        pdf_url = request.build_absolute_uri(repo.archivo.url)
        if 'comparecencia_id' in request.session:
            del request.session['comparecencia_id']

        return JsonResponse({
            'status': 'success',
            'message': 'Comparecencia guardada con éxito y disponible para visualización.',
            'pdf_url': pdf_url  # Envía la URL del PDF en la respuesta

        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'}, status=500)

class lisExtranjerosInicio(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjerosInicio.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')
            TipoAcuerdo.objects.get_or_create(tipo="Acuerdo Inicio")

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
  # Crear una lista de los últimos nup para todos los Extranjeros en el queryset
            listado_nup = [obj.nup for obj in context['object_list']]

            # Verificar qué NoProceso tienen un "Acuerdo Inicio" en el modelo Acuerdo
            acuerdo_inicio_exists = Acuerdo.objects.filter(
                nup__in=listado_nup,
                delAcuerdo__tipo="Acuerdo Inicio"
            ).values_list('nup', flat=True)

            context['acuerdos_inicio'] = set(acuerdo_inicio_exists)
            context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
            context['seccion'] = 'inicio'
            context['navbar1'] = 'inicio'  # Cambia esto según la página activa

            context['seccion1'] = 'inicio'

            return context
    
class AcuerdoInicioCreateView(CreateView):
    model = Acuerdo
    form_class = AcuerdoInicioForm
    template_name = 'modals/crearAcuerdoInicio.html'  # Debes especificar la ubicación del template que usarás.

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extranjero'] = Extranjero.objects.get(numeroExtranjero=self.kwargs['proceso_id'])
        return context

    def form_valid(self, form):
        # Aquí puedes hacer ajustes antes de guardar el objeto, como llenar campos adicionales.
        # Por ejemplo:
        acuerdo, _ = TipoAcuerdo.objects.get_or_create(tipo="Acuerdo Inicio")
        form.instance.delAcuerdo = acuerdo

        noproceso = NoProceso.objects.get(nup=self.kwargs['proceso_id'])
        form.instance.delExtanjero = noproceso.extranjero
        form.instance.nup = noproceso  # <- Asegúrate de asignar el NoProceso al Acuerdo

        # Continúa con el proceso normal de guardado.
        return super().form_valid(form)

    def get_success_url(self):
        # Puedes redirigir al usuario a donde quieras después de guardar el objeto.
        # Por ejemplo, de vuelta a la página de detalles del extranjero:
        return reverse('lisExtranjerosInicio')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sign_link = "https://tu_dominio.com/firmar?token=token_unico" # Cambia tu_dominio y token_unico por lo que necesites
        
        # Crear QR
        img = qrcode.make(sign_link)
        buf = BytesIO()
        img.save(buf, format="PNG")
        image_stream = base64.b64encode(buf.getvalue()).decode()

        # Pasar QR como dato en base64 a la plantilla
        context['qr_code'] = image_stream
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['seccion'] = 'inicio'
        context['navbar1'] = 'inicio'  # Cambia esto según la página activa

        context['seccion1'] = 'inicio'

        return context
    
def registro_acuerdo_inicio(request, proceso_id):
    # Obtener el NoProceso usando proceso_id
    try:
        noproceso = NoProceso.objects.get(nup=proceso_id)
    except NoProceso.DoesNotExist:
        return JsonResponse({'status':'ERROR', 'message':'NoProceso no encontrado'}, status=404)
    
    if request.method == 'POST':
        step = request.POST.get('step')

        if step == '1':
            form_acuerdo_inicio = AcuerdoInicioForm(request.POST)
            if form_acuerdo_inicio.is_valid():
                # Establecer campos por defecto antes de guardar
                acuerdo = form_acuerdo_inicio.save(commit=False) # No guardar todavía
                acuerdo_tipo, _ = TipoAcuerdo.objects.get_or_create(tipo="Acuerdo Inicio")
                acuerdo.delAcuerdo = acuerdo_tipo
                acuerdo.delExtanjero = noproceso.extranjero
                acuerdo.nup = noproceso
                acuerdo.save()  # Ahora guardar

                return JsonResponse({'status':'OK', 'acuerdo_id':acuerdo.id})
            else:
                errors = form_acuerdo_inicio.errors.as_json()
                return JsonResponse({'status':'ERROR', 'errors':errors}, status=400)

    else:
        form_acuerdo_inicio = AcuerdoInicioForm()
    return render(request, "modals/crearAcuerdoInicio.html", {'form_acuerdo': form_acuerdo_inicio, 'proceso_id': proceso_id})

def generar_qr_acuerdos(request, acuerdo_id, testigo):
    base_url = settings.BASE_URL

    if testigo == "testigo_uno":
        url = f"{base_url}acuerdos/firma_testigo_uno/{acuerdo_id}/"
    elif testigo == "testigo_dos":
        url = f"{base_url}acuerdos/firma_testigo_dos/{acuerdo_id}/"
    else:
        return HttpResponseBadRequest("Testigo no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

class FirmaTestigoUnoCreateView(CreateView):
    model = FirmaAcuerdo
    form_class = FirmaTestigoUnoForm
    template_name = 'firma/firma_testigo_uno_create.html'
    success_url = reverse_lazy('firma_exitosa')  # Cambia 'some_success_url' al URL de éxito que desees

    def form_valid(self, form):
        acuerdo_id = self.kwargs.get('acuerdo_id')
        acuerdo = get_object_or_404(Acuerdo, pk=acuerdo_id)
        
        # Asociar el acuerdo con la firma
        form.instance.acuerdo = acuerdo
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acuerdo_id'] = self.kwargs.get('acuerdo_id')
        return context

class FirmaTestigoDosCreateView(CreateView):
    model = FirmaAcuerdo
    form_class = FirmaTestigoDosForm
    template_name = 'firma/firma_testigo_dos_create.html'
    success_url = reverse_lazy('firma_exitosa')  # Cambia al URL de éxito que desees

    def form_valid(self, form):
        acuerdo_id = self.kwargs.get('acuerdo_id')
        acuerdo = get_object_or_404(Acuerdo, pk=acuerdo_id)
        
        # Asociar el acuerdo con la firma
        form.instance.acuerdo = acuerdo
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['acuerdo_id'] = self.kwargs.get('acuerdo_id')
        return context
    
def firma_testigo_uno(request, acuerdo_id):
    acuerdo = get_object_or_404(Acuerdo, pk=acuerdo_id)
    
    if request.method == 'POST':
        form = FirmaTestigoUnoForm(request.POST, request.FILES)
        if form.is_valid():
            # Verifica si ya existe una FirmaAcuerdo para este acuerdo
            firma, created = FirmaAcuerdo.objects.get_or_create(acuerdo=acuerdo)

            # Procesar la firma en base64
            data_url = form.cleaned_data['firmaTestigoUno']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaTestigoUno_{acuerdo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTestigoUno.save(file_name, file, save=True)
            
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigoUnoForm()

    return render(request, 'firma/firma_testigo_uno_create.html', {'form': form, 'acuerdo_id': acuerdo_id})

def firma_testigo_dos(request, acuerdo_id):
    acuerdo = get_object_or_404(Acuerdo, pk=acuerdo_id)
    
    if request.method == 'POST':
        form = FirmaTestigoDosForm(request.POST, request.FILES)
        if form.is_valid():
            # Verifica si ya existe una FirmaAcuerdo para este acuerdo
            firma, created = FirmaAcuerdo.objects.get_or_create(acuerdo=acuerdo)

            # Procesar la firma en base64
            data_url = form.cleaned_data['firmaTestigoDos']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaTestigoDos_{acuerdo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTestigoDos.save(file_name, file, save=True)
            
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigoDosForm()

    return render(request, 'firma/firma_testigo_dos_create.html', {'form': form, 'acuerdo_id': acuerdo_id})
@csrf_exempt
def check_firma_testigo_uno(request, acuerdo_id):
    firmas = FirmaAcuerdo.objects.filter(acuerdo_id=acuerdo_id)
    for firma in firmas:
        if firma.firmaTestigoUno:
            # Obtener la URL de la imagen
            image_url = request.build_absolute_uri(firma.firmaTestigoUno.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo Uno encontrada',
                'image_url': image_url
            })
    
    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo Uno aún no registrada'}, status=404)

@csrf_exempt
def check_firma_testigo_dos(request, acuerdo_id):
    firmas = FirmaAcuerdo.objects.filter(acuerdo_id=acuerdo_id)
    for firma in firmas:
        if firma.firmaTestigoDos:
            # Obtener la URL de la imagen
            image_url = request.build_absolute_uri(firma.firmaTestigoDos.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo Dos encontrada',
                'image_url': image_url
            })
    
    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo Dos aún no registrada'}, status=404)
class lisExtranjerosComparecencia(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjerosComparecencia.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['seccion'] = 'inicio'
        context['navbar1'] = 'inicio'  # Cambia esto según la página activa

        context['seccion1'] = 'comparecencia'
        return context
    

class lisExtranjerosPresentacion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjerosPresentacion.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'inicio'  # Cambia esto según la página activa

        context['seccion'] = 'inicio'
        context['seccion1'] = 'presentacion'
        return context
    
# lista de extranjeros de especiales
class listExtranjerosAcumulacion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosAcumulacion.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'acumulacion'
        return context

class listExtranjerosConclusion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosConclusion.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'conclusion'
        return context

class listExtranjerosTraslado(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosTraslado.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'traslado'
        return context
    
class listExtranjerosSeparacion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosSeparacion.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'separacion'
        return context
    
class listExtranjerosRadicacion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosRadicacion.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['seccion'] = 'especiales'
        context['seccion1'] = 'radicacion'
        return context
    
class listExtranjerosRecepcion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosRecepcion.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'recepcion'
        return context
    
class listExtranjerosArticulo(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosArticulo.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'resoluciones'  # Cambia esto según la página activa

        context['seccion'] = 'resoluciones'
        context['seccion1'] = 'articulo'
        return context
    
class listExtranjerosComar(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosComar.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'resoluciones'  # Cambia esto según la página activa

        context['seccion'] = 'resoluciones'
        context['seccion1'] = 'comar'
        return context
    
class listExtranjerosDeportacion(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosDeportacion.html'
    context_object_name = "extranjeros"
    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'resoluciones'  # Cambia esto según la página activa

        context['seccion'] = 'resoluciones'
        context['seccion1'] = 'deportacion'
        return context
    
class listExtranjerosLibre(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosLibre.html'
    context_object_name = "extranjeros"
    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'resoluciones'  # Cambia esto según la página activa

        context['seccion'] = 'resoluciones'
        context['seccion1'] = 'libre'
        return context
    
class listExtranjerosRetorno(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosRetorno.html'
    context_object_name = "extranjeros"
    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'resoluciones'  # Cambia esto según la página activa

        context['seccion'] = 'resoluciones'
        context['seccion1'] = 'retorno'
        return context
    


# ----- Vista de Prueba para visualizar las plantillas en html -----
def homeAcuerdo(request):
    return render(request,"documentos/Derechos.html")

# ----- Vista de prueba para visualizar los pdf -----
def pdf(request):
    # Tu lógica para obtener los datos y generar el contexto
    context = {
        # ...
    }
    
    # Renderiza la plantilla HTML
    html_template = get_template('documentos/notificacionFiscalia.html')
    html_string = html_template.render(context)
    
    # Convierte la plantilla HTML a PDF con WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="docPrueba.pdf"'
    
    html = HTML(string=html_string)
    html.write_pdf(response)
    
    return response

# ----- Lista Extranjeros para ver o generar Acuerdo de Inicio -----
class acuerdo_inicio(LoginRequiredMixin,ListView):
    template_name = 'acuerdoInicio.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get(self, request):
        extranjeros = Extranjero.objects.filter(estatus='Activo')
        # extranjeros = Extranjero.objects.all() # Obtiene todos los extranjeros 
        
        # Calcular si el PDF existe para cada extranjero
        pdf_existencia = [(extranjero, pdf_exist(extranjero.id)) for extranjero in extranjeros]

        # Ordenar la lista en función de pdf_exists (False primero)
        extranjeros_ordenados = sorted(pdf_existencia, key=lambda x: x[1])

        context = {
            'navbar': 'acuerdos', # Sección de acuerdos 
            'seccion': 'presentacion', # Sección de Inicio de acuerdos
            'acuerdo': 'inicio',
            'extranjeros': [extranjero for extranjero, _ in extranjeros_ordenados],
            'extranjeros_pdf': pdf_existencia
            }
        return render(request, self.template_name, context)

class listRepositorio(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjeros.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            # Obtener la estación del usuario y el estado
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            # Filtrar extranjeros por estación y estado
            extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
            if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
            elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
            ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

            extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context

class DocumentosListView(LoginRequiredMixin,ListView):
    model = Documentos
    template_name = 'verAllAcuerdos.html'  # El nombre de tu template para mostrar los documentos
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        nup_value = self.kwargs.get('nup')
        return Documentos.objects.filter(nup__nup=nup_value)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context
        
class RepositorioListView(LoginRequiredMixin,ListView):
    model = Repositorio
    template_name = 'verAllAcuerdos.html'  # El nombre de tu template para mostrar los documentos
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        nup_value = self.kwargs.get('nup')
        return Repositorio.objects.filter(nup__nup=nup_value)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nup_value = self.kwargs.get('nup')
            
        try:
            no_proceso_instance = NoProceso.objects.get(nup=nup_value)
            apellido_materno = no_proceso_instance.extranjero.apellidoMaternoExtranjero
            if apellido_materno:  # Si hay apellido materno
                extranjero_name = f"{no_proceso_instance.extranjero.nombreExtranjero} {no_proceso_instance.extranjero.apellidoPaternoExtranjero} {apellido_materno}"
            else:  # Si no hay apellido materno
                extranjero_name = f"{no_proceso_instance.extranjero.nombreExtranjero} {no_proceso_instance.extranjero.apellidoPaternoExtranjero}"
            
            context['nombre_extranjero'] = extranjero_name
        except NoProceso.DoesNotExist:
            context['nombre_extranjero'] = "Desconocido"
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context


def servir_pdf(request, repositorio_id):
    try:
        repo = Repositorio.objects.get(id=repositorio_id)
        file_path = repo.archivo.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404
    except Repositorio.DoesNotExist:
        raise Http404
    
# ----- Comprueba si el acuerdo de inicio existe en la carpeta 
def pdf_exist(extranjero_id):
    nombre_pdf = f"AcuerdoInicio_{extranjero_id}.pdf"
    ubicacion_pdf = os.path.join("pame/media/files", nombre_pdf)
    exists = os.path.exists(ubicacion_pdf)

    return exists

# ----- Funcion para cambiar los numeros del dia a palabra
def numero_a_palabra(numero):
    palabras = [
        'cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez',
        'once', 'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve',
        'veinte', 'veintiuno', 'veintidós', 'veintitrés', 'veinticuatro', 'veinticinco', 'veintiséis',
        'veintisiete', 'veintiocho', 'veintinueve', 'treinta', 'treinta y uno'
    ]
    return palabras[numero]

# ----- Funcion para cambiar de numero a palabra los meses
def mes_a_palabra(mes):
    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]
    return meses[mes - 1]  # Restamos 1 porque los meses se cuentan desde 1 enero a 12 diciembre 

# ----- Genera el documento PDF acuerdo de inicio y lo guarda en la ubicacion especificada 
def acuerdoInicio_pdf(request, nup_id):
    no_proceso = NoProceso.objects.get(nup=nup_id)
    extranjero = no_proceso.extranjero
    acuerdo = get_object_or_404(Acuerdo, nup=no_proceso)  # Aquí pasamos el objeto no_proceso directamente
    nombre = extranjero.nombreExtranjero
    apellidop = extranjero.apellidoPaternoExtranjero
    apellidom = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    nombreac = extranjero.deLaEstacion.responsable.nombre
    apellidopac = extranjero.deLaEstacion.responsable.apellidoPat
    apellidomac = extranjero.deLaEstacion.responsable.apellidoMat
    lugar = extranjero.deLaEstacion.estado
    estacion = extranjero.deLaEstacion.nombre
    dia = extranjero.fechaRegistro.day
    mes = extranjero.fechaRegistro.month
    anio = extranjero.fechaRegistro.year

    dia_texto = numero_a_palabra(dia)
    mes_texto = mes_a_palabra(mes)

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'nombre': nombre,
        'apellidop': apellidop,
        'apellidom': apellidom,
        'nacionalidad': nacionalidad,
        'nombreac' : nombreac,
        'apellidopac': apellidopac,
        'apellidomac': apellidomac,
        'lugar': lugar,
        'estacion' : estacion,
        'dia': dia_texto,
        'mes': mes_texto,
        'anio': anio,
        'acuerdo': acuerdo,

    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acuerdoInicio.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de nombramiento de representante legal
def nombramientoRepresentante_pdf(request):
    # extranjero = Extranjero.objects.get(id=extranjero_id)

    #consultas 

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/nombramientoRepresentante.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF de Lista de llamadas "Constancia de llamadas"
def listaLlamadas_pdf_noSirve(request, extranjero_id):
    extranjero = Extranjero.objects.get(id=extranjero_id)
    llamadas = LlamadasTelefonicas.objects.filter(noExtranjero=extranjero_id)


    #consultas
    nombre = extranjero.nombreExtranjero 
    paterno = extranjero.apellidoPaternoExtranjero
    materno = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    ingreso = extranjero.fechaRegistro
    firma = extranjero.firma

    fechas_llamadas = [llamada.fechaHoraLlamada.strftime('%d/%m/%y') for llamada in llamadas]

    

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
        'nombreEx': nombre,
        'paterno': paterno,
        'materno': materno,
        'nacionalidad': nacionalidad,
        'ingreso': ingreso,
        'fechas_llamadas': fechas_llamadas,
        'firma': firma
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/listaLlamadas.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de comparecencia  


# ----- Genera el documento PDF, de Presentacion   
def presentacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/presentacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Recepcion de documentos
def recepcionDoc_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/recepcionDoc.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de constancia de no firma 
def noFirma_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/noFirma.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de radicacion 
def radicacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/radicacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de separacion de alojados
def separacionAlojados_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/separacionAlojados.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de acumulacion de expedientes
def acumulacionExpedientes_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/acumulacionExpedientes.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de suspension provisional del procedimiento
def suspensionProvisional_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/suspensionProvisional.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de continuacion del procedimiento 
def continuacionProcedimiento_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/continuacionProcedimiento.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de egreso de instalacion migratoria
def egresoInstalacion_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/egresoInstalacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo administrativo
def administrativo_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/administrativo.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo conclusion de procedimiento 
def conclusionProcedimiento_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/conclusionProcedimiento.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de procedimiento administrativo migratorio
def procedimientoAdministrativo_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/procedimientoAdministrativo.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de ampliacion de alojamiento por factor de riesgo
def ampliacionAlojamiento_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/ampliacionAlojamiento.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF, de Acuerdo de notificacion consular
def notificacionConsulado_pdf(request):
    # no_proceso = NoProceso.objects.get(nup=nup_id)
    # extranjero = no_proceso.extranjero
    
    #consultas 
    
    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/notificacionConsular.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response







# -----------------------Seccion de GUARDAR PDF AL REPOSITORIO ----------------------


#------------NOTIFICACION CONSULAR ------------------
def notificacionConsulado_pdf(request):
    # DEFINES LOS GET QUE SE CAPTURAN EN EL FORMS
    delaEstacion = request.POST.get('delaEstacion', '')
    nup = request.POST.get('nup', '')
    numeroOficio = request.POST.get('numeroOficio', '')
    delConsulado = request.POST.get('delConsulado', '')
    accion = request.POST.get('accion', '')
    delaAutoridad = request.POST.get('delaAutoridad', '')


    no_proceso = get_object_or_404(NoProceso, nup=nup)
    extranjero = no_proceso.extranjero
    autoridad_actuante = None
    if delaAutoridad:
        autoridad_actuante = get_object_or_404(AutoridadesActuantes, pk=delaAutoridad)

    consulado = None
    if delConsulado:  
        consulado = get_object_or_404(Consulado, pk=delConsulado)

    context = {
        'consulado': consulado,
        'nup': nup,
        'numeroOficio': numeroOficio,
        'delConsulado': delConsulado,
        'accion': accion,
        'autoridad_actuante': autoridad_actuante,
        'extranjero': extranjero,  # Agregando el objeto extranjero al contexto

    }

    template = get_template('documentos/notificacionConsular.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    return response



def obtener_datos_notificacion_consular(notificacion_consular_id):
    try:
        notificacion_consular = NotificacionConsular.objects.get(id=notificacion_consular_id)
        firma = FirmaNotificacionConsular.objects.filter(notificacionConsular=notificacion_consular).first()
        return notificacion_consular, firma
    except NotificacionConsular.DoesNotExist:
        return None, None
def renderizar_pdf_notificacion_consular(context):
    template = get_template('guardar/notificacionConsularGuardar.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    return html.write_pdf()

def guardar_pdf_notificacion_consular(pdf_bytes, notificacion_consular, usuario_actual):
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificaciones Consulares")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Notificacion Consular", delaClasificacion=clasificacion)
    nombre_pdf = f"Notificacion_Consular_{notificacion_consular.id}.pdf"

    no_proceso = notificacion_consular.nup
    no_proceso.save()

    repo = Repositorio(
        nup=notificacion_consular.nup,
        delTipo=tipo_doc,
        delaEstacion=usuario_actual.estancia,
        delResponsable=usuario_actual.get_full_name(),
    )

    repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
    repo.save()
    return repo 


def guardar_notificacion_consular(request, notificacion_consular_id):
    notificacion_consular, firma = obtener_datos_notificacion_consular(notificacion_consular_id)
    if not notificacion_consular:
        return JsonResponse({'status': 'error', 'message': 'Notificación Consular no encontrada.'}, status=404)

    try:
        # Preparar contexto con las URLs de las firmas y otros datos necesarios
        firma_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url) if firma and firma.firmaAutoridadActuante else None

        context = {
            'notificacion_consular': notificacion_consular,
            'firma': firma,
            'firma_autoridad_actuante_url': firma_url,
            # Añadir más datos al contexto si es necesario
        }

        pdf_bytes = renderizar_pdf_notificacion_consular(context)
        repo = guardar_pdf_notificacion_consular(pdf_bytes, notificacion_consular, request.user)

        pdf_url = request.build_absolute_uri(repo.archivo.url)

 
        return JsonResponse({
            'status': 'success',
            'message': 'Notificación Consular guardada con éxito y disponible para visualización.',
            'pdf_url': pdf_url  # Envía la URL del PDF en la respuesta

        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'}, status=500)
#------------FIN NOTIFICACION CONSULAR ------------------

#------------NOTIFICACION COMAR ------------------
# ----- Genera el documento PDF, de Acuerdo de solicitud de refugio


def solicitudRefugio_pdf(request):
    delaEstacion = request.POST.get('delaEstacion', '')
    nup = request.POST.get('nup', '')
    deComar = request.POST.get('deComar', '')
    numeroOficio = request.POST.get('numeroOficio', '')
    notificacionComar = request.POST.get('notificacionComar', '')
    delaComparecencia = request.POST.get('delaComparecencia', '')
    delaAutoridad = request.POST.get('delaAutoridad', '')
    no_proceso = get_object_or_404(NoProceso, nup=nup)
    extranjero = no_proceso.extranjero
    comparecencias = no_proceso.comparecencias.all()
    comparecencia = comparecencias.last() 

    autoridad_actuante = None
    if delaAutoridad:
        autoridad_actuante = get_object_or_404(AutoridadesActuantes, pk=delaAutoridad)
    puestas = {
        'puesta_imn': extranjero.deLaPuestaIMN,
        'puesta_ac': extranjero.deLaPuestaAC,
        'puesta_vp': extranjero.deLaPuestaVP,
    }
    puestas = {key: val for key, val in puestas.items() if val is not None}
    comar = None
    if deComar:  
        comar = get_object_or_404(Comar, pk=deComar)



    context = {
        'contexto': 'variables',
        'nup': nup,
        'extranjero': extranjero,  # Agregando el objeto extranjero al context
        'autoridad_actuante': autoridad_actuante,
        'comparecencias': comparecencia,  # Agregar comparecencias al contexto
        'puestas': puestas,  # Agregar el diccionario de puestas al contexto
        'deComar': comar,

    }

    template = get_template('documentos/refugioComar.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    return response


def obtener_datos_notificacion_comar(notificacion_comar_id):
    try:
        notificacion_comar = NotificacionCOMAR.objects.get(id=notificacion_comar_id)
        firma = FirmaNotificacionComar.objects.filter(notificacionComar=notificacion_comar).first()
        no_proceso = notificacion_comar.nup
        extranjero = no_proceso.extranjero
        comparecencia = Comparecencia.objects.filter(nup=no_proceso).order_by('-fechahoraComparecencia').first()
        puestas = {
                'puesta_imn': extranjero.deLaPuestaIMN,
                'puesta_ac': extranjero.deLaPuestaAC,
                'puesta_vp': extranjero.deLaPuestaVP,
            }
        puestas = {key: val for key, val in puestas.items() if val is not None}

        return notificacion_comar, firma, extranjero, comparecencia,puestas
    except NotificacionCOMAR.DoesNotExist:
        return None, None
    
def renderizar_pdf_notificacion_comar(context):
    template = get_template('guardar/refugioComarGuardar.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    return html.write_pdf()

def guardar_pdf_notificacion_comar(pdf_bytes, notificacion_comar, usuario_actual):
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificaciones")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Notificacion a COMAR", delaClasificacion=clasificacion)

    # Genera un nombre único para el archivo PDF
    nombre_pdf = f"Notificacion_Consular_{notificacion_comar.id}.pdf"

    # Actualiza información relevante en el modelo NoProceso si es necesario
    no_proceso = notificacion_comar.nup
    # no_proceso.notificacion_consular = True  # Descomenta y ajusta si es necesario
    no_proceso.save()

    # Crea una nueva instancia en el repositorio para el archivo PDF
    repo = Repositorio(
        nup=notificacion_comar.nup,
        delTipo=tipo_doc,
        delaEstacion=usuario_actual.estancia,
        delResponsable=usuario_actual.get_full_name(),
    )

    # Guarda el archivo PDF en el modelo Repositorio
    repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
    repo.save()
    return repo 


def guardar_notificacion_comar(request, notificacion_comar_id):
    notificacion_comar, firma, extranjero, comparecencia, puestas  = obtener_datos_notificacion_comar(notificacion_comar_id)
    if not notificacion_comar:
        return JsonResponse({'status': 'error', 'message': 'Notificación Comar no encontrada.'}, status=404)

    try:
        # Preparar contexto con las URLs de las firmas y otros datos necesarios
        firma_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url) if firma and firma.firmaAutoridadActuante else None

        context = {
            'notificacion_comar': notificacion_comar,
            'firma': firma,
            'firma_autoridad_actuante_url': firma_url,
            'extranjero': extranjero,
            'comparecencia': comparecencia,
            'puestas': puestas,
            # Añadir más datos al contexto si es necesario
        }


        pdf_bytes = renderizar_pdf_notificacion_comar(context)
        repo = guardar_pdf_notificacion_comar(pdf_bytes, notificacion_comar, request.user)

        pdf_url = request.build_absolute_uri(repo.archivo.url)

 
        return JsonResponse({
            'status': 'success',
            'message': 'Notificación Comar guardada con éxito y disponible para visualización.',
            'pdf_url': pdf_url  # Envía la URL del PDF en la respuesta

        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'}, status=500)
    
#--- FIN DE NOTIFICACION COMAR

#------- INICIO NOTIFICACION FISCALIA
def notificacionFiscalia_pdf(request):
    numeroOficio = request.POST.get('numeroOficio', '')
    delaFiscalia = request.POST.get('delaFiscalia', '')
    delaAutoridad = request.POST.get('delaAutoridad', '')
    condicion = request.POST.get('condicion', '')
    delaEstacion = request.POST.get('delaEstacion', '')
    nup = request.POST.get('nup', '')
    delaComparecencia = request.POST.get('delaComparecencia', '')
    no_proceso = get_object_or_404(NoProceso, nup=nup)
    extranjero = no_proceso.extranjero
    comparecencias = no_proceso.comparecencias.all()
    comparecencia = comparecencias.last() 

    
    autoridad_actuante = None
    if delaAutoridad:
        autoridad_actuante = get_object_or_404(AutoridadesActuantes, pk=delaAutoridad)
    
    fiscalia = None
    if delaFiscalia:  
        fiscalia = get_object_or_404(Fiscalia, pk=delaFiscalia)
    context = {
        'contexto': 'variables',
        'nup': nup,
        'extranjero': extranjero,  # Agregando el objeto extranjero al context
        'autoridad_actuante': autoridad_actuante,
        'comparecencias': comparecencia,  
        'fiscalia': fiscalia,
        'condicion':condicion,

    }
    template = get_template('documentos/notificacionFiscalia.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    pdf_bytes = html.write_pdf()
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    return response


def obtener_datos_notificacion_fiscalia(notificacion_fiscalia_id):
    try:
        notificacion_fiscalia = NotificacionFiscalia.objects.get(id=notificacion_fiscalia_id)
        firma = FirmaNotificacionFiscalia.objects.filter(notificacionFiscalia=notificacion_fiscalia).first()
        return notificacion_fiscalia, firma
    except NotificacionFiscalia.DoesNotExist:
        return None, None
    
def renderizar_pdf_notificacion_fiscalia(context):
    template = get_template('guardar/notificacionFiscaliaGuardar.html')
    html_content = template.render(context)
    html = HTML(string=html_content)
    return html.write_pdf()

def guardar_pdf_notificacion_fiscalia(pdf_bytes, notificacion_fiscalia, usuario_actual):
    clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Notificaciones")
    tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Notificacion a Fiscalia", delaClasificacion=clasificacion)

    # Genera un nombre único para el archivo PDF
    nombre_pdf = f"Notificacion_Fiscalia_{notificacion_fiscalia.id}.pdf"

    # Actualiza información relevante en el modelo NoProceso si es necesario
    no_proceso = notificacion_fiscalia.nup
    # no_proceso.notificacion_consular = True  # Descomenta y ajusta si es necesario
    no_proceso.save()

    # Crea una nueva instancia en el repositorio para el archivo PDF
    repo = Repositorio(
        nup=notificacion_fiscalia.nup,
        delTipo=tipo_doc,
        delaEstacion=usuario_actual.estancia,
        delResponsable=usuario_actual.get_full_name(),
    )

    # Guarda el archivo PDF en el modelo Repositorio
    repo.archivo.save(nombre_pdf, ContentFile(pdf_bytes))
    repo.save()
    return repo 


def guardar_notificacion_fiscalia(request, notificacion_fiscalia_id):
    notificacion_fiscalia, firma = obtener_datos_notificacion_fiscalia(notificacion_fiscalia_id)
    if not notificacion_fiscalia:
        return JsonResponse({'status': 'error', 'message': 'Notificación Fiscalia no encontrada.'}, status=404)

    try:
        # Preparar contexto con las URLs de las firmas y otros datos necesarios
        firma_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url) if firma and firma.firmaAutoridadActuante else None

        context = {
            'notificacion_fiscalia': notificacion_fiscalia,
            'firma': firma,
            'firma_autoridad_actuante_url': firma_url,
            # Añadir más datos al contexto si es necesario
        }

        pdf_bytes = renderizar_pdf_notificacion_fiscalia(context)
        repo = guardar_pdf_notificacion_fiscalia(pdf_bytes, notificacion_fiscalia, request.user)

        pdf_url = request.build_absolute_uri(repo.archivo.url)

 
        return JsonResponse({
            'status': 'success',
            'message': 'Notificación Fiscalia guardada con éxito y disponible para visualización.',
            'pdf_url': pdf_url  # Envía la URL del PDF en la respuesta

        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Ocurrió un error: {str(e)}'}, status=500)
    
#------ FIN DE NOTIFICACION FISCALIA