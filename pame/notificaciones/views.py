from audioop import reverse
import base64
from datetime import timezone
from typing import Any
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render
from weasyprint import HTML
from vigilancia.models import NoProceso, Extranjero, AutoridadesActuantes, AsignacionRepresentante
from vigilancia.views import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, View, TemplateView
from .models import Defensorias,Relacion, NotificacionConsular, FirmaNotificacionConsular
from .forms import NotificacionesAceptadasForm,modalnotificicacionForm,NotificacionConsularForm, FirmaAutoridadActuanteConsuladoForm, NotificacionComarForm, FirmaAutoridadActuanteComarForm, NotificacionFiscaliaForm, FirmaAutoridadActuanteFiscaliaForm
from django.urls import reverse_lazy
from vigilancia.models import Extranjero
from django.utils import timezone
from vigilancia.models import NoProceso
from django.db.models import OuterRef, Subquery
from comparecencia.models import Comparecencia
from django.db.models import Q
from django.core.files.base import ContentFile
from django.template.loader import render_to_string, get_template
import qrcode
from django.http import HttpResponse, HttpResponseNotFound
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import HttpResponse, HttpResponseNotFound
import base64
from django.views.decorators.csrf import csrf_exempt
from acuerdos.models import Repositorio
import qrcode
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.db.models import Exists, OuterRef
from django.http import HttpResponse, Http404
import os
from django.utils import timezone
from datetime import timedelta

from .models import NotificacionCOMAR,FirmaNotificacionComar,NotificacionFiscalia,FirmaNotificacionFiscalia
class notificar(LoginRequiredMixin,ListView):
    model = Defensorias
    template_name='notificacion.html'
    context_object_name = 'defensorias'
    login_url = '/permisoDenegado/'  
    def get_queryset(self):
        queryset =  Defensorias.objects.all()
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))['consecutivo__max']

        ultimo_alegato = Relacion.objects.filter(extranjero_id=extranjero_id, nup__consecutivo=ultimo_nup).order_by('-fechaHora').first()

        if ultimo_alegato:
            # Obtener el id del último alegato
            ultimo_alegato_id = ultimo_alegato.id
        else:
            # No hay alegatos asociados al último NUP
            ultimo_alegato_id = None
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        apellido = extranjero.apellidoPaternoExtranjero
        nacionalidad = extranjero.nacionalidad
        apellidom = extranjero.apellidoMaternoExtranjero
        estacion = extranjero.deLaEstacion
        fechanacimiento = extranjero.fechaNacimiento
        numeroextranjero = extranjero.numeroExtranjero
        context['noti']= ultimo_alegato_id
        context['extranjero']=extranjero
        context['numeroextranjero']=numeroextranjero
        context['fechanacimiento']=fechanacimiento
        context['estacion']=estacion
        context['apellidom']=apellidom
        context['nacionalidad']=nacionalidad
        context['apellido']=apellido 
        context['nombre']= nombre
        context['navbar'] = 'notificaciones'
        context['seccion'] = 'defensoria'
        context['nombre_estacion'] = self.request.user.estancia.nombre
        return context

    
