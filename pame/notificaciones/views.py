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
from django.views.generic import ListView, CreateView, View, TemplateView, UpdateView
from .models import Defensorias, FirmaNombramientoExterno,Relacion, NotificacionConsular, FirmaNotificacionConsular, ExtranjeroDefensoria, DocumentoRespuestaDefensoria, nombramientoRepresentante
from .forms import FirmaAutoridadActuanteNombramientoExternoForm, FirmaExtranjeroNombramientoExternoForm, FirmaRepresentanteLegalNombramientoExternoForm, FirmaTestigo1NombramientoExternoForm, FirmaTestigo2NombramientoExternoForm, FirmaTraductorNombramientoExternoForm, NotificacionesAceptadasForm,modalnotificicacionForm,NotificacionConsularForm, FirmaAutoridadActuanteConsuladoForm, NotificacionComarForm, FirmaAutoridadActuanteComarForm, NotificacionFiscaliaForm, FirmaAutoridadActuanteFiscaliaForm, firmasDefenso,NombramientoRepresentanteExternoForm
from .forms import ExtranjeroDefensoriaForm, firmasDefensoForms, DocumentoRespuestaDefensoriaForm,NombramientoRepresentanteInternoForm, FirmaAutoridadActuanteNombramientoInternoForm, FirmaRepresentanteLegalNombramientoInternoForm, FirmaTraductorNombramientoInternoForm, FirmaTestigo1NombramientoInternoForm, FirmaTestigo2NombramientoInternoForm, FirmaExtranjeroNombramientoInternoForm
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
from catalogos.models import RepresentantesLegales
from .models import NotificacionCOMAR,FirmaNotificacionComar,NotificacionFiscalia,FirmaNotificacionFiscalia,FirmaNombramientoInterno
from acuerdos.models import Repositorio, TiposDoc, ClasificaDoc
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
class listExtranjerosDefensoria(LoginRequiredMixin, ListView):
    model = NoProceso
    template_name = 'defensoria/defensoria.html'
    context_object_name = "extranjeros"
    
    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        estado = self.request.GET.get('estado_filtrado', 'activo')

        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
        if estado == 'activo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
        elif estado == 'inactivo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

        ultimo_no_proceso = NoProceso.objects.filter(
            extranjero_id=OuterRef('pk')
        ).order_by('-consecutivo')

        extranjeros_filtrados = extranjeros_filtrados.annotate(
            ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
        )

        defensoria_asignada = ExtranjeroDefensoria.objects.filter(
            nup=OuterRef('pk')
        )

        estado_defensoria = self.request.GET.get('estado_defensoria', None)

        queryset = NoProceso.objects.filter(
            nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
        ).annotate(
            tiene_defensoria_asignada=Exists(defensoria_asignada)
        )
        documento_existente = DocumentoRespuestaDefensoria.objects.filter(
            extranjero_defensoria__nup=OuterRef('nup')
        )
        queryset = queryset.annotate(
            documento_subido=Exists(documento_existente)
        )

        fecha_subida_documento = DocumentoRespuestaDefensoria.objects.filter(
            extranjero_defensoria__nup=OuterRef('nup')
        ).order_by('-fecha_creacion').values('fecha_creacion')[:1]

        queryset = queryset.annotate(
            fecha_subida_documento=Subquery(fecha_subida_documento)
        )

        # Añade una anotación para obtener el ID de ExtranjeroDefensoria
        queryset = queryset.annotate(
            extranjero_defensoria_id=Subquery(
                ExtranjeroDefensoria.objects.filter(nup=OuterRef('pk')).values('id')[:1]
            )
        )

        # Anotación para obtener la URL del documento del repositorio
        tipo_respuesta_defensoria = TiposDoc.objects.filter(descripcion="Respuesta de Defensoria").first()
        if tipo_respuesta_defensoria:
            ultimo_documento_id = Repositorio.objects.filter(
                nup=OuterRef('pk'),
                delTipo=tipo_respuesta_defensoria
            ).order_by('-fechaGeneracion').values('id')[:1]

            queryset = queryset.annotate(
                ultimo_documento_id=Subquery(ultimo_documento_id)
            )
        if estado_defensoria == 'por_notificar':
            queryset = queryset.filter(tiene_defensoria_asignada=False)
        elif estado_defensoria == 'ya_notificado':
            queryset = queryset.filter(tiene_defensoria_asignada=True)
        else:
            queryset = queryset.filter(tiene_defensoria_asignada=False)

        now = timezone.now()
        for no_proceso in queryset:
            time_diff = now - no_proceso.horaRegistroNup
            horas_desde_registro = time_diff // timedelta(hours=1)
            no_proceso.horas_desde_registro = min(horas_desde_registro, 36)

        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for extranjero in context['extranjeros']:
            documento_id = getattr(extranjero, 'ultimo_documento_id', None)
            if documento_id:
                try:
                    documento = Repositorio.objects.get(id=documento_id)
                    extranjero.url_documento = documento.archivo.url
                except Repositorio.DoesNotExist:
                    extranjero.url_documento = None

        context['navbar'] = 'Notificaciones'  # Cambia esto según la página activa

        context['seccion'] = 'defensoria'
        return context
        
   


