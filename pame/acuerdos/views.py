from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vigilancia.models import Extranjero
from django.http import HttpResponse, FileResponse
from weasyprint import HTML
from django.template.loader import render_to_string, get_template
from django.views.generic import ListView
from vigilancia.models import Extranjero
import os
from operator import itemgetter
from datetime import datetime
import locale
from llamadasTelefonicas.models import Notificacion
from vigilancia.models import NoProceso
from acuerdos.models import Documentos
from django.core.files.base import ContentFile


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
    html_template = get_template('documentos/derechosObligaciones.html')
    html_string = html_template.render(context)
    
    # Convierte la plantilla HTML a PDF con WeasyPrint
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="docPrueba.pdf"'
    
    html = HTML(string=html_string)
    html.write_pdf(response)
    
    return response

# ----- Lista Extranjeros para ver o generar Acuerdo de Inicio -----
class acuerdo_inicio(ListView):
    template_name = 'acuerdoInicio.html'

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

# ----- Comprueba si el acuerdo de inicio existe en la carpeta 
def pdf_exist(extranjero_id):
    nombre_pdf = f"AcuerdoInicio_{extranjero_id}.pdf"
    ubicacion_pdf = os.path.join("pame/media/files", nombre_pdf)
    exists = os.path.exists(ubicacion_pdf)
    # print(f"PDF para extranjero {extranjero_id}: {exists}")
    # print(f"Ruta del archivo PDF para extranjero {extranjero_id}: {ubicacion_pdf}")
    return exists

# ----- Genera el documento PDF acuerdo de inicio y lo guarda en la ubicacion especificada 
def acuerdoInicio_pdf(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Obtener el nombre del archivo PDF
    nombre_pdf = f"AcuerdoInicio_{extranjero.id}.pdf"
    ubicacion_pdf = os.path.abspath(os.path.join("pame/media/files", nombre_pdf))

    # Verificar si el archivo PDF ya existe en la ubicación
    if not os.path.exists(ubicacion_pdf):
        # Si el archivo no existe, procede a generarlo y guardarlo
        html_context = {
            'contexto': 'variables',
        }

        # Crear un objeto HTML a partir de una plantilla o contenido HTML
        html_content = render_to_string('documentos/acuerdoInicio.html', html_context)
        html = HTML(string=html_content)

        # Generar el PDF
        pdf_bytes = html.write_pdf()

        # Guardar el PDF en el Servidor
        with open(ubicacion_pdf, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)

    # Devolver el PDF como una respuesta HTTP directamente desde los bytes generados
    response = FileResponse(open(ubicacion_pdf, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
    return response

# ----- Genera el documento PDF derechos y obligaciones y lo guarda en la ubicacion especificada 
def derechoObligaciones_pdf(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Obtener el nombre del archivo PDF
    nombre_pdf = f"DerechosObligaciones_{extranjero.id}.pdf"
    ubicacion_pdf = os.path.abspath(os.path.join("pame/media/files", nombre_pdf))

    # Verificar si el archivo PDF ya existe en la ubicación
    if not os.path.exists(ubicacion_pdf):
        # Si el archivo no existe, procede a generarlo y guardarlo
        html_context = {
            'contexto': 'variables',
        }

        # Crear un objeto HTML a partir de una plantilla o contenido HTML
        html_content = render_to_string('documentos/derechosObligaciones.html', html_context)
        html = HTML(string=html_content)

        # Generar el PDF
        pdf_bytes = html.write_pdf()

        # Guardar el PDF en el Servidor
        with open(ubicacion_pdf, "wb") as pdf_file:
            pdf_file.write(pdf_bytes)

    # Devolver el PDF como una respuesta HTTP directamente desde los bytes generados
    response = FileResponse(open(ubicacion_pdf, 'rb'), content_type='application/pdf')
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
def constancia_llamada(request=None, extranjero_id=None):
    print("Iniciando constancia_llamada")
    
    try:
        extranjero = Extranjero.objects.get(id=extranjero_id)
    except Extranjero.DoesNotExist:
        print(f"No se encontró Extranjero con ID {extranjero_id}")
        return HttpResponseNotFound("No se encontró Extranjero con el ID proporcionado.")
    
    print("Extranjero obtenido:", extranjero)
    
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    fecha = datetime.now().strftime('%d de %B de %Y')

    notificaciones = Notificacion.objects.filter(delExtranjero=extranjero.id)
    print("Notificaciones:", notificaciones)

    if notificaciones.exists():
        print("Entrando al bloque de notificaciones existentes")

        notificacion = notificaciones.latest('nup')
        print("Notificacion:", notificacion)

        nombre = extranjero.nombreExtranjero
        apellidop = extranjero.apellidoPaternoExtranjero
        apellidom = extranjero.apellidoMaternoExtranjero
        nacionalidad = extranjero.nacionalidad
        deseaLlamar = notificacion.deseaLlamar
        motivo = notificacion.motivoNoLlamada
        fecha = notificacion.fechaHoraNotificacion
        nombre_pdf = f"Constancia_llamadas.pdf"
        
        html_context = {
            'fecha': fecha,
            'motivo': motivo,
            'desea': deseaLlamar,
            'contexto': 'variables',
            'nombre': nombre,
            'apellidop': apellidop,
            'apellidom': apellidom,
            'nacionalidad': nacionalidad,
            'fecha': fecha,
        }
        
        html_content = render_to_string('documentos/constanciaLlamada.html', html_context)
        html = HTML(string=html_content)
        pdf_bytes = html.write_pdf()

        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        print("Ultimo NoProceso:", ultimo_no_proceso)

        documentos, created = Documentos.objects.get_or_create(nup=ultimo_no_proceso)
        print("Documentos:", documentos, "Creado:", created)

        try:
            # Guarda el archivo PDF en el campo oficio_llamada
            documentos.oficio_llamada.save(nombre_pdf, ContentFile(pdf_bytes))
            documentos.save()
            print("Documento guardado correctamente.")
        except Exception as e:
            print("Error al guardar el documento:", e)

        # Si se ha proporcionado un request, devolver una respuesta HTTP
        if request:
            response = HttpResponse(pdf_bytes, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
            return response
