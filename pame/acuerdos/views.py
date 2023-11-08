from typing import Any
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vigilancia.models import Extranjero
from django.http import HttpResponse, HttpResponseNotFound
from weasyprint import HTML
from django.template.loader import render_to_string, get_template
from django.views.generic import ListView, CreateView
from vigilancia.models import Extranjero, Firma
import os
from datetime import datetime
import locale
from llamadasTelefonicas.models import Notificacion
from vigilancia.models import NoProceso
from acuerdos.models import Documentos, ClasificaDoc, TiposDoc , Repositorio
from llamadasTelefonicas.models import LlamadasTelefonicas
from pertenencias.models import EnseresBasicos
from django.core.files.base import ContentFile
from django.db.models import OuterRef, Subquery
from django.contrib.auth.decorators import login_required  # Importa el decorador login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Exists, OuterRef
from .models import TipoAcuerdo,Acuerdo
from .forms import AcuerdoInicioForm
from django.shortcuts import redirect
from django.urls import reverse
from io import BytesIO
import base64
import qrcode
from django.http import JsonResponse
from django.views import View
from django.http import HttpResponseBadRequest

from .forms import FirmaTestigoDosForm, FirmaTestigoUnoForm
from .models import FirmaAcuerdo
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.core.files.storage import default_storage
import io

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
    html_template = get_template('documentos/comparecencia.html')
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
def notificacionRepresentacion_pdf(request):
    # extranjero = Extranjero.objects.get(id=extranjero_id)

    #consultas 

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
    }

    # Obtener la plantilla HTML
    template = get_template('documentos/notificacionRepresentacion.html')
    html_content = template.render(context)

    # Crear un objeto HTML a partir de la plantilla HTML
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=""'
    
    return response

# ----- Genera el documento PDF de Inventario de pertenencias y valores
def inventarioPV_pdf(request):
    # extranjero = Extranjero.objects.get(id=extranjero_id)

    #consultas 

    # Definir el contexto de datos para tu plantilla
    context = {
        'contexto': 'variables',
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
def listaLlamadas_pdf(request, extranjero_id):
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
    firma = extranjero.firma

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
        'firma': firma
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

    #consultas 
    nombre = extranjero.nombreExtranjero
    paterno = extranjero.apellidoPaternoExtranjero
    materno = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad.nombre
    ingreso = extranjero.fechaRegistro
    firma = extranjero.firma

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
        'firma': firma,
        'enseres_asignados': enseres_asignados_str,
        'enseres_extras': enseres_extras
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

# ----- Genera el documento PDF derechos y obligaciones y lo guarda en la ubicacion especificada 
def mostrar_derechoObligaciones_pdf(request, extranjero_id):
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)
    nombre_pdf = f"DerechosObligaciones_{extranjero.id}.pdf"
    
    # Crear el contenido del PDF
    html_context = {'contexto': 'variables'}  # Añade las variables que necesitas aquí
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

# ----- Genera el documento PDF de la constancia de llamada 
@login_required(login_url="/permisoDenegado/")
def constancia_llamada(request, extranjero_id=None):
    
    try:
        extranjero = Extranjero.objects.get(id=extranjero_id)
    except Extranjero.DoesNotExist:
        return HttpResponseNotFound("No se encontró Extranjero con el ID proporcionado.")
    
    
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
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
        nombre_pdf = f"Constancia_llamadas.pdf"
        
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
            'firma':firma,
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

# Lista de acuerdo inicio 
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