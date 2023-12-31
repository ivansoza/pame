from django.shortcuts import render
from django.views.generic import CreateView, ListView,DetailView, TemplateView
from .models import Traslado, Extranjero, ExtranjeroTraslado, SolicitudTraslado
from django.views.generic import CreateView, ListView,DetailView, UpdateView, DeleteView, FormView
from .models import Traslado, Extranjero, ExtranjeroTraslado
from vigilancia.models import Estacion
from django.http import JsonResponse
from .forms import TrasladoForm, EstatusTrasladoForm, EstatusTrasladoFormExtranjero, EstatusTrasladoFormOrigen, EstatusTrasladoFormOrigenDestino, DecisionForm,CambioEstacionForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
from django.db.models import Count  # Añade esta línea al principio del archivo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required  # Importa el decorador login_required

from datetime import date




# Create your views here.
class ListTraslado(LoginRequiredMixin,ListView):
    model = Traslado          
    template_name = "origen/listPuestasTraslado.html" 
    context_object_name = 'puestasTraslado'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = Traslado.objects.filter(estacion_origen=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa

        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia

        puestas_count = self.get_queryset().count() 
        context['puestas_count'] = puestas_count

        #extranjeros_total = Extranjero.objects.filter(deLaEstacion=user_estacion).count() #OBTENER EL NUMERO TOTAL DE EXTRANJERO POR LA ESTACION 
        extranjeros_total = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion, estatus='Activo').count()
        context['extranjeros_total'] = extranjeros_total
        nacionalidades_count = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion).values('nacionalidad').distinct().count()
        context['nacionalidades_count'] = nacionalidades_count

        hombres_count = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion, genero=0, estatus='Activo').count()
        mujeres_count = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion, genero=1, estatus='Activo').count()
        context['mujeres_count'] = mujeres_count
        context['hombres_count'] = hombres_count
        capacidad_actual = user_estacion.capacidad
        context['capacidad_actual'] = capacidad_actual

        return context

class estadisticasPuestaINM(LoginRequiredMixin,ListView):
    model=Traslado
    template_name =  "listPuestasTraslado.html" 
    context_object_name = 'puestainm'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = Traslado.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa
        return context
    
class listarEstaciones(LoginRequiredMixin,ListView):
    model = Extranjero
    template_name = "origen/selecEstacion.html"
    context_object_name = 'traslado'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        queryset = Extranjero.objects.filter(deLaEstacion=user_estacion, estatus='Activo')
        return queryset    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        estaciones = Estacion.objects.exclude(pk=user_estacion.pk)
        context['estaciones'] = estaciones
        return context

    def post(self, request, *args, **kwargs):
     


        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            estacion_id = request.POST.get('estacion_id')
            try:
                estacion = Estacion.objects.get(pk=estacion_id)
                # Obtén el nombre del responsable de la estación
                responsable_nombre = f"{estacion.responsable.nombre} {estacion.responsable.apellidoPat} {estacion.responsable.apellidoMat}"
                estado_nombre = estacion.estado.estado  # Accede directamente al nombre del estado
                estancia_nombre = estacion.nombre
                email_nombre = estacion.email
                calle_nombre = estacion.calle
                noext_nombre = estacion.noext
                cp_nombre = estacion.cp
                colonia_nombre = estacion.colonia
                tel_reponsable = estacion.responsable.telefono
                email_responsable = estacion.responsable.email
                return JsonResponse({'capacidad': estacion.capacidad, 
                                     'responsable': responsable_nombre, 
                                     'estado': estado_nombre,
                                     'estancia':estancia_nombre,
                                     'email':email_nombre,
                                     'calle':calle_nombre,
                                     'no':noext_nombre,
                                     'cp':cp_nombre,
                                     'colonia':colonia_nombre,
                                     'telResponsable':tel_reponsable,
                                     'emailResponsable':email_responsable

                                     })
            except Estacion.DoesNotExist:
                return JsonResponse({'capacidad': 'N/A', 
                                     'responsable': 'N/A',
                                     'estado':'N/A',
                                     'estancia':'N/A',
                                     'email':'N/A',
                                     'calle':'N/A',
                                     'no':'N/A',
                                     'cp':'N/A',
                                     'colonia':'N/A',
                                     'telResponsable':'N/A',
                                     'emailResponsable':'N/A'

                                     })
        

        return super().post(request, *args, **kwargs)




