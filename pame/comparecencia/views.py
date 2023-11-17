from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from vigilancia.models import NoProceso, Extranjero, AutoridadesActuantes, AsignacionRepresentante
# Create your views here.
from django.db.models import OuterRef, Subquery,Exists
from django.shortcuts import get_object_or_404

from .models import Comparecencia
from django.views.generic import ListView, CreateView, View, TemplateView
from django.urls import reverse_lazy
from .forms import ComparecenciaForm
from django.db.models import Q
from django.http import JsonResponse
from catalogos.models import Traductores
import qrcode
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.http import HttpResponse, HttpResponseNotFound

from .forms import (FirmaAutoridadActuanteForm, FirmaRepresentanteLegalForm, 
                    FirmaTraductorForm, FirmaExtranjeroForm, 
                    FirmaTestigo1Form, FirmaTestigo2Form)
from .models import FirmaComparecencia
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.views.decorators.csrf import csrf_exempt

def homeComparecencia(request):
    return render(request,"homeComparecencia.html")



class listExtranjerosComparecencia(ListView):
    model=NoProceso
    template_name="comparecencia/listExtranjerosComparecencia.html"
    context_object_name = "extranjeros"

    def get_queryset(self):
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')
            
            representantes_asignados = AsignacionRepresentante.objects.filter(
                no_proceso=OuterRef('pk')
            )
            
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

            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id],
                extranjero__deLaEstacion=estacion_usuario
            ).annotate(
                tiene_asignacion=Exists(representantes_asignados)
            )

            tiene_representante = self.request.GET.get('con_representante', None)
            
            if tiene_representante == 'no':
                queryset = queryset.filter(tiene_asignacion=False)
            elif tiene_representante == 'si':
                queryset = queryset.filter(tiene_asignacion=True)
            else:
                queryset = queryset.filter(tiene_asignacion=True)

            return queryset

    def get_context_data(self, **kwargs): 
            context = super().get_context_data(**kwargs)
            context['navbar'] = 'comparecencia'  # Cambia esto según la página activa
            context['seccion'] = 'comparecencia'
    
            return context
    

class CrearComparecencia(CreateView):
    model = Comparecencia
    form_class = ComparecenciaForm
    template_name = 'comparecencia/crearComparecencia.html'
    success_url = reverse_lazy('lisExtranjerosComparecencia')  

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        nup_id = self.kwargs.get('nup_id')
        no_proceso = NoProceso.objects.get(nup=nup_id)
        extranjero = no_proceso.extranjero
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
        form.fields['traductor'].queryset = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)

        return form
    def get_initial(self):
        initial = super(CrearComparecencia, self).get_initial()
        nup_id = self.kwargs.get('nup_id')
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero
        initial['nup'] = no_proceso
        initial['estadoCivil'] = extranjero.estado_Civil
        initial['escolaridad'] = extranjero.grado_academico
        initial['ocupacion'] = extranjero.ocupacion
        initial['nacionalidad'] = extranjero.nacionalidad.nombre  
        initial['nombrePadre'] = extranjero.nombreDelPadre
        initial['nombreMadre'] = extranjero.nombreDelaMadre
        initial['nacionalidadPadre'] = extranjero.nacionalidad_Padre.nombre if extranjero.nacionalidad_Padre else ''
        initial['nacionalidadMadre'] = extranjero.nacionalidad_Madre.nombre if extranjero.nacionalidad_Madre else ''
        return initial
    def form_valid(self, form):
        form.instance.nup = get_object_or_404(NoProceso, nup=self.kwargs.get('nup_id'))
        return super(CrearComparecencia, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            nup_id = self.kwargs.get('nup_id')
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            context['extranjero'] = no_proceso.extranjero
            context['navbar'] = 'comparecencia'  
            context['seccion'] = 'comparecencia'
            return context
    

class CrearComparecenciaAjax(View):
    def post(self, request, nup_id, *args, **kwargs):
        form = ComparecenciaForm(request.POST)
        if form.is_valid():
            comparecencia = form.save(commit=False)
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            comparecencia.nup = no_proceso
            comparecencia.save()
            data = {'success': True, 'message': 'Comparecencia creada con éxito.', 'comparecencia_id': comparecencia.id}
            return JsonResponse(data, status=200)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)

    def get(self, request, nup_id, *args, **kwargs):
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            extranjero = no_proceso.extranjero
            asignacion_rep_legal = AsignacionRepresentante.objects.filter(no_proceso=no_proceso).first()
   
            # Crear el formulario y establecer valores iniciales
  
            initial_data = {
            'estadoCivil': extranjero.estado_Civil,
            'escolaridad': extranjero.grado_academico,
            'ocupacion': extranjero.ocupacion,
            'nacionalidad': extranjero.nacionalidad.nombre,
            'nombrePadre': extranjero.nombreDelPadre,
            'nombreMadre': extranjero.nombreDelaMadre,
            'nacionalidadPadre': extranjero.nacionalidad_Padre.nombre if extranjero.nacionalidad_Padre else '',
            'nacionalidadMadre': extranjero.nacionalidad_Madre.nombre if extranjero.nacionalidad_Madre else '',
            'DomicilioPais': extranjero.domicilio,
            'lugarOrigen': extranjero.origen,


            }
            if asignacion_rep_legal:
                initial_data['representanteLegal'] = asignacion_rep_legal.representante_legal

            form = ComparecenciaForm(initial=initial_data)

            # Filtrar las autoridades actuantes según la lógica proporcionada
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

            # Establecer el queryset de autoridades actuantes y traductor
            form.fields['autoridadActuante'].queryset = autoridades
            form.fields['traductor'].queryset = Traductores.objects.filter(estacion=extranjero.deLaEstacion)

            # Preparar el contexto para la plantilla
            context = {
                'form': form,
                'nup_id': nup_id,
                'extranjero': extranjero,
                'navbar': 'comparecencia',
                'seccion': 'comparecencia',
            }
            return render(request, 'comparecencia/crearComparecencia1.html', context)
        
