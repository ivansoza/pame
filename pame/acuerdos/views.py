from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vigilancia.models import Extranjero
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string

def homeAcuerdoInicio(request):
    return render(request,"homeAcuerdoInicio.html")

def generate_pdf(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Obtener el objeto Traslado 
    # traslado = ExtranjeroTraslado.objects.filter(delExtranjero=extranjero).first()

    # Definir el mapeo de los nombres de los meses en español
    nombres_meses_espanol = {
        'January': 'enero',
        'February': 'febrero',
        'March': 'marzo',
        'April': 'abril',
        'May': 'mayo',
        'June': 'junio',
        'July': 'julio',
        'August': 'agosto',
        'September': 'septiembre',
        'October': 'octubre',
        'November': 'noviembre',
        'December': 'diciembre',
    }

    # OBtener datos a renderizar 
    nombre_extranjero = extranjero.nombreExtranjero
    apellidop_extranjero = extranjero.apellidoPaternoExtranjero
    apellidom_extranjero = extranjero.apellidoMaternoExtranjero
    nacionalidad = extranjero.nacionalidad
    nombre_estacion = extranjero.deLaEstacion.nombre
    estado_estacion = extranjero.deLaEstacion.estado
    calle = extranjero.deLaEstacion.calle
    noExt = extranjero.deLaEstacion.noext
    # hora = traslado.delTraslado.fechaSolicitud
    # dia = traslado.delTraslado.fechaSolicitud.strftime('%d')
    # mes = traslado.delTraslado.fechaSolicitud.strftime('%B')
    # mes_espanol = nombres_meses_espanol.get(mes, mes)
    # anio = traslado.delTraslado.fechaSolicitud.strftime('%Y')

    html_context = {
        'contexto': 'variables',
        'nombre_extranjero': nombre_extranjero,
        'apellidop': apellidop_extranjero,
        'apellidom': apellidom_extranjero,
        'nacionalidad': nacionalidad,
        'nombre_estacion': nombre_estacion,
        'estado_estacion': estado_estacion,
        'calle': calle,
        'noExt': noExt,
        # 'hora': hora,
        # 'dia': dia,
        # 'mes': mes_espanol,
        # 'anio': anio,
    }

    # Crear un objeto HTML a partir de una plantilla o contenido HTML
    html_content = render_to_string('documentos/acuerdoTraslado.html', html_context)
    html = HTML(string=html_content)

    # Generar el PDF
    pdf_bytes = html.write_pdf()

    # Devolver el PDF como una respuesta HTTP
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Acuerdo de Traslado {{nombre_extranjero}}.pdf"'
    return response