# LISTA DE EXTRANJEROS PARA DEFENSORIA
class listExtranjerosDefensoria(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'defensoria/defensoria.html'
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

        # Filtrar NoProceso basado en estos últimos registros
        queryset = NoProceso.objects.filter(
            nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
        )

        # Calcular la diferencia de tiempo para cada NoProceso
        now = timezone.now()
        for no_proceso in queryset:
            time_diff = now - no_proceso.horaRegistroNup
            no_proceso.horas_desde_registro = time_diff // timedelta(hours=1)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'acuerdos'  # Cambia esto según la página activa
        context['navbar1'] = 'resoluciones'  # Cambia esto según la página activa

        context['seccion'] = 'resoluciones'
        context['seccion1'] = 'retorno'
        return context
        
   



# views.py
from django.shortcuts import render, redirect
from .forms import DefensorForm

def defensores(request):
    if request.method == 'POST':
        form = DefensorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listdefensores')
    else:
        form = DefensorForm()

    context = {
        'form': form,
        'navbar': 'catalogos',
        'seccion': 'defensorias',
    }

    return render(request, 'defensorias.html', context)



class tabladefensores(LoginRequiredMixin,ListView):
    model = Defensorias
    template_name = 'tabladefensores.html'
    context_object_name = 'defensorias'
    login_url = '/permisoDenegado/' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'defensorias'    
        return context

    
from .models import notificacionesAceptadas, Defensorias

# views.py
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import notificacionesAceptadas, Defensorias
from .forms import NotificacionesAceptadasForm
from django.contrib import messages

class SubirArchivo(LoginRequiredMixin,CreateView):
    template_name = 'modal.html'
    form_class = NotificacionesAceptadasForm
    model = notificacionesAceptadas
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Archivo subido exitosamente')

        return reverse_lazy('defensoria')
    


class modalnotificar(LoginRequiredMixin, CreateView):
    template_name = 'modalnotificar.html'
    form_class = modalnotificicacionForm
    model = Relacion
    login_url = '/permisoDenegado/'

    def get_success_url(self):
        messages.success(self.request, 'Notificacion creada exitosamente')
        extranjero_id = self.kwargs['extranjero_id']
        return reverse_lazy('notificacion', kwargs={'pk': extranjero_id})

    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        defen_id = self.kwargs.get('defensoria_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_proceso = extranjero.noproceso_set.latest('consecutivo')
        proceso_id = ultimo_proceso.nup
        initial['nup'] = proceso_id
        defen = Defensorias.objects.get(id=defen_id)
        initial['defensoria'] = defen
        initial['extranjero'] = extranjero
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero = self.kwargs['extranjero_id']
        defenso = self.kwargs['defensoria_id']
        context['extranjero'] = get_object_or_404(Extranjero, pk=extranjero)
        context['defensoria'] = get_object_or_404(Defensorias, pk=defenso)
        return context

class listExtranjerosComar(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'comar/listExtranjerosComar.html'
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
            comparecencias_con_refugio = set(Comparecencia.objects.filter(solicitaRefugio=True).values_list('nup', flat=True))
            nups_extranjeros_filtrados = set([e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id])
            nups_finales = nups_extranjeros_filtrados & comparecencias_con_refugio
            
            queryset = NoProceso.objects.filter(
            nup__in=nups_finales,
            comparecencia=True
            )
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['navbar'] = 'Notificaciones'
        context['seccion'] = 'comar'
        return context
    

class CrearNotificacionComar(View):
    def post(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        form = NotificacionComarForm(request.POST)
        if form.is_valid():
            notificacionComar= form.save(commit=False)
            notificacionComar.nup = no_proceso
            notificacionComar.save()
            data = {
                    'success': True, 
                    'message': 'Notificación Comar creada con éxito.', 
                    'comar_id': notificacionComar.id
                }
            return JsonResponse(data, status=200)

        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)

    def get(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero 
        try:
            ultima_comparecencia = Comparecencia.objects.filter(nup=no_proceso).order_by('-fechahoraComparecencia').first()
        except Comparecencia.DoesNotExist:
            ultima_comparecencia = None

        initial_data = {
             'delaEstacion': extranjero.deLaEstacion,
             'nup':no_proceso,
             'delaComparecencia': ultima_comparecencia,  # Añadir la instancia de Comparecencia aquí

 
        }

        form =  NotificacionComarForm(initial=initial_data)
        autoridades = AutoridadesActuantes.objects.none()
        if extranjero.deLaPuestaIMN:
                autoridades = AutoridadesActuantes.objects.filter(
                    Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaUno_id) |
                    Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaDos_id)
                )
        elif extranjero.deLaPuestaAC:
                autoridades = AutoridadesActuantes.objects.filter(
                    Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaUno_id) |
                    Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaDos_id)
                )
        else:
                autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)
        form.fields['delaAutoridad'].queryset = autoridades

        context = {
            'form': form,
            'nup_id': nup_id,
            'extranjero': extranjero,
            'navbar': 'Notificaciones',
            'seccion':'comar',
        }
        
         
        return render(request, 'comar/crearNotificacionComar.html', context)

