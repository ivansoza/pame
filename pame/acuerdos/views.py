from typing import Any
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from vigilancia.models import Extranjero
from django.http import HttpResponse, FileResponse
from weasyprint import HTML
from django.template.loader import render_to_string, get_template
from django.views.generic import ListView
from vigilancia.models import Extranjero, Firma
import os
from datetime import datetime
import locale
from llamadasTelefonicas.models import Notificacion
from vigilancia.models import NoProceso
from acuerdos.models import Documentos, ClasificaDoc, TiposDoc , Repositorio
from django.core.files.base import ContentFile
from django.db.models import OuterRef, Subquery


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
    html_template = get_template('documentos/nombramientoDefensor.html')
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



class listRepositorio(ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjeros.html'
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
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context

class DocumentosListView(ListView):
    model = Documentos
    template_name = 'verAllAcuerdos.html'  # El nombre de tu template para mostrar los documentos

    def get_queryset(self):
        nup_value = self.kwargs.get('nup')
        return Documentos.objects.filter(nup__nup=nup_value)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'repositorio'  # Cambia esto según la página activa
        context['seccion'] = 'verrepo'
        return context

        
class RepositorioListView(ListView):
    model = Repositorio
    template_name = 'verAllAcuerdos.html'  # El nombre de tu template para mostrar los documentos

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
    # print(f"PDF para extranjero {extranjero_id}: {exists}")
    # print(f"Ruta del archivo PDF para extranjero {extranjero_id}: {ubicacion_pdf}")
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
def acuerdoInicio_pdf(request, extranjero_id):
    extranjero = Extranjero.objects.get(id=extranjero_id)

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
        'anio': anio
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
def constancia_llamada(request, extranjero_id=None):
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

class lisExtranjerosInicio(ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjerosInicio.html'
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
        context['seccion'] = 'inicio'
        context['navbar1'] = 'inicio'  # Cambia esto según la página activa

        context['seccion1'] = 'inicio'

        return context
    
class lisExtranjerosComparecencia(ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjerosComparecencia.html'
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
        context['seccion'] = 'inicio'
        context['navbar1'] = 'inicio'  # Cambia esto según la página activa

        context['seccion1'] = 'comparecencia'
        return context
    

class lisExtranjerosPresentacion(ListView):

    model = NoProceso
    template_name = 'inicio/listExtranjerosPresentacion.html'
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
        context['navbar1'] = 'inicio'  # Cambia esto según la página activa

        context['seccion'] = 'inicio'
        context['seccion1'] = 'presentacion'
        return context
    


# lista de extranjeros de especiales

class listExtranjerosAcumulacion(ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosAcumulacion.html'
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
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'acumulacion'
        return context

class listExtranjerosConclusion(ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosConclusion.html'
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
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'conclusion'
        return context
    


class listExtranjerosTraslado(ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosTraslado.html'
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
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'traslado'
        return context
    
class listExtranjerosSeparacion(ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosSeparacion.html'
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
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'separacion'
        return context
    
class listExtranjerosRadicacion(ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosRadicacion.html'
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
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['seccion'] = 'especiales'
        context['seccion1'] = 'radicacion'
        return context
    
class listExtranjerosRecepcion(ListView):

    model = NoProceso
    template_name = 'especiales/listExtranjerosRecepcion.html'
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
        context['navbar1'] = 'especiales'  # Cambia esto según la página activa

        context['seccion'] = 'especiales'
        context['seccion1'] = 'recepcion'
        return context
    
class listExtranjerosArticulo(ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosArticulo.html'
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
        context['seccion1'] = 'articulo'
        return context
    
class listExtranjerosComar(ListView):

    model = NoProceso
    template_name = 'resoluciones/listExtranjerosComar.html'
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
        context['seccion1'] = 'comar'
        return context
    

class listExtranjerosDeportacion(ListView):

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
    
class listExtranjerosLibre(ListView):

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
    
class listExtranjerosRetorno(ListView):

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