class DocumentoRespuestaDefensoriaCreateView(CreateView):
    model = DocumentoRespuestaDefensoria
    form_class = DocumentoRespuestaDefensoriaForm
    template_name = 'defensoria/respuesta_defensoria.html'  # Reemplaza con el nombre de tu plantilla HTML

    def form_valid(self, form):
            # Obtener los IDs de la URL
            extranjero_defensoria_id = self.kwargs.get('extranjero_defensoria_id')
            nup_id = self.kwargs.get('nup_id')

            # Obtener los objetos basados en los IDs y asignarlos al objeto del formulario
            form.instance.extranjero_defensoria = ExtranjeroDefensoria.objects.get(id=extranjero_defensoria_id)
            form.instance.nup = NoProceso.objects.get(nup=nup_id)

            # Llamada al método form_valid original para guardar el DocumentoRespuestaDefensoria
            response = super(DocumentoRespuestaDefensoriaCreateView, self).form_valid(form)

            # Obtener el objeto DocumentoRespuestaDefensoria recién creado
            documento_respuesta_defensoria = form.instance

            # Crear o recuperar la categoría y el tipo de documento para el Repositorio
            clasificacion, _ = ClasificaDoc.objects.get_or_create(clasificacion="Defensoria")
            tipo_doc, _ = TiposDoc.objects.get_or_create(descripcion="Respuesta de Defensoria", delaClasificacion=clasificacion)

            # Generar un nombre de archivo para el Repositorio
            nombre_archivo_repo = f"Respuesta_Defensoria_{documento_respuesta_defensoria.id}.pdf"

            # Crear una nueva instancia en el Repositorio
            repo = Repositorio(
                nup=documento_respuesta_defensoria.nup,
                delTipo=tipo_doc,
                delaEstacion=self.request.user.estancia,  # Asumiendo que el usuario tiene una estancia asociada
                delResponsable=self.request.user.get_full_name(),
            )

            # Si es necesario, copiar el archivo al Repositorio
            if documento_respuesta_defensoria.archivo:
                with documento_respuesta_defensoria.archivo.open() as archivo:
                    repo.archivo.save(nombre_archivo_repo, ContentFile(archivo.read()))

            repo.save()

            return response

    def get_success_url(self):
        return reverse_lazy('defensoria')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener los IDs de la URL
        extranjero_defensoria_id = self.kwargs.get('extranjero_defensoria_id')
        nup_id = self.kwargs.get('nup_id')

        # Obtener el objeto ExtranjeroDefensoria
        extranjero_defensoria = ExtranjeroDefensoria.objects.get(id=extranjero_defensoria_id)
        context['extranjero_defensoria'] = extranjero_defensoria

        # Obtener el objeto NoProceso
        nup = NoProceso.objects.get(nup=nup_id)
        context['nup'] = nup

        # Si es necesario, puedes agregar también el objeto Defensoria
        defensoria = extranjero_defensoria.defensoria
        context['defensoria'] = defensoria
        context['navbar'] = 'Notificaciones'  # Cambia esto según la página activa

        context['seccion'] = 'defensoria'
        return context
# views.py
from django.shortcuts import render, redirect
from .forms import DefensorForm

class createDEfensoria(CreateView):
    template_name='defensorias.html'
    model = Defensorias
    form_class = DefensorForm
    def get_success_url(self):
        messages.success(self.request, 'Defensoria creada exitosamente')
        return reverse_lazy('listdefensores')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'defensor'
        return context


class editarDefensoria(UpdateView):
    template_name='editarDefensoria.html'
    model = Defensorias
    form_class= DefensorForm
    def get_success_url(self):
        messages.success(self.request, 'Defensoria editada exitosamente')
        return reverse_lazy('listdefensores')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'defensor'
        return context

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
        context['seccion'] = 'defensor'
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