def generar_qr_firma_notificacion_comar(request, comar_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}notificaciones/firma_autoridad_actuante-comar/{comar_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante_notifi_comar(request, comar_id):
    notificacion_comar = get_object_or_404(NotificacionCOMAR, pk=comar_id)
    firma, created = FirmaNotificacionComar.objects.get_or_create(notificacionComar=notificacion_comar)

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente1')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteComarForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{comar_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteComarForm()
    return render(request, 'firma/firma_autoridad_actuante.html', {'form': form, 'comar_id': comar_id})

@csrf_exempt
def verificar_firma_autoridad_actuante_comar(request, comar_id):
    try:
        firma = FirmaNotificacionComar.objects.get(notificacionComar=comar_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaNotificacionComar.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

class CrearNotificacionFiscalia(View):
    def post(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        form = NotificacionFiscaliaForm(request.POST)
        if form.is_valid():
            notificacionFiscalia= form.save(commit=False)
            notificacionFiscalia.nup = no_proceso
            notificacionFiscalia.save()
            data = {
                    'success': True, 
                    'message': 'Notificación Fiscalia creada con éxito.', 
                    'fiscalia_id': notificacionFiscalia.id
                }
            return JsonResponse(data, status=200)

        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)

    def get(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero 
        try:
            ultima_comparecencia = Comparecencia.objects.filter(nup=no_proceso).order_by('-fechahoraComparecencia').first()
        except Comparecencia.DoesNotExist:
            ultima_comparecencia = None
        initial_data = {
            'delaEstacion': extranjero.deLaEstacion,
            'nup':no_proceso,
            'delaComparecencia': ultima_comparecencia,  # Añadir la instancia de Comparecencia aquí

 
        }

        form =  NotificacionFiscaliaForm(initial=initial_data)
        autoridades = AutoridadesActuantes.objects.none()
        if extranjero.deLaPuestaIMN:
                autoridades = AutoridadesActuantes.objects.filter(
                    Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaUno_id) |
                    Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaDos_id)
                )
        elif extranjero.deLaPuestaAC:
                autoridades = AutoridadesActuantes.objects.filter(
                    Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaUno_id) |
                    Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaDos_id)
                )
        else:
                autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)
        form.fields['delaAutoridad'].queryset = autoridades

        context = {
            'form': form,
            'nup_id': nup_id,
            'extranjero': extranjero,
            'navbar': 'notificacion',
            'seccion': 'fiscalia',
            'navbar': 'Notificaciones',
            'seccion':'fiscalia',
        }
        
        return render(request, 'fiscalia/crearNotificacionFiscalia.html', context)