class TrasladoCreateView(LoginRequiredMixin,CreateView):
    model = Traslado
    form_class = TrasladoForm
    template_name = 'modal/crearPuestaTraslado.html'  
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_success_url(self):
        destino_id = self.object.estacion_destino_id
        return reverse('traslado', kwargs={'traslado_id': self.object.pk, 'destino_id': destino_id})
    def form_valid(self, form):
        numero_camiones = form.cleaned_data.get('numero_camiones')
        if numero_camiones == 0:
            return self.form_invalid(form)

        origen_id = self.kwargs['origen_id']
        destino_id = self.kwargs['destino_id']
        
        form.instance.estacion_origen_id = origen_id
        form.instance.estacion_destino_id = destino_id

        return super().form_valid(form)
    

    def form_invalid(self, form):
        messages.error(self.request, 'No está permitido elegir 0 camiones para hacer un traslado.')
        return redirect(reverse('listEstaciones'))

    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        nombre_usuario = usuario.get_full_name()
        initial['nombreAutoridadEnvia'] = nombre_usuario

        ultimo_registro = Traslado.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroUnicoProceso.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/TRA/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroUnicoProceso'] = nuevo_numero
        initial['estacion_origen'] = self.kwargs['origen_id']
        initial['estacion_destino'] = self.kwargs['destino_id']
        return initial

class cambiarStatus(LoginRequiredMixin,UpdateView):
    model = Traslado
    form_class = EstatusTrasladoForm
    template_name = 'modal/seleccionarSttausdeTraslado.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def form_valid(self, form):
        # Si el estatus cambió a ACEPTADO
        if 'status' in form.changed_data and form.instance.status == 1: 
            form.instance.fecha_aceptacion = timezone.now()
            form.instance.nombreAutoridadRecibe = self.request.user.get_full_name()

        # Si el estatus cambió a RECHAZADO
        if 'status' in form.changed_data and form.instance.status == 2:  
            form.instance.fecha_rechazo = timezone.now()
            # El motivo_rechazo se capturará directamente desde el formulario
        
        return super(cambiarStatus, self).form_valid(form)

    def get_success_url(self):
        return reverse('traslados_recibidos')
    def get_initial(self):
            initial = super().get_initial()
            
            # Obtener el nombre completo del usuario actual
            nombre_usuario = self.request.user.get_full_name()
            
            # Establecer ese nombre como valor inicial para 'nombreAutoridadRecibe'
            initial['nombreAutoridadRecibe'] = nombre_usuario
            
            return initial