class listExtranjerosComar(LoginRequiredMixin, ListView):
    model = NoProceso
    template_name = 'comar/listExtranjerosComar.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        estado = self.request.GET.get('estado_filtrado', 'activo')

        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
        if estado == 'activo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
        elif estado == 'inactivo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

        ultimo_no_proceso = NoProceso.objects.filter(
            extranjero_id=OuterRef('pk')
        ).order_by('-consecutivo')

        extranjeros_filtrados = extranjeros_filtrados.annotate(
            ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
        )

        comparecencias_con_refugio = set(Comparecencia.objects.filter(solicitaRefugio=True).values_list('nup', flat=True))
        nups_extranjeros_filtrados = set([e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id])
        nups_finales = nups_extranjeros_filtrados & comparecencias_con_refugio

        notificacion_comar_existente = NotificacionCOMAR.objects.filter(
            nup=OuterRef('pk')
        )

        repositorio_existente = Repositorio.objects.filter(
            nup=OuterRef('pk')
        ).order_by('-fechaGeneracion').values('id')[:1]

        estado_notificacion = self.request.GET.get('estado_notificacion', None)

        queryset = NoProceso.objects.filter(
            nup__in=nups_finales,
            comparecencia=True
        ).annotate(
            tiene_notificacion_comar=Exists(notificacion_comar_existente),
            repositorio_id=Subquery(repositorio_existente)
        )

        if estado_notificacion == 'por_notificar':
            queryset = queryset.filter(tiene_notificacion_comar=False)
        elif estado_notificacion == 'ya_notificado':
            queryset = queryset.filter(tiene_notificacion_comar=True)
        else:
            queryset = queryset.filter(tiene_notificacion_comar=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'Notificaciones'  # Cambia esto según la página activa
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



class listExtranjerosFiscalia(LoginRequiredMixin, ListView):
    model = NoProceso
    template_name = 'fiscalia/listExtranjeroFiscalia.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'

    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        estado = self.request.GET.get('estado_filtrado', 'activo')

        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
        if estado == 'activo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
        elif estado == 'inactivo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

        ultimo_no_proceso = NoProceso.objects.filter(
            extranjero_id=OuterRef('pk')
        ).order_by('-consecutivo')

        extranjeros_filtrados = extranjeros_filtrados.annotate(
            ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
        )

        comparecencias_con_delito = set(Comparecencia.objects.filter(victimaDelito=True).values_list('nup', flat=True))
        nups_extranjeros_filtrados = set([e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id])
        nups_finales = nups_extranjeros_filtrados & comparecencias_con_delito

        notificacion_fiscalia_existente = NotificacionFiscalia.objects.filter(
            nup=OuterRef('pk')
        )

        repositorio_existente = Repositorio.objects.filter(
            nup=OuterRef('pk')
        ).order_by('-fechaGeneracion').values('id')[:1]

        estado_notificacion = self.request.GET.get('estado_notificacion', None)

        queryset = NoProceso.objects.filter(
            nup__in=nups_finales,
            comparecencia=True
        ).annotate(
            tiene_notificacion_fiscalia=Exists(notificacion_fiscalia_existente),
            repositorio_id=Subquery(repositorio_existente)
        )

        if estado_notificacion == 'por_notificar':
            queryset = queryset.filter(tiene_notificacion_fiscalia=False)
        elif estado_notificacion == 'ya_notificado':
            queryset = queryset.filter(tiene_notificacion_fiscalia=True)
        else:
            queryset = queryset.filter(tiene_notificacion_fiscalia=False)

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['navbar'] = 'Notificaciones'
        context['seccion'] = 'fiscalia'
        return context
class listExtranjerosConsulado(LoginRequiredMixin, ListView):
    model = NoProceso
    template_name = 'consulado/listExtranjerosConsulado.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'

    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        estado = self.request.GET.get('estado_filtrado', 'activo')

        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
        if estado == 'activo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
        elif estado == 'inactivo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

        comparecencias_excluidas = set(Comparecencia.objects.filter(
            Q(victimaDelito=True) | Q(solicitaRefugio=True)
        ).values_list('nup', flat=True))

        notificacion_consular_existente = NotificacionConsular.objects.filter(
            nup=OuterRef('pk')
        )

        repositorio_existente = Repositorio.objects.filter(
            nup=OuterRef('pk')
        ).order_by('-fechaGeneracion').values('id')[:1]

        estado_notificacion = self.request.GET.get('estado_notificacion', None)

        queryset = NoProceso.objects.filter(
            extranjero_id__in=extranjeros_filtrados.values('id'),
            comparecencia=True
        ).exclude(
            nup__in=comparecencias_excluidas
        ).annotate(
            tiene_notificacion_consular=Exists(notificacion_consular_existente),
            repositorio_id=Subquery(repositorio_existente)
        )

        if estado_notificacion == 'por_notificar':
            queryset = queryset.filter(tiene_notificacion_consular=False)
        elif estado_notificacion == 'ya_notificado':
            queryset = queryset.filter(tiene_notificacion_consular=True)
        else:
            queryset = queryset.filter(tiene_notificacion_consular=False)

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







#-------------------------------------------------Selección Defesoria------------------------------
class selectDefensoria(ListView):
    model = Defensorias
    template_name = 'defensoria/elegirDefensoria.html'
    context_object_name = 'defensorias'
    login_url = '/permisoDenegado/' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_proceso = extranjero.noproceso_set.latest('consecutivo')
        proceso_id = ultimo_proceso.nup       
        context['nup'] = proceso_id
        context['extranjero'] = extranjero
        context['navbar'] = 'catalogos'
        context['seccion'] = 'defensor'
        return context
   
class crearRelacionAjax(View):
    def post(self, request, nup_id,defensoria_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        defensoria = get_object_or_404(Defensorias, id=defensoria_id)


        form = ExtranjeroDefensoriaForm(request.POST)
        if form.is_valid():
            defensorias = form.save(commit=False)
            defensorias.nup = no_proceso
            defensorias.defensoria = defensoria

                # Solo guarda una nueva comparecencia si no existe una previa
            defensorias.save()
            defensoria_id = defensorias.id

                # Guardar el ID de la comparecencia en la sesión

            data = {'success': True, 'message': 'Constancia creada con éxito.', 'defensoria_id': defensoria_id}
            return JsonResponse(data, status=200)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)
    def get(self, request, nup_id,defensoria_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        defensoria = get_object_or_404(Defensorias, id=defensoria_id)

    

        extranjero = no_proceso.extranjero
        dd = defensoria
        defenso = defensoria.id
        initial_data = {
            'nup':no_proceso,
            'defensoria':defenso,
            # ... otros campos que quieras incluir ...
        }
        form = ExtranjeroDefensoriaForm(initial= initial_data)
        autoridades = AutoridadesActuantes.objects.none()
        # ... lógica para establecer autoridades y traductor ...
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

            # Establecer el queryset de autoridades actuantes y traductor
        form.fields['autoridadActuante'].queryset = autoridades
        context = {
            'form': form,
            'nup_id': nup_id,
            'extranjero': extranjero,
            'navbar': 'alegatos',
            'seccion': 'nofirma',
            'defensorias':dd,

        }

        return render(request, 'modalDefensoria/crearRelacion.html', context)

def generar_qr_firmas_defensoria(request, defensoria_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}notificaciones/firma_autoridad_actuante_defensoria/{defensoria_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante_defensoria(request, defensoria_id):
    notificacion = get_object_or_404(ExtranjeroDefensoria, pk=defensoria_id)
    firma, created = firmasDefenso.objects.get_or_create(defensoria=notificacion)  # Usar comparecencia aquí

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    if request.method == 'POST':
        form = firmasDefensoForms(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{defensoria_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = firmasDefenso()
    return render(request, 'modalDefensoria/firmaDefensoria.html', {'form': form, 'defensoria_id': defensoria_id})
@csrf_exempt
def verificar_firma_autoridad_actuante_defensoria(request, defensoria_id):
    try:
        firma = firmasDefenso.objects.get(defensoria=defensoria_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except firmasDefenso.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

def estado_firmas_defensoria(request, defensoria_id):
    # Obtener la instancia de Comparecencia, o devolver un error 404 si no se encuentra
    notificacion = get_object_or_404(ExtranjeroDefensoria, pk=defensoria_id)

    # Obtener la instancia de FirmaComparecencia asociada a la Comparecencia
    firma = firmasDefensoForms.objects.filter(defenosria=notificacion).first()

    # Si no existe una instancia de FirmaComparecencia, establecer todas las firmas como None
    if not firma:
        estado_firmas = {
            'firmaAutoridadActuante': None,
        }
    else:
        # Crear un diccionario con el estado de cada firma (True si existe, False si no)
        estado_firmas = {
            'firmaAutoridadActuante': firma.firmaAutoridadActuante is not None,
        }

    # Devolver el estado de las firmas en formato JSON
    return JsonResponse(estado_firmas)

def verificar_firmas_defensoria(request, defensoria_id):
    try:
        constancia_firmas = firmasDefensoForms.objects.filter(defensoria=defensoria_id).values('firmaAutoridadActuante')
        
        firmas_existen = all(constancia_firma for constancia_firma in constancia_firmas[0].values())
        
        return JsonResponse({'firmas_existen': firmas_existen})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def obtener_datos_defensoria(request, defensoria_id):
    constancia = get_object_or_404(ExtranjeroDefensoria, pk=defensoria_id)

    datos = {
        'nombreAutoridadActuante': f"{constancia.autoridadActuante.autoridad.nombre} {constancia.autoridadActuante.autoridad.apellidoPaterno} {constancia.autoridadActuante.autoridad.apellidoMaterno or ''}".strip() if constancia.autoridadActuante else '',
    }

    return JsonResponse(datos)


# class CrearNombramientoInterno(View):

#     def post(self, request, nup_id, *args, **kwargs):
#         no_proceso = get_object_or_404(NoProceso, nup=nup_id)
#         form = NotificacionConsularForm(request.POST)
#         if form.is_valid():
#             notificacionConsular = form.save(commit=False)
#             notificacionConsular.nup = no_proceso
#             notificacionConsular.save()

#             data = {
#                 'success': True, 
#                 'message': 'Notificación Consular creada con éxito.', 
#                 'consulado_id': notificacionConsular.id
#             }
#             return JsonResponse(data, status=200)
#         else:
#             data = {'success': False, 'errors': form.errors}
#             return JsonResponse(data, status=400)
        

#     def get(self, request, nup_id, *args, **kwargs):
#         no_proceso = get_object_or_404(NoProceso, nup=nup_id)
#         extranjero = no_proceso.extranjero 
#         ultimo_registro = ExtranjeroDefensoria.objects.filter(nup=no_proceso).order_by('-fechaHora').first()
#         numero_oficio = ultimo_registro.oficio if ultimo_registro else None
#         defensoria = ultimo_registro.defensoria if ultimo_registro else None

#         initial_data = {
#             'delaEstacion': extranjero.deLaEstacion,
#             'nup':no_proceso,
#             'oficio': numero_oficio,  # Establecer el número de oficio inicial
#             'defensoria': defensoria,  # Establecer la defensoría inicial

#         }

#         form = NombramientoRepresentanteForm(initial=initial_data)

#         if defensoria:
#             representantes_legales = RepresentantesLegales.objects.filter(defensoria=defensoria)
#             form.fields['representanteLegal'].queryset = representantes_legales
#         else:
#             form.fields['representanteLegal'].queryset = RepresentantesLegales.objects.none()

#         autoridades = AutoridadesActuantes.objects.none()
#         if extranjero.deLaPuestaIMN:
#                 autoridades = AutoridadesActuantes.objects.filter(
#                     Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaUno_id) |
#                     Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaDos_id)
#                 )
#         elif extranjero.deLaPuestaAC:
#                 autoridades = AutoridadesActuantes.objects.filter(
#                     Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaUno_id) |
#                     Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaDos_id)
#                 )
#         else:
#                 autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)
#         form.fields['autoridadActuante'].queryset = autoridades

#         context = {
#             'form': form,
#             'nup_id': nup_id,
#             'extranjero': extranjero,
#             'navbar': 'Notificaciones',
#             'seccion': 'defensoria',
#         }
        
#         return render(request, 'defensoria/crearNombramientoInterno.html', context)


class CrearNombramientoInterno(View):

    def post(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        form = NombramientoRepresentanteInternoForm(request.POST)
        if form.is_valid():
            nombramientoRepresentante = form.save(commit=False)
            nombramientoRepresentante.nup = no_proceso
            estacion_origen = no_proceso.extranjero.deLaEstacion
            nombramientoRepresentante.delaEstacion = estacion_origen
            nombramientoRepresentante.save()

            data = {
                'success': True, 
                'message': 'Notificación Representante creada con éxito.', 
                'nombramiento_id': nombramientoRepresentante.id
            }
            return JsonResponse(data, status=200)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)
        

    def get(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero 
        ultimo_registro = ExtranjeroDefensoria.objects.filter(nup=no_proceso).order_by('-fechaHora').first()
        numero_oficio = ultimo_registro.oficio if ultimo_registro else None
        defensoria = ultimo_registro.defensoria if ultimo_registro else None

        initial_data = {
            'delaEstacion': extranjero.deLaEstacion,
            'nup':no_proceso,
            'oficio': numero_oficio,  # Establecer el número de oficio inicial
            'defensoria': defensoria,  # Establecer la defensoría inicial

        }

        form = NombramientoRepresentanteInternoForm(initial=initial_data)

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
        form.fields['autoridadActuante'].queryset = autoridades

        context = {
            'form': form,
            'nup_id': nup_id,
            'extranjero': extranjero,
            'navbar': 'Notificaciones',
            'seccion': 'defensoria',
        }
        
        return render(request, 'defensoria/crearNombramientoInterno.html', context)

class CrearNombramientoExterno(View):

    def post(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        form = NombramientoRepresentanteExternoForm(request.POST)
        if form.is_valid():
            nombramientoRepresentante = form.save(commit=False)
            nombramientoRepresentante.nup = no_proceso
            estacion_origen = no_proceso.extranjero.deLaEstacion
            nombramientoRepresentante.delaEstacion = estacion_origen
            nombramientoRepresentante.es_representante_externo = True  # Aquí se establece el campo en True
            nombramientoRepresentante.save()

            data = {
                'success': True, 
                'message': 'Notificación Consular creada con éxito.', 
                'nombramiento_id': nombramientoRepresentante.id
            }
            return JsonResponse(data, status=200)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)
        

    def get(self, request, nup_id, *args, **kwargs):
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero 
        ultimo_registro = ExtranjeroDefensoria.objects.filter(nup=no_proceso).order_by('-fechaHora').first()
        numero_oficio = ultimo_registro.oficio if ultimo_registro else None
        defensoria = ultimo_registro.defensoria if ultimo_registro else None

        initial_data = {
            'delaEstacion': extranjero.deLaEstacion,
            'nup':no_proceso,
            'oficio': numero_oficio,  # Establecer el número de oficio inicial
            'defensoria': defensoria,  # Establecer la defensoría inicial

        }

        form = NombramientoRepresentanteExternoForm(initial=initial_data)

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
        form.fields['autoridadActuante'].queryset = autoridades

        context = {
            'form': form,
            'nup_id': nup_id,
            'extranjero': extranjero,
            'navbar': 'Notificaciones',
            'seccion': 'defensoria',
        }
        
        return render(request, 'defensoria/crearNombramientoExterno.html', context)



def generar_qr_firmas_nombramiento_Externo(request, nombramiento_externo_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}notificaciones/firma_autoridad_actuante_nombramiento_ext/{nombramiento_externo_id}/"
    elif tipo_firma == "representanteLegal":
        url = f"{base_url}notificaciones/firma_representante_legal_nombramiento_ext/{nombramiento_externo_id}/"
    elif tipo_firma == "traductor":
        url = f"{base_url}notificaciones/firma_traductor_nombramiento_ext/{nombramiento_externo_id}/"
    elif tipo_firma == "extranjero":
        url = f"{base_url}notificaciones/firma_extranjero_nombramiento_ext/{nombramiento_externo_id}/"
    elif tipo_firma == "testigo1":
        url = f"{base_url}notificaciones/firma_testigo1_nombramiento_ext/{nombramiento_externo_id}/"
    elif tipo_firma == "testigo2":
        url = f"{base_url}notificaciones/firma_testigo2_nombramiento_ext/{nombramiento_externo_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response



def generar_qr_firmas_nombramiento_Interno(request, nombramiento_interno_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}notificaciones/firma_autoridad_actuante_nombramiento/{nombramiento_interno_id}/"
    elif tipo_firma == "representanteLegal":
        url = f"{base_url}notificaciones/firma_representante_legal_nombramiento/{nombramiento_interno_id}/"
    elif tipo_firma == "traductor":
        url = f"{base_url}notificaciones/firma_traductor_nombramiento/{nombramiento_interno_id}/"
    elif tipo_firma == "extranjero":
        url = f"{base_url}notificaciones/firma_extranjero_nombramiento/{nombramiento_interno_id}/"
    elif tipo_firma == "testigo1":
        url = f"{base_url}notificaciones/firma_testigo1_nombramiento/{nombramiento_interno_id}/"
    elif tipo_firma == "testigo2":
        url = f"{base_url}notificaciones/firma_testigo2_nombramiento/{nombramiento_interno_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


def firma_autoridad_actuante_nom_ext(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    firma, created = FirmaNombramientoExterno.objects.get_or_create(nombramientoExterno=nombramiento_externo)  

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteNombramientoExternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{nombramiento_externo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteNombramientoExternoForm()
    return render(request, 'firma/firma_autoridad_actuante.html', {'form': form, 'nombramiento_externo_id': nombramiento_externo_id})




def firma_representante_legal_nom_ext(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    firma, created = FirmaNombramientoExterno.objects.get_or_create(nombramientoExterno=nombramiento_externo)  # Usar comparecencia aquí
    if firma.firmaRepresentanteLegal:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaRepresentanteLegalNombramientoExternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaRepresentanteLegal']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr)) 
            file_name = f"firmaRepresentanteLegal_{nombramiento_externo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaRepresentanteLegal.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaRepresentanteLegalNombramientoExternoForm()

    return render(request, 'firma/firma_representante_legal.html', {'form': form, 'nombramiento_externo_id': nombramiento_externo_id})


def firma_traductor_nom_ext(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    firma, created = FirmaNombramientoExterno.objects.get_or_create(nombramientoExterno=nombramiento_externo)  # Usar comparecencia aquí
    if firma.firmaTraductor:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTraductorNombramientoExternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaTraductor']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaTraductor_{nombramiento_externo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaTraductor.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTraductorNombramientoExternoForm()

    return render(request, 'firma/firma_traductor.html', {'form': form, 'nombramiento_externo_id': nombramiento_externo_id})

def firma_extranjero_nom_ext(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    firma, created = FirmaNombramientoExterno.objects.get_or_create(nombramientoExterno=nombramiento_externo)  # Usar comparecencia aquí
    if firma.firmaExtranjero:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaExtranjeroNombramientoExternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaExtranjero']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaExtranjero_{nombramiento_externo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaExtranjero.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaExtranjeroNombramientoExternoForm()
    return render(request, 'firma/firma_extranjero.html', {'form': form, 'nombramiento_externo_id': nombramiento_externo_id})


def firma_testigo1_nom_ext(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    firma, created = FirmaNombramientoExterno.objects.get_or_create(nombramientoExterno=nombramiento_externo)  # Usar comparecencia aquí
    if firma.firmaTestigo1:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTestigo1NombramientoExternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaTestigo1']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaTestigo1_{nombramiento_externo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaTestigo1.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigo1NombramientoExternoForm()

    return render(request, 'firma/firma_testigo1.html', {'form': form, 'nombramiento_externo_id': nombramiento_externo_id})

def firma_testigo2_nom_ext(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    firma, created = FirmaNombramientoExterno.objects.get_or_create(nombramientoExterno=nombramiento_externo)

    if firma.firmaTestigo2:
        return redirect('firma_existente_acuerdos')  # Asumiendo que tienes una URL para este caso

    if request.method == 'POST':
        form = FirmaTestigo2NombramientoExternoForm(request.POST, request.FILES)
        if form.is_valid():
            # Código para procesar y guardar la firma
            data_url = form.cleaned_data['firmaTestigo2']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaTestigo2_{nombramiento_externo_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaTestigo2.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))  # Asegúrate de que esta URL esté definida
    else:
        form = FirmaTestigo2NombramientoExternoForm()

    return render(request, 'firma/firma_testigo2.html', {'form': form, 'nombramiento_externo_id': nombramiento_externo_id})

#creacion de firmas para nombramiento interno
def firma_autoridad_actuante_nom(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    firma, created = FirmaNombramientoInterno.objects.get_or_create(nombramientoInterno=nombramiento_interno)  

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteNombramientoInternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{nombramiento_interno_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteNombramientoInternoForm()
    return render(request, 'firma/firma_autoridad_actuante.html', {'form': form, 'nombramiento_interno_id': nombramiento_interno_id})




def firma_representante_legal_nom(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    firma, created = FirmaNombramientoInterno.objects.get_or_create(nombramientoInterno=nombramiento_interno)  # Usar comparecencia aquí
    if firma.firmaRepresentanteLegal:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaRepresentanteLegalNombramientoInternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaRepresentanteLegal']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr)) 
            file_name = f"firmaRepresentanteLegal_{nombramiento_interno_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaRepresentanteLegal.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaRepresentanteLegalNombramientoInternoForm()

    return render(request, 'firma/firma_representante_legal.html', {'form': form, 'nombramiento_interno_id': nombramiento_interno_id})


def firma_traductor_nom(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    firma, created = FirmaNombramientoInterno.objects.get_or_create(nombramientoInterno=nombramiento_interno)  # Usar comparecencia aquí
    if firma.firmaTraductor:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTraductorNombramientoInternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaTraductor']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaTraductor_{nombramiento_interno_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaTraductor.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTraductorNombramientoInternoForm()

    return render(request, 'firma/firma_traductor.html', {'form': form, 'nombramiento_interno_id': nombramiento_interno_id})

def firma_extranjero_nom(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    firma, created = FirmaNombramientoInterno.objects.get_or_create(nombramientoInterno=nombramiento_interno)  # Usar comparecencia aquí
    if firma.firmaExtranjero:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaExtranjeroNombramientoInternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaExtranjero']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaExtranjero_{nombramiento_interno_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaExtranjero.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaExtranjeroNombramientoInternoForm()
    return render(request, 'firma/firma_extranjero.html', {'form': form, 'nombramiento_interno_id': nombramiento_interno_id})


def firma_testigo1_nom(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    firma, created = FirmaNombramientoInterno.objects.get_or_create(nombramientoInterno=nombramiento_interno)  # Usar comparecencia aquí
    if firma.firmaTestigo1:
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTestigo1NombramientoInternoForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaTestigo1']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaTestigo1_{nombramiento_interno_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaTestigo1.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigo1NombramientoInternoForm()

    return render(request, 'firma/firma_testigo1.html', {'form': form, 'nombramiento_interno_id': nombramiento_interno_id})

def firma_testigo2_nom(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    firma, created = FirmaNombramientoInterno.objects.get_or_create(nombramientoInterno=nombramiento_interno)

    if firma.firmaTestigo2:
        return redirect('firma_existente_acuerdos')  # Asumiendo que tienes una URL para este caso

    if request.method == 'POST':
        form = FirmaTestigo2NombramientoInternoForm(request.POST, request.FILES)
        if form.is_valid():
            # Código para procesar y guardar la firma
            data_url = form.cleaned_data['firmaTestigo2']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            file_name = f"firmaTestigo2_{nombramiento_interno_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)
            firma.firmaTestigo2.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))  # Asegúrate de que esta URL esté definida
    else:
        form = FirmaTestigo2NombramientoInternoForm()

    return render(request, 'firma/firma_testigo2.html', {'form': form, 'nombramiento_interno_id': nombramiento_interno_id})


class firmExistente(TemplateView):
    template_name='firma/firma_exixtente.html'


@csrf_exempt
def verificar_firma_autoridad_actuante_nom_ext(request, nombramiento_externo_id):
    try:
        firma = FirmaNombramientoExterno.objects.get(nombramientoExterno_id=nombramiento_externo_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoExterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_representante_legal_nom_ext(request, nombramiento_externo_id):
    try:
        firma = FirmaNombramientoExterno.objects.get(nombramientoExterno_id=nombramiento_externo_id)
        if firma.firmaRepresentanteLegal:
            image_url = request.build_absolute_uri(firma.firmaRepresentanteLegal.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Representante Legal encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoExterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Representante Legal aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_traductor_nom_ext(request, nombramiento_externo_id):
    try:
        firma = FirmaNombramientoExterno.objects.get(nombramientoExterno_id=nombramiento_externo_id)
        if firma.firmaTraductor:
            image_url = request.build_absolute_uri(firma.firmaTraductor.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Traductor encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoExterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Traductor aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_extranjero_nom_ext(request, nombramiento_externo_id):
    try:
        firma = FirmaNombramientoExterno.objects.get(nombramientoExterno_id=nombramiento_externo_id)
        if firma.firmaExtranjero:
            image_url = request.build_absolute_uri(firma.firmaExtranjero.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Extranjero encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoExterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Extranjero aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo1_nom_ext(request, nombramiento_externo_id):
    try:
        firma = FirmaNombramientoExterno.objects.get(nombramientoExterno_id=nombramiento_externo_id)
        if firma.firmaTestigo1:
            image_url = request.build_absolute_uri(firma.firmaTestigo1.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 1 encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoExterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 1 aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo2_nom_ext(request, nombramiento_externo_id):
    try:
        firma = FirmaNombramientoExterno.objects.get(nombramientoExterno_id=nombramiento_externo_id)
        if firma.firmaTestigo2:
            image_url = request.build_absolute_uri(firma.firmaTestigo2.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 2 encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoExterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 2 aún no registrada'}, status=404)


# verificar firma de nombramiento interno

@csrf_exempt
def verificar_firma_autoridad_actuante_nom(request, nombramiento_interno_id):
    try:
        firma = FirmaNombramientoInterno.objects.get(nombramientoInterno_id=nombramiento_interno_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoInterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_representante_legal_nom(request, nombramiento_interno_id):
    try:
        firma = FirmaNombramientoInterno.objects.get(nombramientoInterno_id=nombramiento_interno_id)
        if firma.firmaRepresentanteLegal:
            image_url = request.build_absolute_uri(firma.firmaRepresentanteLegal.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Representante Legal encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoInterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Representante Legal aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_traductor_nom(request, nombramiento_interno_id):
    try:
        firma = FirmaNombramientoInterno.objects.get(nombramientoInterno_id=nombramiento_interno_id)
        if firma.firmaTraductor:
            image_url = request.build_absolute_uri(firma.firmaTraductor.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Traductor encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoInterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Traductor aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_extranjero_nom(request, nombramiento_interno_id):
    try:
        firma = FirmaNombramientoInterno.objects.get(nombramientoInterno_id=nombramiento_interno_id)
        if firma.firmaExtranjero:
            image_url = request.build_absolute_uri(firma.firmaExtranjero.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Extranjero encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoInterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Extranjero aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo1_nom(request, nombramiento_interno_id):
    try:
        firma = FirmaNombramientoInterno.objects.get(nombramientoInterno_id=nombramiento_interno_id)
        if firma.firmaTestigo1:
            image_url = request.build_absolute_uri(firma.firmaTestigo1.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 1 encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoInterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 1 aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo2_nom(request, nombramiento_interno_id):
    try:
        firma = FirmaNombramientoInterno.objects.get(nombramientoInterno_id=nombramiento_interno_id)
        if firma.firmaTestigo2:
            image_url = request.build_absolute_uri(firma.firmaTestigo2.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 2 encontrada',
                'image_url': image_url
            })
    except FirmaNombramientoInterno.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 2 aún no registrada'}, status=404)


# Obtener datos de forma externak
def obtener_datos_nombramiento_externo(request, nombramiento_externo_id):
    nombramiento_externo = get_object_or_404(nombramientoRepresentante, pk=nombramiento_externo_id)
    nup = nombramiento_externo.nup

    datos = {
        'nombreAutoridadActuante': f"{nombramiento_externo.autoridadActuante.autoridad.nombre} {nombramiento_externo.autoridadActuante.autoridad.apellidoPaterno} {nombramiento_externo.autoridadActuante.autoridad.apellidoMaterno or ''}".strip() if nombramiento_externo.autoridadActuante else '',
        # 'nombreRepresentanteLegal': f"{nombramiento_externo.representanteLegal.nombre} {nombramiento_externo.representanteLegal.apellido_paterno} {nombramiento_externo.representanteLegal.apellido_materno or ''}".strip() if nombramiento_externo.representanteLegal else '',
        'nombreRepresentanteLegal': nombramiento_externo.representanteLegalExterno if nombramiento_externo.representanteLegalExterno else '',
        'nombreTraductor': f"{nombramiento_externo.traductor.nombre} {nombramiento_externo.traductor.apellido_paterno} {nombramiento_externo.traductor.apellido_materno or ''}".strip() if nombramiento_externo.traductor else '',
        'nombreTestigo1': nombramiento_externo.testigo1,
        'nombreTestigo2': nombramiento_externo.testigo2,
        'nombreExtranjero': f"{nup.extranjero.nombreExtranjero} {nup.extranjero.apellidoPaternoExtranjero} {nup.extranjero.apellidoMaternoExtranjero or ''}".strip()
    }

    return JsonResponse(datos)


def obtener_datos_nombramiento_interno(request, nombramiento_interno_id):
    nombramiento_interno = get_object_or_404(nombramientoRepresentante, pk=nombramiento_interno_id)
    nup = nombramiento_interno.nup

    datos = {
        'nombreAutoridadActuante': f"{nombramiento_interno.autoridadActuante.autoridad.nombre} {nombramiento_interno.autoridadActuante.autoridad.apellidoPaterno} {nombramiento_interno.autoridadActuante.autoridad.apellidoMaterno or ''}".strip() if nombramiento_interno.autoridadActuante else '',
        'nombreRepresentanteLegal': f"{nombramiento_interno.representanteLegal.nombre} {nombramiento_interno.representanteLegal.apellido_paterno} {nombramiento_interno.representanteLegal.apellido_materno or ''}".strip() if nombramiento_interno.representanteLegal else '',
        'nombreTraductor': f"{nombramiento_interno.traductor.nombre} {nombramiento_interno.traductor.apellido_paterno} {nombramiento_interno.traductor.apellido_materno or ''}".strip() if nombramiento_interno.traductor else '',
        'nombreTestigo1': nombramiento_interno.testigo1,
        'nombreTestigo2': nombramiento_interno.testigo2,
        'nombreExtranjero': f"{nup.extranjero.nombreExtranjero} {nup.extranjero.apellidoPaternoExtranjero} {nup.extranjero.apellidoMaternoExtranjero or ''}".strip()
    }

    return JsonResponse(datos)