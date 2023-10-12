from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vigilancia.models import Extranjero
from django.http import HttpResponse, FileResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from django.views.generic import ListView
from vigilancia.models import Extranjero
import os
from operator import itemgetter
from datetime import datetime
import locale
from llamadasTelefonicas.models import Notificacion

def homeAcuerdo(request):
    return render(request,"acuerdoInicio.html")

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
    
def pdf_exist(extranjero_id):
    nombre_pdf = f"AcuerdoUno_{extranjero_id}.pdf"
    ubicacion_pdf = os.path.join("pame/media/files", nombre_pdf)
    exists = os.path.exists(ubicacion_pdf)
    # print(f"PDF para extranjero {extranjero_id}: {exists}")
    # print(f"Ruta del archivo PDF para extranjero {extranjero_id}: {ubicacion_pdf}")
    return exists

def generate_pdf(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Obtener el nombre del archivo PDF
    nombre_pdf = f"AcuerdoUno_{extranjero.id}.pdf"
    ubicacion_pdf = os.path.abspath(os.path.join("pame/media/files", nombre_pdf))

    # Verificar si el archivo PDF ya existe en la ubicación
    if not os.path.exists(ubicacion_pdf):
        # Si el archivo no existe, procede a generarlo y guardarlo
        html_context = {
            'contexto': 'variables',
        }

        # Crear un objeto HTML a partir de una plantilla o contenido HTML
        html_content = render_to_string('documentos/acuerdoTraslado.html', html_context)
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

def constancia_llamada(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    fecha = datetime.now().strftime('%d de %B de %Y')
    notifi = get_object_or_404(Notificacion, delExtranjero=extranjero)

    #Obtener datos a renderizar 
    nombre = extranjero.nombreExtranjero
    apellidop = extranjero.apellidoPaternoExtranjero
    apellidom = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad
    deseaLlamar = notifi.deseaLlamar
    motivo = notifi.motivoNoLlamada
    fecha = notifi.fechaHoraNotificacion
    # Obtener el nombre del archivo PDF
    nombre_pdf = f"Constancia_llamadas_{extranjero.id}.pdf"

    # Crear el objeto HTML a partir de una plantilla o contenido HTML
    html_context = {
        'fecha':fecha,
        'motivo':motivo,
        'desea':deseaLlamar,
        'contexto': 'variables',
        'nombre': nombre,
        'apellidop': apellidop,
        'apellidom': apellidom,
        'nacionalidad': nacionalidad,
        'fecha': fecha,
    }
    html_content = render_to_string('documentos/constanciaLlamada.html', html_context)
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF generado como una respuesta HTTP directamente desde los bytes generados
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{nombre_pdf}"'
    return response