def generar_qr_firma_notificacion_fiscalia(request, fiscalia_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}notificaciones/firma_autoridad_actuante-fiscalia/{fiscalia_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante_notifi_fiscalia(request, fiscalia_id):
    notificacion_fiscalia = get_object_or_404(NotificacionFiscalia, pk=fiscalia_id)
    firma, created = FirmaNotificacionFiscalia.objects.get_or_create(notificacionFiscalia=notificacion_fiscalia)

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente1')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteFiscaliaForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{fiscalia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteFiscaliaForm()
    return render(request, 'firma/firma_autoridad_actuante.html', {'form': form, 'fiscalia_id': fiscalia_id})

@csrf_exempt
def verificar_firma_autoridad_actuante_fiscalia(request, fiscalia_id):
    try:
        firma = FirmaNotificacionFiscalia.objects.get(notificacionFiscalia=fiscalia_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaNotificacionFiscalia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)



class listExtranjerosFiscalia(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'fiscalia/listExtranjeroFiscalia.html'
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
            comparecencias_con_delito = set(Comparecencia.objects.filter(victimaDelito=True).values_list('nup', flat=True))
            nups_extranjeros_filtrados = set([e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id])
            nups_finales = nups_extranjeros_filtrados & comparecencias_con_delito

      
            queryset = NoProceso.objects.filter(
            nup__in=nups_finales,
            comparecencia=True
            )

            return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['navbar'] = 'Notificaciones'
        context['seccion'] = 'fiscalia'
        return context
class listExtranjerosConsulado(LoginRequiredMixin,ListView):

    model = NoProceso
    template_name = 'consulado/listExtranjerosConsulado.html'
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

        # Obtener los NUPs excluidos (comparecencias con delito o refugio)
        comparecencias_excluidas = set(Comparecencia.objects.filter(
            Q(victimaDelito=True) | Q(solicitaRefugio=True)
        ).values_list('nup', flat=True))

        # Consulta para verificar si existe una notificación consular
        notificacion_consular_existente = NotificacionConsular.objects.filter(
            nup=OuterRef('pk')
        )

        repositorio_existente = Repositorio.objects.filter(
        nup=OuterRef('pk')
        ).order_by('-fechaGeneracion').values('id')[:1]

        queryset = NoProceso.objects.filter(
            extranjero_id__in=extranjeros_filtrados.values('id'),
            comparecencia=True
        ).exclude(
            nup__in=comparecencias_excluidas
        ).annotate(
            tiene_notificacion_consular=Exists(notificacion_consular_existente),
            repositorio_id=Subquery(repositorio_existente)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['navbar'] = 'Notificaciones'
        context['seccion'] = 'consulado'
        return context
    

from django.shortcuts import render, redirect
from .models import Qrfirma
from .forms import QrfirmaForm  # Reemplaza con el nombre correcto de tu formulario

def generar_qr_firmas_noti(request, notificacion_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"127.0.0.1:8000/notificaciones/firma_autoridad_actuante_notificacion/{notificacion_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante_notificacion(request, noti_id):
    notificacion = get_object_or_404(Relacion, pk=noti_id)
    firmas, created = Qrfirma.objects.get_or_create(autoridad=notificacion)  # Usar comparecencia aquí

    if firmas.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    if request.method == 'POST':
        form = QrfirmaForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{noti_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firmas.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = QrfirmaForm()
    return render(request, 'firmardocumento.html', {'form': form, 'noti_id': noti_id})


@csrf_exempt
def verificar_firma_autoridad_actuante_notificacion(request, noti_id):
    try:
        firma = Qrfirma.objects.get(autoridad=noti_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except Qrfirma.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

def estado_firmas_notificacion(request, noti_id):
    # Obtener la instancia de Comparecencia, o devolver un error 404 si no se encuentra
    notificacion = get_object_or_404(Relacion, pk=noti_id)

    # Obtener la instancia de FirmaComparecencia asociada a la Comparecencia
    firma = Qrfirma.objects.filter(autoridad=notificacion).first()

    # Si no existe una instancia de FirmaComparecencia, establecer todas las firmas como None
    if not firma:
        estado_firmas = {
            'firmaAutoridadActuante': None,
        }
    else:
        # Crear un diccionario con el estado de cada firma (True si existe, False si no)
        estado_firmas = {
            'firmaAutoridadActuante': firma.firmaAutoridadActuante is not None
        }

    # Devolver el estado de las firmas en formato JSON
    return JsonResponse(estado_firmas)
def verificar_firmas_no(request, noti_id):
    try:
        alegato_firmas = Qrfirma.objects.filter(noti_id=noti_id).values('firmaAutoridadActuante')
        
        firmas_existen = all(alegato_firma for alegato_firma in alegato_firmas[0].values())
        
        return JsonResponse({'firmas_existen': firmas_existen})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    


class CrearNotificacionConsulado(View):
    def post(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        form = NotificacionConsularForm(request.POST)
        if form.is_valid():
            notificacionConsular = form.save(commit=False)
            notificacionConsular.nup = no_proceso
            notificacionConsular.save()

            data = {
                'success': True, 
                'message': 'Notificación Consular creada con éxito.', 
                'consulado_id': notificacionConsular.id
            }
            return JsonResponse(data, status=200)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)
        

    def get(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero 

        initial_data = {
             'delaEstacion': extranjero.deLaEstacion,
             'nup':no_proceso,
 
        }

        form = NotificacionConsularForm(initial=initial_data)
        autoridades = AutoridadesActuantes.objects.none()
        if extranjero.deLaPuestaIMN:
                autoridades = AutoridadesActuantes.objects.filter(
                    Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaUno_id) |
                    Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaDos_id)
                )
        elif extranjero.deLaPuestaAC:
                autoridades = AutoridadesActuantes.objects.filter(
                    Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaUno_id) |
                    Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaDos_id)
                )
        else:
                autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)
        form.fields['delaAutoridad'].queryset = autoridades

        context = {
            'form': form,
            'nup_id': nup_id,
            'extranjero': extranjero,
            'navbar': 'Notificaciones',
            'seccion': 'consulado',
        }
        
        return render(request, 'consulado/crearNotificacionConsulado.html', context)



def generar_qr_firma_notificacion_consular(request, consulado_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}notificaciones/firma_autoridad_actuante/{consulado_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante_notifi_consul(request, consulado_id):
    notificacion_consular = get_object_or_404(NotificacionConsular, pk=consulado_id)
    firma, created = FirmaNotificacionConsular.objects.get_or_create(notificacionConsular=notificacion_consular)

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente1')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteConsuladoForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{consulado_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteConsuladoForm()
    return render(request, 'firma/firma_autoridad_actuante.html', {'form': form, 'consulado_id': consulado_id})

@csrf_exempt
def verificar_firma_autoridad_actuante(request, consulado_id):
    try:
        firma = FirmaNotificacionConsular.objects.get(notificacionConsular=consulado_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaNotificacionConsular.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)