def generar_qr_firmas(request, comparecencia_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}comparecencia/firma_autoridad_actuante/{comparecencia_id}/"
    elif tipo_firma == "representanteLegal":
        url = f"{base_url}comparecencia/firma_representante_legal/{comparecencia_id}/"
    elif tipo_firma == "traductor":
        url = f"{base_url}comparecencia/firma_traductor/{comparecencia_id}/"
    elif tipo_firma == "extranjero":
        url = f"{base_url}comparecencia/firma_extranjero/{comparecencia_id}/"
    elif tipo_firma == "testigo1":
        url = f"{base_url}comparecencia/firma_testigo1/{comparecencia_id}/"
    elif tipo_firma == "testigo2":
        url = f"{base_url}comparecencia/firma_testigo2/{comparecencia_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante(request, comparecencia_id):
    comparecencia = get_object_or_404(Comparecencia, pk=comparecencia_id)
    firma, created = FirmaComparecencia.objects.get_or_create(comparecencia=comparecencia)  # Usar comparecencia aquí

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{comparecencia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteForm()
    return render(request, 'firma/firma_autoridad_actuante.html', {'form': form, 'comparecencia_id': comparecencia_id})


def firma_representante_legal(request, comparecencia_id):
    comparecencia = get_object_or_404(Comparecencia, pk=comparecencia_id)
    firma, created = FirmaComparecencia.objects.get_or_create(comparecencia=comparecencia)  # Usar comparecencia aquí
    if firma.firmaRepresentanteLegal:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaRepresentanteLegalForm(request.POST, request.FILES)
        if form.is_valid():
        
            data_url = form.cleaned_data['firmaRepresentanteLegal']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaRepresentanteLegal_{comparecencia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaRepresentanteLegal.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaRepresentanteLegalForm()

    return render(request, 'firma/firma_representante_legal.html', {'form': form, 'comparecencia_id': comparecencia_id})


def firma_traductor(request, comparecencia_id):
    comparecencia = get_object_or_404(Comparecencia, pk=comparecencia_id)
    firma, created = FirmaComparecencia.objects.get_or_create(comparecencia=comparecencia)  # Usar comparecencia aquí
    if firma.firmaTraductor:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTraductorForm(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaTraductor']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaTraductor_{comparecencia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTraductor.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTraductorForm()

    return render(request, 'firma/firma_traductor.html', {'form': form, 'comparecencia_id': comparecencia_id})

def firma_extranjero(request, comparecencia_id):
    comparecencia = get_object_or_404(Comparecencia, pk=comparecencia_id)
    firma, created = FirmaComparecencia.objects.get_or_create(comparecencia=comparecencia)  # Usar comparecencia aquí
    if firma.firmaExtranjero:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaExtranjeroForm(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaExtranjero']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaExtranjero_{comparecencia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaExtranjero.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaExtranjeroForm()

    return render(request, 'firma/firma_extranjero.html', {'form': form, 'comparecencia_id': comparecencia_id})


def firma_testigo1(request, comparecencia_id):
    comparecencia = get_object_or_404(Comparecencia, pk=comparecencia_id)
    firma, created = FirmaComparecencia.objects.get_or_create(comparecencia=comparecencia)  # Usar comparecencia aquí
    if firma.firmaTestigo1:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTestigo1Form(request.POST, request.FILES)
        if form.is_valid():

            data_url = form.cleaned_data['firmaTestigo1']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaTestigo1_{comparecencia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTestigo1.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigo1Form()

    return render(request, 'firma/firma_testigo1.html', {'form': form, 'comparecencia_id': comparecencia_id})


def firma_testigo2(request, comparecencia_id):
    comparecencia = get_object_or_404(Comparecencia, pk=comparecencia_id)
    firma, created = FirmaComparecencia.objects.get_or_create(comparecencia=comparecencia)  # Usar comparecencia aquí
    if firma.firmaTestigo2:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTestigo2Form(request.POST, request.FILES)
        if form.is_valid():
            data_url = form.cleaned_data['firmaTestigo2']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaTestigo2_{comparecencia_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTestigo2.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigo2Form()

    return render(request, 'firma/firma_testigo2.html', {'form': form, 'comparecencia_id': comparecencia_id})


class firmExistente(TemplateView):
    template_name='firma/firma_exixtente.html'


@csrf_exempt
def verificar_firma_autoridad_actuante(request, comparecencia_id):
    try:
        firma = FirmaComparecencia.objects.get(comparecencia_id=comparecencia_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaComparecencia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_representante_legal(request, comparecencia_id):
    try:
        firma = FirmaComparecencia.objects.get(comparecencia_id=comparecencia_id)
        if firma.firmaRepresentanteLegal:
            image_url = request.build_absolute_uri(firma.firmaRepresentanteLegal.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Representante Legal encontrada',
                'image_url': image_url
            })
    except FirmaComparecencia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Representante Legal aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_traductor(request, comparecencia_id):
    try:
        firma = FirmaComparecencia.objects.get(comparecencia_id=comparecencia_id)
        if firma.firmaTraductor:
            image_url = request.build_absolute_uri(firma.firmaTraductor.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Traductor encontrada',
                'image_url': image_url
            })
    except FirmaComparecencia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Traductor aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_extranjero(request, comparecencia_id):
    try:
        firma = FirmaComparecencia.objects.get(comparecencia_id=comparecencia_id)
        if firma.firmaExtranjero:
            image_url = request.build_absolute_uri(firma.firmaExtranjero.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Extranjero encontrada',
                'image_url': image_url
            })
    except FirmaComparecencia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Extranjero aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo1(request, comparecencia_id):
    try:
        firma = FirmaComparecencia.objects.get(comparecencia_id=comparecencia_id)
        if firma.firmaTestigo1:
            image_url = request.build_absolute_uri(firma.firmaTestigo1.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 1 encontrada',
                'image_url': image_url
            })
    except FirmaComparecencia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 1 aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo2(request, comparecencia_id):
    try:
        firma = FirmaComparecencia.objects.get(comparecencia_id=comparecencia_id)
        if firma.firmaTestigo2:
            image_url = request.build_absolute_uri(firma.firmaTestigo2.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 2 encontrada',
                'image_url': image_url
            })
    except FirmaComparecencia.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 2 aún no registrada'}, status=404)