class cambiarStatusOrigen(LoginRequiredMixin,UpdateView):
    model = Traslado
    form_class = EstatusTrasladoFormOrigen
    template_name = 'modal/seleccionarStatusTrasladoOrigen.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def form_valid(self, form):
        # Si el estatus cambió a ACEPTADO
        if 'status_traslado' in form.changed_data and form.instance.status == 1: 
            form.instance.fecha_inicio = timezone.now()
        return super(cambiarStatusOrigen, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('listTraslado')
    
class cambiarStatusOrigenDestino(LoginRequiredMixin,UpdateView):
    model = Traslado
    form_class = EstatusTrasladoFormOrigenDestino
    template_name = 'modal/seleccionarStatusTrasladoOrigenDestino.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def form_valid(self, form):
        # Si el estatus cambió a ACEPTADO
        if 'status_traslado' in form.changed_data and form.instance.status == 1: 
            form.instance.fecha_traslado = timezone.now()
        return super(cambiarStatusOrigenDestino, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('listTraslado')

class ListTrasladoDestino(LoginRequiredMixin,ListView):
    model = Traslado
    template_name = "destino/listPuestasArribo.html"
    context_object_name = 'trasladosRecibidos'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Filtrar los traslados por la estación destino del usuario logueado
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        queryset = Traslado.objects.filter(estacion_destino=user_estacion)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'traslado'  # Ajusta según la página activa en tu navbar
        context['seccion'] = 'arribo'  # Ajusta según la sección activa
        
        user_profile = self.request.user
        user_estacion = user_profile.estancia

        traslados_count = self.get_queryset().count() 
        context['traslados_count'] = traslados_count

        # Si necesitas más datos en el contexto, puedes añadirlos aquí
        # como lo hiciste en la vista para la estación origen.

        return context
    
class ListaExtranjerosTraslado(LoginRequiredMixin,ListView):
    model = ExtranjeroTraslado
    template_name = "origen/detallesPuestaTraslado.html"
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Obtenemos el ID del traslado desde la URL
        traslado_id = self.kwargs.get('traslado_id')
        
        # Filtramos los extranjeros que comparten el mismo ID de traslado
        queryset = ExtranjeroTraslado.objects.filter(delTraslado_id=traslado_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traslado_id = self.kwargs.get('traslado_id')
        traslado = Traslado.objects.get(pk=traslado_id)
        estacion_id = traslado.estacion_origen.id
        status = traslado.status
        inden = traslado.numeroUnicoProceso
        context['identificador']= inden
        context['status']= status
        context['traslado_id'] = traslado_id 
        context['estacion_id'] = estacion_id  # Pasamos el ID del traslado al contexto
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa
        return context
    

class EtatusTrasladoUpdate(LoginRequiredMixin,UpdateView):
    model = Traslado
    form_class = EstatusTrasladoForm  # Usa tu formulario modificado
    template_name = 'modals/editarEnseresINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Enseres editados con éxito.')

        return reverse_lazy('listarEnseresINM', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['unidadMigratoria'].widget.attrs['readonly'] = True
        return form
    

class DeleteExtranjeroPuestaTraslado(LoginRequiredMixin,DeleteView):
    model = ExtranjeroTraslado
    template_name = 'modal/eliminarExtranjerodePuestaTraslado.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_success_url(self):
        puesta_id = self.object.delTraslado.id
        messages.success(self.request, 'Extranjero Eliminado con Éxito de Traslado.')
        return reverse('listaExtranjerosTraslado', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traslado_id = self.kwargs.get('traslado_id')
        context['traslado_id'] = traslado_id  # Pasamos el ID del traslado al contexto
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa
        return context

class ListaExtranjerosTrasladoDestino(LoginRequiredMixin,ListView):
    model = ExtranjeroTraslado
    template_name = "destino/verExtranjerosTraslado.html"
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Obtenemos el ID del traslado desde la URL
        traslado_id = self.kwargs.get('traslado_id')
        
        # Filtramos los extranjeros que comparten el mismo ID de traslado
        queryset = ExtranjeroTraslado.objects.filter(delTraslado_id=traslado_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traslado_id = self.kwargs.get('traslado_id')
        traslado = Traslado.objects.get(pk=traslado_id)
        estacion_id = traslado.estacion_origen.id
        status = traslado.status
        inden = traslado.numeroUnicoProceso
        context['identificador']= inden
        context['status']= status
        context['traslado_id'] = traslado_id 
        context['estacion_id'] = estacion_id  # Pasamos el ID del traslado al contexto
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'arribo'  # Cambia esto según la página activa
        return context
    
# Reportes PDF
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string

def render_to_pdf(template_src, extranjero):
    # Render the HTML template into a PDF
    html = render_to_string(template_src, {'extranjero': extranjero})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Acuerdo de Traslado - {extranjero.id}.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html.encode('utf-8'), dest=response, encoding='utf-8')

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF: %s' % pisa_status.err, content_type='text/plain')

    return response

def documento_ac(request, extranjero_id):
    # Obtenemos el objeto Extrajero utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Specify the template you want to render
    template_name = "documentos/acuerdoTraslado.html"

    # Render the template into a PDF
    return render_to_pdf(template_name, extranjero)

def mi_vista(request):
    return render(request, 'documentos/acuerdoTraslado.html')

from weasyprint import HTML

def generate_pdf(request, extranjero_id):
    # Obtén el objeto Extranjeros utilizando el ID proporcionado en la URL
    extranjero = get_object_or_404(Extranjero, id=extranjero_id)

    # Obtener el objeto Traslado 
    traslado = ExtranjeroTraslado.objects.filter(delExtranjero=extranjero).first()

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
    hora = traslado.delTraslado.fechaSolicitud
    dia = traslado.delTraslado.fechaSolicitud.strftime('%d')
    mes = traslado.delTraslado.fechaSolicitud.strftime('%B')
    mes_espanol = nombres_meses_espanol.get(mes, mes)
    anio = traslado.delTraslado.fechaSolicitud.strftime('%Y')

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
        'hora': hora,
        'dia': dia,
        'mes': mes_espanol,
        'anio': anio,
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

class cambiarStatusExtranjero(LoginRequiredMixin,UpdateView):
    model = ExtranjeroTraslado
    form_class = EstatusTrasladoFormExtranjero
    template_name = 'modal/seleccionarSttausdeTraslado1.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def form_valid(self, form):
        # Verifica si el status ha cambiado y si es "ACEPTADO," ajusta la fecha de aceptación
        if 'statusTraslado' in form.changed_data and form.instance.statusTraslado == 1:  # 1 representa "ACEPTADO"
            form.instance.fecha_aceptacion = timezone.now()

            # Accede al objeto Extranjero relacionado y actualiza su campo deLaEstacion
            form.instance.delExtranjero.estatus = 'Trasladado'
            form.instance.delExtranjero.save()

            new_station_id = self.request.user.estancia.id
            form.instance.delExtranjero.deLaEstacion_id = new_station_id
            form.instance.delExtranjero.save()

            estacion = self.request.user.estancia
            if estacion:
                estacion.capacidad -= 1
                estacion.save()
            
            if 'statusTraslado' in form.changed_data and form.instance.statusTraslado ==2:
                form.instance.motivo_rechazo = form.cleaned_data.get('motivo_rechazo','')


        return super(cambiarStatusExtranjero, self).form_valid(form)

    def get_success_url(self):
        puesta_id = self.object.delTraslado.id
        messages.success(self.request, 'Status cambiado.')
        return reverse('listaExtranjerosTrasladoDestino', args=[puesta_id])

class seguimientoPuesta(LoginRequiredMixin,DetailView):
    model = Traslado
    template_name = "origen/seguimientoPuesta.html" 
    context_object_name = 'Traslado'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traslado = self.object
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa
 # Cambia esto según la página activa
        return context 
    
class seguimientoPuestaDestino(LoginRequiredMixin,DetailView):
    model = Traslado
    template_name = "destino/seguimientoPuestaDestino.html" 
    context_object_name = 'Traslado'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traslado = self.object
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'arribo'  # Cambia esto según la página activa
        return context 

class estadisticasEnvio(LoginRequiredMixin,TemplateView):
    model = Traslado
    template_name = 'destino/estadisticaDeEnvio.html'
    context_object_name = 'trasladosRecibidos'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Filtrar los traslados por la estación destino del usuario logueado
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        queryset = Traslado.objects.filter(estacion_destino=user_estacion)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        traslado_id = self.kwargs.get('traslado_id')
        traslado = Traslado.objects.get(pk=traslado_id)
        
        # Encuentra los extranjeros asociados a esta puesta de traslado
        extranjeros_en_traslado = ExtranjeroTraslado.objects.filter(delTraslado=traslado)
        nacionalidades = Extranjero.objects.filter(extranjerotraslado__delTraslado=traslado).values('nacionalidad__nombre').annotate(count=Count('id'))
        genero_count = Extranjero.objects.filter(extranjerotraslado__delTraslado=traslado).values('genero').annotate(count=Count('genero'))

        # Cuenta el número de extranjeros en esta puesta de traslado
        numero_extranjeros = extranjeros_en_traslado.count()
        context['navbar'] = 'traslado'  # Ajusta según la página activa en tu navbar
        context['seccion'] = 'arribo'  # Ajusta según la sección activa
        context['traslados_count1'] = numero_extranjeros  # Agregar el recuento de extranjeros
        context['nacionalidades'] = nacionalidades  # Agregar el conteo de extranjeros por nacionalidad
        context['genero'] = genero_count

        user_profile = self.request.user
        user_estacion = user_profile.estancia

        traslados_count = self.get_queryset().count() 
        context['traslados_count'] = traslados_count

        # Si necesitas más datos en el contexto, puedes añadirlos aquí
        # como lo hiciste en la vista para la estación origen.

        return context

    

# en caso de rechazo
class ActualizarTrasladoView(LoginRequiredMixin,FormView):
    template_name = 'modal/actualizar_traslado.html'
    form_class = DecisionForm
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_context_data(self, **kwargs):
        context = super(ActualizarTrasladoView, self).get_context_data(**kwargs)
        traslado = get_object_or_404(Traslado, id=self.kwargs['traslado_id'])
        context['object'] = traslado
        return context

    def form_valid(self, form):
        decision = form.cleaned_data['decision']
        if decision == 'cambiar':
            return redirect('cambio_estacion', pk=self.kwargs['traslado_id'])
        else:
            # Aquí manejas la opción "finalizar proceso" si es necesario.
            # Puedes redirigir a otra página o hacer otro procesamiento aquí.
            return redirect('eliminar_traslado', pk=self.kwargs['traslado_id']) # Esto es solo un ejemplo. Debes decidir a dónde redirigir en este caso.

    
class CambioEstacionView(LoginRequiredMixin,UpdateView):
    model = Traslado
    template_name = 'origen/cambiarEstacion.html'
    form_class = CambioEstacionForm
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_form(self, form_class=None):
        form = super(CambioEstacionView, self).get_form(form_class)
        # Excluye la estación origen y destino actuales del queryset
        form.fields['estacion_destino'].queryset = form.fields['estacion_destino'].queryset.exclude(
            id__in=[self.object.estacion_origen.id, self.object.estacion_destino.id]
        )
        return form


    def form_valid(self, form):
        # Actualiza la estación destino.
        response = super().form_valid(form)

        # Resetear los campos según tus especificaciones.
        self.object.fechaSolicitud = timezone.now()
        self.object.fecha_aceptacion = None
        self.object.fecha_rechazo = None
        self.object.nombreAutoridadRecibe = None
        self.object.motivo_rechazo = None


        # ... resetea los otros campos ...
        self.object.status = 0
        self.object.status_traslado = 0
        self.object.save()

        return response

    def get_success_url(self):
        return reverse_lazy('listTraslado')
from juridico.models import NotificacionDerechos
from llamadasTelefonicas.models import Notificacion

class extranjeroTrasladadoList(LoginRequiredMixin,ListView):
    model = Extranjero
    template_name='destino/verExtranjerosTraladados.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_queryset(self):
        # Obtiene la estación del usuario logueado
        estacion_usuario = self.request.user.estancia

        # Filtra los extranjeros que pertenecen a la estación del usuario y tienen un estatus de "Trasladado"
        queryset = Extranjero.objects.filter(deLaEstacion=estacion_usuario, estatus='Trasladado')
        
        return queryset

  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for extranjero in context['extranjeros']:
         ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
         tiene_notificacion = False

         if ultimo_nup:
            notificacion = Notificacion.objects.filter(nup=ultimo_nup).first()
            if notificacion:
                tiene_notificacion = True

         extranjero.tiene_notificacion = tiene_notificacion
    

        for extranjero in context['extranjeros']:
                ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()

                if ultimo_nup:
                    notificacion = NotificacionDerechos.objects.filter(no_proceso_id=ultimo_nup).first()
                    if notificacion:
                        extranjero.tiene_notificacion_derechos = True
                        extranjero.fecha_aceptacion = notificacion.fechaAceptacion
                        extranjero.estacion_notificacion = notificacion.estacion
                    else:
                        extranjero.tiene_notificacion_derechos = False
                        extranjero.fecha_aceptacion = None
                        extranjero.estacion_notificacion = None

        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'trasladados'  # Cambia esto según la página activa
        return context
    

# eliminar traslado
@login_required(login_url="/permisoDenegado/")
def eliminar_traslado(request, pk):
    traslado = get_object_or_404(Traslado, pk=pk)
    
    # Comprueba si el traslado tiene el status permitido para ser eliminado
    if traslado.status in [0, 2]:
        traslado.delete()
        messages.success(request, 'Traslado eliminado con éxito.')
    else:
        messages.error(request, 'No se puede eliminar el traslado en su estado actual.')

    return redirect('listTraslado')  # Reemplaza 'ruta_lista_traslados' con la ruta correcta para la lista de traslados