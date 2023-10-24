import base64
from pathlib import Path
from typing import Any
from django import forms
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Extranjero, PuestaDisposicionAC, PuestaDisposicionINM, Biometrico, Acompanante, Proceso,descripcion, NoProceso
from .models import Extranjero, Proceso, PuestaDisposicionAC, PuestaDisposicionINM, Biometrico, Acompanante, UserFace
from pertenencias.models import Inventario
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView,DetailView, TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import extranjeroFormsAC, extranjeroFormsInm, puestDisposicionINMForm, puestaDisposicionACForm, BiometricoFormINM, BiometricoFormAC, AcompananteForm, editExtranjeroINMForm, editExtranjeroACForms,descripcionForms
from .forms import BiometricoFormVP
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalogos.models import Estacion, Relacion
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core import serializers
from django.http import JsonResponse
import json
from django.db.models import Count
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponseRedirect
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
import os
import time
from io import BytesIO
from traslados.models import ExtranjeroTraslado
from django.core.files.uploadedfile import InMemoryUploadedFile
from llamadasTelefonicas.models import Notificacion
from pertenencias.models import EnseresBasicos
import sys
import pickle

from django.http import JsonResponse
from django.views import View
from traslados.models import Traslado, ExtranjeroTraslado
from .forms import TrasladoForm, UserFaceForm

from .helpers import image_to_pdf
from PIL import Image

import os
import cv2
import numpy as np
from django.core.files.base import ContentFile
from .forms import CompareFacesForm, SearchFaceForm
import face_recognition
import time  # Importa el módulo de time
from .forms import FirmaExtranjeroForm

from generales.mixins import HandleFileMixin

from django.db import transaction
from biometricos.models import UserFace1

from juridico.models import NotificacionDerechos

import qrcode
from vigilancia.models import Firma
from .forms import FirmaForm
from django.core.files.base import ContentFile

class CreatePermissionRequiredMixin(UserPassesTestMixin):
    login_url = '/permisoDenegado/'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions_required = kwargs.get('permissions_required', {})

    def test_func(self):
        user = self.request.user
        for permission, codename in self.permissions_required.items():
            if not user.has_perm(codename):
                raise PermissionDenied(f"No tienes el permiso necesario: {permission}")
        return True
   
    def test_func(self):
        return all(self.request.user.has_perm(perm) for perm in self.permission_required.values())
 
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # Si el usuario está autenticado pero no tiene el permiso, redirige a una página de acceso denegado
            return redirect('permisoDenegado')  # Cambia 'acceso_denegado' a la URL adecuada
        else:
            # Si el usuario no está autenticado, redirige a la página de inicio de sesión
            return redirect(self.login_url)


def sesionfinal(request):
    return render(request, 'finalizarsesion.html')

class firma(TemplateView):
    template_name= 'modal/firma.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Recuperar el ID del extranjero desde los argumentos de la URL
        extranjero_id = self.kwargs.get('extranjero_id')
        context['extramjero_id'] = extranjero_id
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = get_object_or_404(Extranjero, id=extranjero_id)
        nombre = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero +" "+ extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        return context
    

def guardar_firma(request, extranjero_id):
    extranjero = get_object_or_404(Biometrico, pk=extranjero_id)

    if request.method == 'POST':
        form = FirmaExtranjeroForm(request.POST, request.FILES)

        if form.is_valid():
            extranjero.firmaExtranjero = form.cleaned_data.get('imagen_firma')
            extranjero.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Formulario no válido'})

    return JsonResponse({'error': 'Solicitud no válida'})



# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "home/homeSeguridadGeneral.html",{'navbar':'home'})



def ejemplo(request):
    return render (request, "prueba.html")


def homeSeguridadResponsable(request):
    return render (request, "home/homeSeguridadResponsable.html")


def addAutoridadCompetente(request):
    return render(request, "addAutoridadCompetente.html")



def addHospedaje(request):
    return render(request, "addHospedaje.html")


def addTraslado(request):
    return render(request, "addTraslado.html")

def homePuestaINM (request):
    return render(request, "home/puestas/homePuestaINM.html")

def homePuestaVP (request):
    return render(request, "home/puestas/homePuestaVP.html")

#------------------------ Puesta por INM-----------------------------
class inicioINMList(ListView):
    model = PuestaDisposicionINM          
    template_name = "puestaINM/homePuestaINM.html" 
    context_object_name = 'puestasinm'

    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = PuestaDisposicionINM.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa

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

class estadisticasPuestaINM(ListView):
    model=PuestaDisposicionINM
    template_name = "puestaINM/estadisticasINM.html" 
    context_object_name = 'puestainm'

    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = PuestaDisposicionINM.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context
    
    




class createPuestaINM(HandleFileMixin,CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicioninm',
    }
    model = PuestaDisposicionINM               
    form_class = puestDisposicionINMForm      
    template_name = 'puestaINM/createPuestaINM.html'  
    success_url = reverse_lazy('homePuestaINM')

    def get_initial(self):
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            UsuarioId = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        # Generar el número con formato automáticamente
        ultimo_registro = PuestaDisposicionINM.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.identificadorProceso.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'{numero_identificador}/{datetime.now().year}/{UsuarioId}/{ultimo_numero + 1:04d}'

        initial['identificadorProceso'] = nuevo_numero
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'La puesta de disposición se ha creado con éxito.')
        return super().get_success_url()
    
    def form_valid(self, form):
        instance = form.save()  
        self.handle_file(instance,'oficioPuesta')
        self.handle_file(instance,'oficioComision')
        return super(createPuestaINM, self).form_valid(form)

class createExtranjeroINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'puestaINM/crearExtranjeroINM.html'     
    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        if self.object.viajaSolo:
            messages.success(self.request, 'Extranjero Creado con Éxito.')
            return reverse('agregar_biometricoINM', args=[extranjero_id])
        else:
            messages.success(self.request, 'Extranjero Creado con Éxito.')
            return reverse('listAcompanantesINM', args=[extranjero_id, puesta_id])
                
    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
            numero_identificador_puesta = puesta.identificadorProceso
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass

        return {'deLaPuestaIMN': puesta, 'deLaEstacion': estacion, 'viajaSolo': viaja_solo}
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        if estacion:
            estacion.capacidad -= 1
            estacion.save()  
        nuevo_consecutivo = 1  
        status_default = 'Activo' 
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
        except Usuario.DoesNotExist:
            pass
        with transaction.atomic():
            extranjero = form.save(commit=False)
            extranjero.puesta = puesta

            # Guarda el objeto para obtener un ID asignado
            extranjero.save()

            # Asigna el númeroExtranjero basado en el ID del registro
            year_actual = extranjero.fechaRegistro.year  # Obtiene el año actual
            nomenclatura = usuario_data.estancia.identificador  # Tu nomenclatura personalizada
            numero_extranjero = f"{year_actual}/{nomenclatura}/{extranjero.id}"
            extranjero.numeroExtranjero = numero_extranjero

            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"

            # Crea un registro en la tabla NoProceso
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = status_default,
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                name, ext = os.path.splitext(file.name)
                
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa

        return context
    

class listarExtranjeros(ListView):
    model = Extranjero
    template_name = 'puestaINM/listExtranjeros.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        estado = self.request.GET.get('estado_filtrado', 'activo') 
        queryset = Extranjero.objects.filter(deLaPuestaIMN_id=puesta_id).order_by('nombreExtranjero')

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset

    
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     puesta_id = self.kwargs['puesta_id']
     puesta = PuestaDisposicionINM.objects.get(id=puesta_id)  

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
                    extranjero.hora_aceptacion = None
                    extranjero.estacion_notificacion = None

     for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_enseres = False

            if ultimo_nup:
                enseres = EnseresBasicos.objects.filter(nup=ultimo_nup).first()
                if enseres:
                    tiene_enseres = True

            extranjero.tiene_enseres = tiene_enseres

     for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_inventario = False

            if ultimo_nup:
                inventario = Inventario.objects.filter(nup=ultimo_nup).first()
                if inventario:
                    tiene_inventario = True

            extranjero.tiene_inventario = tiene_inventario

     context['puesta'] = puesta
     context['navbar'] = 'seguridad'
     context['seccion'] = 'seguridadINM'
     return context
     
class EditarExtranjeroINM(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroINMForm
    template_name = 'puestaINM/editarExtranjeroINM.html'

    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
        return reverse('listarExtranjeros', args=[self.object.deLaPuestaIMN.id])
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)  # Obtén el extranjero original antes de modificar
        instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta'] = self.object.deLaPuestaIMN
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Obtén el registro que se va a editar
        registro = self.get_object()

        # Calcula la diferencia de tiempo
        diferencia = timezone.now() - registro.horaRegistro

        # Define el límite de tiempo permitido para la edición (dos días en este caso)
        limite_de_tiempo = timedelta(days=1)

        if diferencia > limite_de_tiempo:
            # Si han pasado más de tres minutos, muestra un mensaje de error y redirige
            messages.error(request, "No puedes editar este registro después de 1 dia.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la URL actual o a la página de inicio si no se puede determinar la URL actual

        return super().dispatch(request, *args, **kwargs)
    
class EditarExtranjeroINMProceso(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroINMForm
    template_name = 'puestaINM/editarExtranjeroINM.html'
    def get_initial(self):
        initial = super().get_initial()
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        initial['deLaPuestaIMN']=puesta
        initial['deLaPuestaVP']=None
        initial['deLaPuestaAC'] =None
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        return initial
    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
        return reverse('listarExtranjeros', args=[self.object.deLaPuestaIMN.id])
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)  # Obtén el extranjero original antes de modificar
        puesta_id = self.request.GET.get('puesta_id', None)

      
        if puesta_id:
            extranjero.deLaPuestaIMN_id = puesta_id

        with transaction.atomic():
            # Cálculo del nuevo consecutivo
            extranjeros_con_mismo_id = Extranjero.objects.filter(id=extranjero.id)
            if extranjeros_con_mismo_id.exists():
                # Obtén el último proceso asociado al extranjero si existe
                try:
                    ultimo_proceso = extranjeros_con_mismo_id.latest('fechaRegistro').noproceso_set.latest('consecutivo')
                    nuevo_consecutivo = ultimo_proceso.consecutivo + 1
                except NoProceso.DoesNotExist:
                    nuevo_consecutivo = 1
            else:
                nuevo_consecutivo = 1

            # Crea un registro en la tabla NoProceso
            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = 'Activo',
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=extranjero.deLaEstacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()
           
        instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = get_object_or_404(PuestaDisposicionINM, id=puesta_id)

        context['form'].fields['deLaPuestaIMN'].initial = puesta
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
    
class AgregarBiometricoINM(CreateView):
    model = Biometrico
    form_class = BiometricoFormINM
    template_name = 'puestaINM/createBiometricosINM.html'  # Cambiar a la ruta correcta

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Biometrico Agregado con Éxito.')

        return reverse('listarExtranjeros', args=[extranjero.deLaPuestaIMN.id])
    
    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        initial['Extranjero'] = extranjero
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del extranjero del argumento en la URL
        extranjero_id = self.kwargs.get('extranjero_id')
        # Obtén la instancia del extranjero correspondiente al ID
        context['form'] = BiometricoFormINM()
        context['form1'] = descripcionForms()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM' 
         # Datos iniciales para el segundo formulario (descripcionForms)
        biometrico_initial = {
          'Extranjero': extranjero,
        # Agrega aquí más campos y sus valores iniciales según tu formulario BiometricoFormINM
        }
        context['form'] = BiometricoFormINM(initial=biometrico_initial)
        descripcion_initial = {
            'delExtranjero': extranjero,
        }
        context['form1'] = descripcionForms(initial=descripcion_initial)

        return context
    
    def form_valid(self, form):
    # Lógica de recorte
     image = form.cleaned_data['fotografiaExtranjero']
     img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
     faces = face_cascade.detectMultiScale(img, 1.3, 5)
     region = None  # Definición inicial de la variable "region"

     for (x,y,w,h) in faces:
        margen_vertical_arriba = int(0.4 * h)  # 10% arriba para que el recorte no sea exactamente desde el inicio del cabello
        margen_vertical_abajo = int(0.4 * h)  # 40% hacia abajo para incluir cuello y clavícula
        margen_horizontal = int(0.2 * w)
            
        inicio_x = max(0, x - margen_horizontal)
        inicio_y = max(0, y - margen_vertical_arriba)
        fin_x = min(img.shape[1], x + w + margen_horizontal)
        fin_y = min(img.shape[0], y + h + margen_vertical_abajo)
            
        region = img[inicio_y:fin_y, inicio_x:fin_x]
    
     if region is not None and region.size > 0:
        is_success, im_buf_arr = cv2.imencode(".jpg", region)
        region_bytes = im_buf_arr.tobytes()
        
        # Guarda en el modelo Biometrico
        biometrico = form.save(commit=False)
        biometrico.fotografiaExtranjero.save(f'{image.name}_recortada.jpg', ContentFile(region_bytes), save=True)

        # Calcula el face encoding y guarda en el modelo UserFace1
        image_path = biometrico.fotografiaExtranjero.path
        image_array = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image_array)

        if face_encodings:
            biometrico.face_encoding = face_encodings[0].tolist()
            biometrico.save()
            user_face1 = UserFace1(extranjero=biometrico.Extranjero)
            user_face1.face_encoding = face_encodings[0].tolist()
            user_face1.save()
     else:
        # Muestra un mensaje al usuario
        messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, sube una imagen con un rostro visible.")
        return super().form_invalid(form)
    
    # Procesa el segundo formulario (DescripcionForm)
     descripcion_form = descripcionForms(self.request.POST)
    
     if descripcion_form.is_valid():
        descripcion = descripcion_form.save(commit=False)
        # Asigna cualquier relación necesaria para el segundo formulario aquí
        # Por ejemplo, si necesitas relacionar con el biometrico
        descripcion.biometrico = biometrico  # Asegúrate de ajustar esto según tu modelo real
        descripcion.save()
     else:
        messages.error(self.request, "Error en el segundo formulario. Por favor, verifica los datos.")
        return super().form_invalid(form)

     return super().form_valid(form)

    


class EditarBiometricoINM(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_biometrico',
    }
    model = Biometrico
    form_class = BiometricoFormINM
    template_name = 'puestaINM/editBiometricosINM.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
        return reverse('listarExtranjeros', args=[extranjero.deLaPuestaIMN.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        descripcion_obj, created = descripcion.objects.get_or_create(delExtranjero=extranjero)
        # Pasar el formulario de Descripcion al contexto con la instancia correspondiente
        context['form1'] = descripcionForms(instance=descripcion_obj)

        return context
    def form_valid(self, form):
        # Lógica de recorte
        image = form.cleaned_data['fotografiaExtranjero']
        
        img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        region = None  # Definición inicial de la variable "region"

        for (x,y,w,h) in faces:
            margen_vertical_arriba = int(0.4 * h)  # 10% arriba para que el recorte no sea exactamente desde el inicio del cabello
            margen_vertical_abajo = int(0.4 * h)  # 40% hacia abajo para incluir cuello y clavícula
            margen_horizontal = int(0.2 * w)
                
            inicio_x = max(0, x - margen_horizontal)
            inicio_y = max(0, y - margen_vertical_arriba)
            fin_x = min(img.shape[1], x + w + margen_horizontal)
            fin_y = min(img.shape[0], y + h + margen_vertical_abajo)
                
            region = img[inicio_y:fin_y, inicio_x:fin_x]

        if region is not None and region.size > 0:
            is_success, im_buf_arr = cv2.imencode(".jpg", region)
            region_bytes = im_buf_arr.tobytes()
            
            biometrico = form.save(commit=False)
            biometrico.fotografiaExtranjero.save(f'{image.name}_recortada.jpg', ContentFile(region_bytes), save=False)
            
            # Actualiza el face_encoding del objeto Biometrico
            image_path = biometrico.fotografiaExtranjero.path
            image_array = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image_array)
            
            if face_encodings:
                biometrico.face_encoding = face_encodings[0].tolist()
                biometrico.save()
                
                # Actualiza o crea el objeto UserFace1 correspondiente
                user_face1, created = UserFace1.objects.update_or_create(
                    extranjero=biometrico.Extranjero,
                    defaults={'face_encoding': face_encodings[0].tolist()}
                )
        else:
            messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, sube una imagen con un rostro visible.")
            return super().form_invalid(form)
    

        return super().form_valid(form)
        

class DeleteExtranjeroINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Extranjero
    template_name = 'modal/eliminarExtranjeroINM.html'

    def get_success_url(self):
        puesta_id = self.object.deLaPuestaIMN.id
        messages.success(self.request, 'Extranjero Eliminado con Éxito.')
        return reverse('listarExtranjeros', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context

class acompananteList(ListView):
    model = Extranjero
    template_name = "puestaINM/listAcompananteINM.html" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)

        # Obtener la lista de extranjeros de la misma puesta
        extranjeros_puesta = Extranjero.objects.filter(deLaPuestaIMN_id=puesta_id, estatus ='Activo').exclude(pk=extranjero_principal_id)

        # Filtrar extranjeros no relacionados
        extranjeros_no_relacionados = extranjeros_puesta.exclude(
            Q(acompanantes_delExtranjero__delAcompanante=extranjero_principal) |
            Q(acompanantes_delAcompanante__delExtranjero=extranjero_principal)
        )

        # Filtrar las relaciones donde el extranjero principal es delExtranjero y no está relacionado como delAcompanante
        relaciones_del_extranjero = Acompanante.objects.filter(delExtranjero=extranjero_principal).exclude(delAcompanante=extranjero_principal)
        
        # Filtrar las relaciones donde el extranjero principal es delAcompanante y no está relacionado como delExtranjero
        relaciones_del_acompanante = Acompanante.objects.filter(delAcompanante=extranjero_principal).exclude(delExtranjero=extranjero_principal)

        context['extranjero_principal'] = extranjero_principal
        context['extranjeros_no_relacionados'] = extranjeros_no_relacionados
        context['relaciones_del_extranjero'] = relaciones_del_extranjero
        context['relaciones_del_acompanante'] = relaciones_del_acompanante
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class AgregarAcompananteViewINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_acompanante',
    }
    model = Acompanante
    form_class = AcompananteForm
    template_name = 'modal/acompananteINM.html'

    def get_success_url(self):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        messages.success(self.request, 'Acompañante Agregado con Éxito.')

        return reverse_lazy('listAcompanantesINM', kwargs={'extranjero_id': extranjero_principal.id, 'puesta_id': extranjero_principal.deLaPuestaIMN.id})
    
    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']

        form.instance.delExtranjero_id = extranjero_principal_id
        form.instance.delAcompanante_id = extranjero_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']
        context['extranjero_principal'] = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        context['extranjero'] = get_object_or_404(Extranjero, pk=extranjero_id)
        return context
    
class DeleteAcompananteINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteINM.html'

    def get_success_url(self):
        acompanante = self.object
        extranjero_id = acompanante.delExtranjero.id
        puesta_id = acompanante.delExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Acompañante Eliminado con Éxito.')
        return reverse_lazy('listAcompanantesINM', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context
class DeleteAcompananteINM1(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteINM1.html'

    def get_success_url(self):
        acompanante = self.object
        extranjero_id = acompanante.delAcompanante.id
        puesta_id = acompanante.delAcompanante.deLaPuestaIMN.id
        messages.success(self.request, 'Acompañante Eliminado con Éxito.')
        return reverse_lazy('listAcompanantesINM', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    

class DeleteAcompananteAC(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteAC.html'

    def get_success_url(self):
        acompanante = self.object
        extranjero_id = acompanante.delExtranjero.id
        puesta_id = acompanante.delExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Acompañante Eliminado con Éxito.')
        return reverse_lazy('listAcompanantesAC', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context
class DeleteAcompananteAC1(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteAC1.html'

    def get_success_url(self):
        acompanante = self.object
        extranjero_id = acompanante.delAcompanante.id
        puesta_id = acompanante.delAcompanante.deLaPuestaAC.id
        messages.success(self.request, 'Acompañante Eliminado con Éxito.')
        return reverse_lazy('listAcompanantesAC', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
    
    
class createExtranjeroAcomINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'puestaINM/crearAcompananteINM.html' 
    # success_url = reverse_lazy('homePuestaINM')
    
    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal del contexto
        messages.success(self.request, 'Extranjero Creado con Éxito.')
        return reverse('listAcompanantesINM', args=[extranjero_principal_id, puesta_id])
        
    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass

        return {'deLaPuestaIMN': puesta, 'deLaEstacion':estacion, 'viajaSolo':viaja_solo} 

    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']

        if estacion:
            estacion.capacidad -= 1
            estacion.save()

        nuevo_consecutivo = 1  
        status_default = 'Activo' 
 
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
        except Usuario.DoesNotExist:
            pass
        with transaction.atomic():
            extranjero = form.save(commit=False)
            extranjero.puesta = puesta

            # Guarda el objeto para obtener un ID asignado
            extranjero.save()

            # Asigna el númeroExtranjero basado en el ID del registro
            year_actual = extranjero.fechaRegistro.year  # Obtiene el año actual
            nomenclatura = usuario_data.estancia.identificador  # Tu nomenclatura personalizada
            numero_extranjero = f"{year_actual}/{nomenclatura}/{extranjero.id}"
            extranjero.numeroExtranjero = numero_extranjero

            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"

            # Crea un registro en la tabla NoProceso
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = status_default,
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )
        # Manejo de los archivos
        handle_file('documentoIdentidad')
        return super().form_valid(form) 
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal
        context['extranjero_principal_id'] = extranjero_principal_id  # Pasa el ID al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa

        return context

#------------------------ Fin Puesta por INM-----------------------------

#------------------------  Puesta por AC -----------------------------
class inicioACList(ListView):
    model = PuestaDisposicionAC
    template_name = "puestaAC/homePuestaAC.html" 
    context_object_name = 'puestaAC'
    
    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = PuestaDisposicionAC.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia

        puestas_count = self.get_queryset().count() 
        context['puestas_count'] = puestas_count

        #extranjeros_total = Extranjero.objects.filter(deLaEstacion=user_estacion).count() #OBTENER EL NUMERO TOTAL DE EXTRANJERO POR LA ESTACION 
        extranjeros_total = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion, estatus='Activo').count()
        context['extranjeros_total'] = extranjeros_total
        nacionalidades_count = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion).values('nacionalidad').distinct().count()
        context['nacionalidades_count'] = nacionalidades_count

        hombres_count = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion, genero=0, estatus='Activo').count()
        mujeres_count = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion, genero=1, estatus='Activo').count()
        context['mujeres_count'] = mujeres_count
        context['hombres_count'] = hombres_count
        capacidad_actual = user_estacion.capacidad
        context['capacidad_actual'] = capacidad_actual

        return context
    
class createPuestaAC(HandleFileMixin,CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicionac',
    }
    model = PuestaDisposicionAC               
    form_class = puestaDisposicionACForm      
    template_name = 'puestaAC/createPuestaAC.html'  
    success_url = reverse_lazy('homePuestaAC')

    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        ultimo_registro = PuestaDisposicionAC.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.identificadorProceso.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'{numero_identificador}/{datetime.now().year}/{usuario_id}/{ultimo_numero + 1:04d}'

        initial['identificadorProceso'] = nuevo_numero
        initial['entidadFederativa'] = estado
        initial['dependencia'] = estacionM
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context
    
    def form_valid(self, form):
        instance = form.save() 
        self.handle_file(instance,'oficioPuesta')
        self.handle_file(instance,'oficioComision')
        self.handle_file(instance,'certificadoMedico')
        return super(createPuestaAC, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'La puesta por autoridad competente se ha creado con éxito.')
        return super().get_success_url()
    
class createExtranjeroAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'puestaAC/createExtranjeroAC.html' 

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        if self.object.viajaSolo:
            messages.success(self.request, 'Extranjero creado con éxito.')
            return reverse('agregar_biometricoAC', args=[extranjero_id])
        else:
            messages.success(self.request, 'Extranjero creado con éxito.')
            return reverse('listAcompanantesAC', args=[extranjero_id, puesta_id])

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
       
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id= usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador_puesta = puesta.identificadorProceso
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        viaja_solo = True
        initial['viajaSolo'] = viaja_solo
        return {'deLaPuestaAC': puesta, 'deLaEstacion':estacion, 'viajaSolo': viaja_solo } 
     
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        
        if estacion:
            estacion.capacidad -= 1
            estacion.save()     
        nuevo_consecutivo = 1   
        status_proceso = 'Activo'
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
        except Usuario.DoesNotExist:
            pass
        with transaction.atomic():
            extranjero = form.save(commit=False)
            extranjero.puesta = puesta

            # Guarda el objeto para obtener un ID asignado
            extranjero.save()

            # Asigna el númeroExtranjero basado en el ID del registro
            year_actual = extranjero.fechaRegistro.year  # Obtiene el año actual
            nomenclatura = usuario_data.estancia.identificador  # Tu nomenclatura personalizada
            numero_extranjero = f"{year_actual}/{nomenclatura}/{extranjero.id}"
            extranjero.numeroExtranjero = numero_extranjero
            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"

            # Crea un registro en la tabla NoProceso
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = status_proceso,
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class listarExtranjerosAC(ListView):
    model = Extranjero
    template_name = 'puestaAC/listExtranjerosAC.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        estado = self.request.GET.get('estado_filtrado', 'activo') 
        queryset = Extranjero.objects.filter(deLaPuestaAC_id=puesta_id)

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)  # Asegúrate de reemplazar 'Puesta' con el nombre correcto de tu modelo
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
            tiene_enseres = False
            if ultimo_nup:
                notificacion = NotificacionDerechos.objects.filter(no_proceso_id=ultimo_nup).first()
                if notificacion:
                    extranjero.tiene_notificacion_derechos = True
                    extranjero.fecha_aceptacion = notificacion.fechaAceptacion
                    extranjero.estacion_notificacion = notificacion.estacion
                else:
                    extranjero.tiene_notificacion_derechos = False
                    extranjero.fecha_aceptacion = None
                    extranjero.hora_aceptacion = None
                    extranjero.estacion_notificacion = None
            if ultimo_nup:
                enseres = EnseresBasicos.objects.filter(nup=ultimo_nup).first()
                if enseres:
                    tiene_enseres = True

            extranjero.tiene_enseres = tiene_enseres
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_inventario = False

            if ultimo_nup:
                inventario = Inventario.objects.filter(nup=ultimo_nup).first()
                if inventario:
                    tiene_inventario = True

            extranjero.tiene_inventario = tiene_inventario
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class EditarExtranjeroAC(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroACForms
    template_name = 'puestaAC/editarExtranjeroAC.html'
    def form_valid(self, form):
        # Guarda el formulario, pero no comitea a la base de datos aún
        instance = form.save(commit=False)

        # Manejo de archivos
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')

        # Lógica relacionada con el cambio de estatus
        old_extranjero = Extranjero.objects.get(pk=instance.pk)  # Obtén el extranjero original antes de modificar

        if old_extranjero.estatus == 'Activo' and instance.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = instance.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and instance.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = instance.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        # Finalmente, guarda la instancia
        instance.save()

        return super().form_valid(form)

        

    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
        return reverse('listarExtranjeroAC', args=[self.object.deLaPuestaAC.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
        extranjero = Extranjero.objects.get(id=extranjero_id)
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['puesta'] = self.object.deLaPuestaAC
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context    
    def dispatch(self, request, *args, **kwargs):
        # Obtén el registro que se va a editar
        registro = self.get_object()

        # Calcula la diferencia de tiempo
        diferencia = timezone.now() - registro.horaRegistro

        # Define el límite de tiempo permitido para la edición (dos días en este caso)
        limite_de_tiempo = timedelta(days=1)

        if diferencia > limite_de_tiempo:
            # Si han pasado más de tres minutos, muestra un mensaje de error y redirige
            messages.error(request, "No puedes editar este registro después de 1 dia.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la URL actual o a la página de inicio si no se puede determinar la URL actual

        return super().dispatch(request, *args, **kwargs)
    
class EditarExtranjeroACProceso(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroACForms
    template_name = 'puestaAC/editarExtranjeroAC.html'
    def get_initial(self):
        initial = super().get_initial()
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        initial['deLaPuestaAC']=puesta
        initial['deLaPuestaIMN']=None
        initial['deLaPuestaVP']=None
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        return initial
    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
        return reverse('listarExtranjeroAC', args=[self.object.deLaPuestaAC.id])
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)  # Obtén el extranjero original antes de modificar
         # Obtén el ID de la nueva puesta de la URL
        puesta_id = self.request.GET.get('puesta_id', None)

        # Asigna el ID de la nueva puesta al campo deLaPuestaIMN
        if puesta_id:
            extranjero.deLaPuestaAC_id = puesta_id

        with transaction.atomic():
            # Cálculo del nuevo consecutivo
            extranjeros_con_mismo_id = Extranjero.objects.filter(id=extranjero.id)
            if extranjeros_con_mismo_id.exists():
                # Obtén el último proceso asociado al extranjero si existe
                try:
                    ultimo_proceso = extranjeros_con_mismo_id.latest('fechaRegistro').noproceso_set.latest('consecutivo')
                    nuevo_consecutivo = ultimo_proceso.consecutivo + 1
                except NoProceso.DoesNotExist:
                    nuevo_consecutivo = 1
            else:
                nuevo_consecutivo = 1

            # Crea un registro en la tabla NoProceso
            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status='Activado',
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=extranjero.deLaEstacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()
           
        instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = get_object_or_404(PuestaDisposicionAC, id=puesta_id)

        context['form'].fields['deLaPuestaAC'].initial = puesta
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    

class AgregarBiometricoAC(CreateView):
    model = Biometrico
    form_class = BiometricoFormAC
    template_name = 'puestaAC/createBiometricosAC.html'  # Cambiar a la ruta correcta

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Biometricos creados con éxito.')
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    
    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        initial['Extranjero'] = extranjero
        return initial
    
    def form_valid(self, form):
        # Lógica de recorte
        image = form.cleaned_data['fotografiaExtranjero']
        
        img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        region = None  # Definición inicial de la variable "region"

        for (x,y,w,h) in faces:
            margen_vertical_arriba = int(0.4 * h)  # 10% arriba para que el recorte no sea exactamente desde el inicio del cabello
            margen_vertical_abajo = int(0.4 * h)  # 40% hacia abajo para incluir cuello y clavícula
            margen_horizontal = int(0.2 * w)
                
            inicio_x = max(0, x - margen_horizontal)
            inicio_y = max(0, y - margen_vertical_arriba)
            fin_x = min(img.shape[1], x + w + margen_horizontal)
            fin_y = min(img.shape[0], y + h + margen_vertical_abajo)
                
            region = img[inicio_y:fin_y, inicio_x:fin_x]

        if region is not None and region.size > 0:
         is_success, im_buf_arr = cv2.imencode(".jpg", region)
         region_bytes = im_buf_arr.tobytes()
        
        # Guarda en el modelo Biometrico
         biometrico = form.save(commit=False)
         biometrico.fotografiaExtranjero.save(f'{image.name}_recortada.jpg', ContentFile(region_bytes), save=True)

        # Calcula el face encoding y guarda en el modelo UserFace1
         image_path = biometrico.fotografiaExtranjero.path
         image_array = face_recognition.load_image_file(image_path)
         face_encodings = face_recognition.face_encodings(image_array)

         if face_encodings:
            biometrico.face_encoding = face_encodings[0].tolist()
            biometrico.save()
            user_face1 = UserFace1(extranjero=biometrico.Extranjero)
            user_face1.face_encoding = face_encodings[0].tolist()
            user_face1.save()
        else:
        # Muestra un mensaje al usuario
         messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, sube una imagen con un rostro visible.")
         return super().form_invalid(form)

        # Procesar el segundo formulario (descripcionForms)
        descripcion_form = descripcionForms(self.request.POST)
        if descripcion_form.is_valid():
            descripcion = descripcion_form.save(commit=False)
            # Asigna cualquier relación necesaria para el segundo formulario aquí
            descripcion.save()
        else:
        # Muestra un mensaje al usuario
          messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, toma una imagen con un rostro visible.")
          return super().form_invalid(form)

        return super().form_valid(form)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del extranjero del argumento en la URL
        extranjero_id = self.kwargs.get('extranjero_id')
        # Obtén la instancia del extranjero correspondiente al ID
        context['form'] = BiometricoFormAC()
        context['form1'] = descripcionForms()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaAC
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        biometrico_initial = {
          'Extranjero': extranjero,
        # Agrega aquí más campos y sus valores iniciales según tu formulario BiometricoFormINM
        }
        context['form'] = BiometricoFormAC(initial=biometrico_initial)
        descripcion_initial = {
            'delExtranjero': extranjero,
        }
        context['form1'] = descripcionForms(initial=descripcion_initial)

        return context

class EditarBiometricoAC(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_biometrico',
    }
    model = Biometrico
    form_class = BiometricoFormAC
    template_name = 'puestaAC/editBiometricosAC.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Biometricos editados con éxito.')
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaAC
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        descripcion_obj, created = descripcion.objects.get_or_create(delExtranjero=extranjero)
        # Pasar el formulario de Descripcion al contexto con la instancia correspondiente
        context['form1'] = descripcionForms(instance=descripcion_obj)
        return context
    
    def form_valid(self, form):
            # Lógica de recorte
            image = form.cleaned_data['fotografiaExtranjero']
            
            img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            region = None  # Definición inicial de la variable "region"

            for (x,y,w,h) in faces:
                margen_vertical_arriba = int(0.4 * h)  # 10% arriba para que el recorte no sea exactamente desde el inicio del cabello
                margen_vertical_abajo = int(0.4 * h)  # 40% hacia abajo para incluir cuello y clavícula
                margen_horizontal = int(0.2 * w)
                    
                inicio_x = max(0, x - margen_horizontal)
                inicio_y = max(0, y - margen_vertical_arriba)
                fin_x = min(img.shape[1], x + w + margen_horizontal)
                fin_y = min(img.shape[0], y + h + margen_vertical_abajo)
                    
                region = img[inicio_y:fin_y, inicio_x:fin_x]

            if region is not None and region.size > 0:
                is_success, im_buf_arr = cv2.imencode(".jpg", region)
                region_bytes = im_buf_arr.tobytes()
                
                biometrico = form.save(commit=False)
                biometrico.fotografiaExtranjero.save(f'{image.name}_recortada.jpg', ContentFile(region_bytes), save=False)
                
                # Actualiza el face_encoding del objeto Biometrico
                image_path = biometrico.fotografiaExtranjero.path
                image_array = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image_array)
                
                if face_encodings:
                    biometrico.face_encoding = face_encodings[0].tolist()
                    biometrico.save()
                    
                    # Actualiza o crea el objeto UserFace1 correspondiente
                    user_face1, created = UserFace1.objects.update_or_create(
                        extranjero=biometrico.Extranjero,
                        defaults={'face_encoding': face_encodings[0].tolist()}
                    )
            else:
                messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, sube una imagen con un rostro visible.")
                return super().form_invalid(form)
        

            return super().form_valid(form)
        
        

class DeleteExtranjeroAC(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Extranjero
    template_name = 'modal/eliminarExtranjeroAC.html'
    
    def get_success_url(self):
        puesta_id = self.object.deLaPuestaAC.id
        messages.success(self.request, 'Extranjero eliminado con éxito.')
        return reverse('listarExtranjeroAC', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaAC.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class createAcompananteAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'puestaAC/createAcompananteAC.html' 

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal del contexto
        messages.success(self.request, 'Extranjero creado con éxito.')
        return reverse('listAcompanantesAC', args=[extranjero_principal_id, puesta_id])
    

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
       
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id= usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        viaja_solo = True
        initial['viajaSolo'] = viaja_solo
        return {'deLaPuestaAC': puesta, 'deLaEstacion':estacion,'viajaSolo': viaja_solo } 
     
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        
        if estacion:
            estacion.capacidad -= 1
            estacion.save()
        nuevo_consecutivo = 1   
        status_proceso ='Activo'
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
        except Usuario.DoesNotExist:
            pass
        with transaction.atomic():
            extranjero = form.save(commit=False)
            extranjero.puesta = puesta

            # Guarda el objeto para obtener un ID asignado
            extranjero.save()

            # Asigna el númeroExtranjero basado en el ID del registro
            year_actual = extranjero.fechaRegistro.year  # Obtiene el año actual
            nomenclatura = usuario_data.estancia.identificador  # Tu nomenclatura personalizada
            numero_extranjero = f"{year_actual}/{nomenclatura}/{extranjero.id}"
            extranjero.numeroExtranjero = numero_extranjero

            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"

            # Crea un registro en la tabla NoProceso
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = status_proceso,
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            instance = form.save(commit=False)

        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )
        # Manejo de los archivos
        handle_file('documentoIdentidad')
        return super().form_valid(form)  # Cambié "createPuestaAC" por "super()"
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal
        context['extranjero_principal_id'] = extranjero_principal_id  # Pasa el ID al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
    
class ListAcompanantesAC(ListView):
    model = Extranjero
    template_name = 'puestaAC/listAcompanantesAC.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)

        # Obtener la lista de extranjeros de la misma puesta
        extranjeros_puesta = Extranjero.objects.filter(deLaPuestaAC_id=puesta_id, estatus='Activo').exclude(pk=extranjero_principal_id)
        
        # Filtrar extranjeros no relacionados
        extranjeros_no_relacionados = extranjeros_puesta.exclude(
            Q(acompanantes_delExtranjero__delAcompanante=extranjero_principal) |
            Q(acompanantes_delAcompanante__delExtranjero=extranjero_principal)
        )

        # Filtrar las relaciones donde el extranjero principal es delExtranjero y no está relacionado como delAcompanante
        relaciones_del_extranjero = Acompanante.objects.filter(delExtranjero=extranjero_principal).exclude(delAcompanante=extranjero_principal)
        
        # Filtrar las relaciones donde el extranjero principal es delAcompanante y no está relacionado como delExtranjero
        relaciones_del_acompanante = Acompanante.objects.filter(delAcompanante=extranjero_principal).exclude(delExtranjero=extranjero_principal)

        context['extranjero_principal'] = extranjero_principal
        context['extranjeros_no_relacionados'] = extranjeros_no_relacionados
        context['relaciones_del_extranjero'] = relaciones_del_extranjero
        context['relaciones_del_acompanante'] = relaciones_del_acompanante
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context


class AgregarAcompananteViewAC(CreateView):
    model = Acompanante
    form_class = AcompananteForm
    # template_name = 'puestaAC/agregar_acompananteAC.html'
    template_name = 'modal/acompananteAC.html'

    def get_success_url(self):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        messages.success(self.request, 'Acompañante agregado con éxito.')

        return reverse_lazy('listAcompanantesAC', kwargs={'extranjero_id': extranjero_principal.id, 'puesta_id': extranjero_principal.deLaPuestaAC.id})
    
    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']

        form.instance.delExtranjero_id = extranjero_principal_id
        form.instance.delAcompanante_id = extranjero_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']
        context['extranjero_principal'] = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        context['extranjero'] = get_object_or_404(Extranjero, pk=extranjero_id)
        return context
    



class CrearRelacionAcompananteAC(CreateView):
    model = Acompanante
    form_class = AcompananteForm
    template_name= 'puestaAC/listAcompanantesAC.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        kwargs['extranjero_principal_id'] = extranjero_principal_id
        return kwargs

    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = Extranjero.objects.get(pk=extranjero_principal_id)

        self.object = form.save(commit=False)
        self.object.delExtranjero = extranjero_principal
        self.object.save()

        puesta_id = extranjero_principal.deLaPuestaAC_id
        return redirect('listAcompanantesAC', extranjero_principal.id, puesta_id)
    
class CrearRelacionView(View):
    def post(self, request, extranjero_id, relacion_id):
        extranjero_principal = Extranjero.objects.get(pk=extranjero_id)
        relacion = Relacion.objects.get(pk=relacion_id)

        # Crea la relación
        nueva_relacion = Acompanante(delExtranjero=extranjero_principal, relacion=relacion)
        nueva_relacion.save()

        return JsonResponse({'success': True})
    

class CalcularTamanoDiscoView(DetailView):
    model = Extranjero
    template_name = 'tester/calcular_tamano_disco.html'
    context_object_name = 'extranjero'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero = self.get_object()
        size_on_disk = sys.getsizeof(pickle.dumps(extranjero))
        context['size_on_disk'] = size_on_disk        
        puesta_imn = extranjero.deLaPuestaIMN
        size_on_disk_puesta_imn2 = sys.getsizeof(pickle.dumps(puesta_imn))
        context['size_on_disk_puesta_imn2'] = size_on_disk_puesta_imn2


        try:
            biometrico = extranjero.biometrico
            size_on_disk_biometrico_relation = sys.getsizeof(pickle.dumps(biometrico))
        except Biometrico.DoesNotExist:
            size_on_disk_biometrico_relation = 0
        context['size_on_disk_biometrico_relation'] = size_on_disk_biometrico_relation

        acompanantes = Acompanante.objects.filter(Q(delExtranjero=extranjero) | Q(delAcompanante=extranjero))
        size_on_disk_acompanantes = sum(sys.getsizeof(pickle.dumps(acompanante)) for acompanante in acompanantes)
        context['size_on_disk_acompanantes'] = size_on_disk_acompanantes

        


        return context

from .models import PuestaDisposicionVP
from .forms import puestaVPForm, extranjeroFormsVP, editExtranjeroVPForm
#------------------------ Puesta por VP-----------------------------
class inicioVPList(ListView):
    model = PuestaDisposicionVP       
    template_name = "puestaVP/homePuestaVP.html" 
    context_object_name = 'puestasvp'

    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = PuestaDisposicionVP.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa

        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia

        puestas_count = self.get_queryset().count() 
        context['puestas_count'] = puestas_count

        #extranjeros_total = Extranjero.objects.filter(deLaEstacion=user_estacion).count() #OBTENER EL NUMERO TOTAL DE EXTRANJERO POR LA ESTACION 
        extranjeros_total = Extranjero.objects.filter(deLaPuestaVP__deLaEstacion=user_estacion, estatus='Activo').count()
        context['extranjeros_total'] = extranjeros_total
        nacionalidades_count = Extranjero.objects.filter(deLaPuestaVP__deLaEstacion=user_estacion).values('nacionalidad').distinct().count()
        context['nacionalidades_count'] = nacionalidades_count

        hombres_count = Extranjero.objects.filter(deLaPuestaVP__deLaEstacion=user_estacion, genero=0, estatus='Activo').count()
        mujeres_count = Extranjero.objects.filter(deLaPuestaVP__deLaEstacion=user_estacion, genero=1, estatus='Activo').count()
        context['mujeres_count'] = mujeres_count
        context['hombres_count'] = hombres_count
        capacidad_actual = user_estacion.capacidad
        context['capacidad_actual'] = capacidad_actual

        return context
    
class createPuestaVP(CreateView):
    model = PuestaDisposicionVP             
    form_class = puestaVPForm     
    template_name = 'puestaVP/createPuestaVP.html'  
    success_url = reverse_lazy('homePuestasVP')

    def get_initial(self):
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            UsuarioId = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identifica = estacion.identificador
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        # Generar el número con formato automáticamente
        ultimo_registro = PuestaDisposicionVP.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroOficio.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'{numero_identifica}/{datetime.now().year}/{UsuarioId}/{ultimo_numero + 1:04d}'

        initial['numeroOficio'] = nuevo_numero
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        return context
    def get_success_url(self):
        messages.success(self.request, 'La puesta de voluntad se ha creado con éxito.')
        return super().get_success_url()

class listarExtranjerosVP(ListView):
    model = Extranjero
    template_name = 'puestaVP/listExtranjeroVP.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        estado = self.request.GET.get('estado_filtrado', 'activo') 
        queryset = Extranjero.objects.filter(deLaPuestaVP_id=puesta_id)

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionVP.objects.get(id=puesta_id)  # Asegúrate de reemplazar 'Puesta' con el nombre correcto de tu modelo
        for extranjero in context['extranjeros']:
         ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
         tiene_notificacion = False
         if ultimo_nup:
                notificacion = NotificacionDerechos.objects.filter(no_proceso_id=ultimo_nup).first()
                if notificacion:
                    extranjero.tiene_notificacion_derechos = True
                    extranjero.fecha_aceptacion = notificacion.fechaAceptacion
                    extranjero.estacion_notificacion = notificacion.estacion
                else:
                    extranjero.tiene_notificacion_derechos = False
                    extranjero.fecha_aceptacion = None
                    extranjero.hora_aceptacion = None
                    extranjero.estacion_notificacion = None
         if ultimo_nup:
            notificacion = Notificacion.objects.filter(nup=ultimo_nup).first()
            if notificacion:
                tiene_notificacion = True

         extranjero.tiene_notificacion = tiene_notificacion
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_enseres = False

            if ultimo_nup:
                enseres = EnseresBasicos.objects.filter(nup=ultimo_nup).first()
                if enseres:
                    tiene_enseres = True

            extranjero.tiene_enseres = tiene_enseres
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_inventario = False

            if ultimo_nup:
                inventario = Inventario.objects.filter(nup=ultimo_nup).first()
                if inventario:
                    tiene_inventario = True

            extranjero.tiene_inventario = tiene_inventario
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class createExtranjeroVP(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsVP  
    template_name = 'puestaVP/createExtranjeroVP.html' 
    
    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        if self.object.viajaSolo:
            messages.success(self.request, 'Extranjero creado con éxito.')
            return reverse('agregar_biometricoVP', args=[extranjero_id])
        else:
            messages.success(self.request, 'Extranjero creado con éxito.')
            return reverse('list-acompanantes-vp', args=[extranjero_id, puesta_id])
                
    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionVP.objects.get(id=puesta_id)
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador_puesta = puesta.numeroOficio
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass
        return {'deLaPuestaVP': puesta, 'deLaEstacion':estacion, 'viajaSolo':viaja_solo} 

    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionVP.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        if estacion:
            estacion.capacidad -= 1
            estacion.save()     
        nuevo_consecutivo = 1   
        status_proceso = 'Activo'
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
        except Usuario.DoesNotExist:
            pass
        with transaction.atomic():
            extranjero = form.save(commit=False)
            extranjero.puesta = puesta

            # Guarda el objeto para obtener un ID asignado
            extranjero.save()

            # Asigna el númeroExtranjero basado en el ID del registro
            year_actual = extranjero.fechaRegistro.year  # Obtiene el año actual
            nomenclatura = usuario_data.estancia.identificador  # Tu nomenclatura personalizada
            numero_extranjero = f"{year_actual}/{nomenclatura}/{extranjero.id}"
            extranjero.numeroExtranjero = numero_extranjero
            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"

            # Crea un registro en la tabla NoProceso
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = status_proceso,
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

        instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        
        return super().form_valid(form)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionVP.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa

        return context
    


class listarAcompanantesVP(ListView):
    model = Extranjero
    template_name = "puestaVP/listAcompananteVP.html" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)

        # Obtener la lista de extranjeros de la misma puesta
        extranjeros_puesta = Extranjero.objects.filter(deLaPuestaVP_id=puesta_id, estatus ='Activo').exclude(pk=extranjero_principal_id)

        # Filtrar extranjeros no relacionados
        extranjeros_no_relacionados = extranjeros_puesta.exclude(
            Q(acompanantes_delExtranjero__delAcompanante=extranjero_principal) |
            Q(acompanantes_delAcompanante__delExtranjero=extranjero_principal)
        )

        # Filtrar las relaciones donde el extranjero principal es delExtranjero y no está relacionado como delAcompanante
        relaciones_del_extranjero = Acompanante.objects.filter(delExtranjero=extranjero_principal).exclude(delAcompanante=extranjero_principal)
        
        # Filtrar las relaciones donde el extranjero principal es delAcompanante y no está relacionado como delExtranjero
        relaciones_del_acompanante = Acompanante.objects.filter(delAcompanante=extranjero_principal).exclude(delExtranjero=extranjero_principal)

        context['extranjero_principal'] = extranjero_principal
        context['extranjeros_no_relacionados'] = extranjeros_no_relacionados
        context['relaciones_del_extranjero'] = relaciones_del_extranjero
        context['relaciones_del_acompanante'] = relaciones_del_acompanante
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class EditarExtranjeroVP(UpdateView):
    model = Extranjero
    form_class = editExtranjeroVPForm
    template_name = 'puestaVP/editExtranjeroVP.html'

    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')

        return reverse('listarExtranjerosVP', args=[self.object.deLaPuestaVP.id])
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)
          # Obtén el extranjero original antes de modificar
        instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')

        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta'] = self.object.deLaPuestaVP
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
    def dispatch(self, request, *args, **kwargs):
        # Obtén el registro que se va a editar
        registro = self.get_object()

        # Calcula la diferencia de tiempo
        diferencia = timezone.now() - registro.horaRegistro

        # Define el límite de tiempo permitido para la edición (dos días en este caso)
        limite_de_tiempo = timedelta(days=1)

        if diferencia > limite_de_tiempo:
            # Si han pasado más de tres minutos, muestra un mensaje de error y redirige
            messages.error(request, "No puedes editar este registro después de 1 dia.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirige a la URL actual o a la página de inicio si no se puede determinar la URL actual

        return super().dispatch(request, *args, **kwargs)

class EditarExtranjeroVPProceso(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroVPForm
    template_name = 'puestaVP/editExtranjeroVP.html'
    def get_initial(self):
        initial = super().get_initial()
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionVP.objects.get(id=puesta_id)
        initial['deLaPuestaVP']=puesta
        initial['deLaPuestaAC'] =None
        initial['deLaPuestaIMN'] =None
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        return initial
    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
        return reverse('listarExtranjerosVP', args=[self.object.deLaPuestaVP.id])
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)  # Obtén el extranjero original antes de modificar
         # Obtén el ID de la nueva puesta de la URL
        puesta_id = self.request.GET.get('puesta_id', None)

        # Asigna el ID de la nueva puesta al campo deLaPuestaIMN
        if puesta_id:
            extranjero.deLaPuestaVP_id = puesta_id

        with transaction.atomic():
            # Cálculo del nuevo consecutivo
            extranjeros_con_mismo_id = Extranjero.objects.filter(id=extranjero.id)
            if extranjeros_con_mismo_id.exists():
                # Obtén el último proceso asociado al extranjero si existe
                try:
                    ultimo_proceso = extranjeros_con_mismo_id.latest('fechaRegistro').noproceso_set.latest('consecutivo')
                    nuevo_consecutivo = ultimo_proceso.consecutivo + 1
                except NoProceso.DoesNotExist:
                    nuevo_consecutivo = 1
            else:
                nuevo_consecutivo = 1

            # Crea un registro en la tabla NoProceso
            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status='Activado',
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=extranjero.deLaEstacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()
           
        instance = form.save(commit=False)
        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = get_object_or_404(PuestaDisposicionVP, id=puesta_id)

        context['form'].fields['deLaPuestaVP'].initial = puesta
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class DeleteExtranjeroVP(DeleteView):
    model = Extranjero
    template_name = 'modal/eliminarExtranjeroVP.html'

    def get_success_url(self):
        puesta_id = self.object.deLaPuestaVP.id
        messages.success(self.request, 'Extranjero eliminado con éxito.')
        return reverse('listarExtranjerosVP', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaVP.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
   

#-----------------------Agregar Biometricos-------------
class AgregarBiometricoVP(CreateView):
    model = Biometrico
    form_class = BiometricoFormVP
    template_name = 'puestaVP/createBiometricosVP.html'  # Cambiar a la ruta correcta

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Biometrico agregado con éxito.')

        return reverse('listarExtranjerosVP', args=[extranjero.deLaPuestaVP.id])
    
    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        initial['Extranjero'] = extranjero
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del extranjero del argumento en la URL
        extranjero_id = self.kwargs.get('extranjero_id')
        # Obtén la instancia del extranjero correspondiente al ID
        context['form'] = BiometricoFormVP()
        context['form1'] = descripcionForms()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaVP
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        biometrico_initial = {
          'Extranjero': extranjero,
        # Agrega aquí más campos y sus valores iniciales según tu formulario BiometricoFormINM
        }
        context['form'] = BiometricoFormVP(initial=biometrico_initial)
        descripcion_initial = {
            'delExtranjero': extranjero,
        }
        context['form1'] = descripcionForms(initial=descripcion_initial)

        return context
    
    def form_valid(self, form):
    # Lógica de recorte
     image = form.cleaned_data['fotografiaExtranjero']
     img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
     img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
     faces = face_cascade.detectMultiScale(img, 1.3, 5)
     region = None  # Definición inicial de la variable "region"

     for (x,y,w,h) in faces:
        margen_vertical_arriba = int(0.4 * h)  # 10% arriba para que el recorte no sea exactamente desde el inicio del cabello
        margen_vertical_abajo = int(0.4 * h)  # 40% hacia abajo para incluir cuello y clavícula
        margen_horizontal = int(0.2 * w)
            
        inicio_x = max(0, x - margen_horizontal)
        inicio_y = max(0, y - margen_vertical_arriba)
        fin_x = min(img.shape[1], x + w + margen_horizontal)
        fin_y = min(img.shape[0], y + h + margen_vertical_abajo)
            
        region = img[inicio_y:fin_y, inicio_x:fin_x]
    
     if region is not None and region.size > 0:
        is_success, im_buf_arr = cv2.imencode(".jpg", region)
        region_bytes = im_buf_arr.tobytes()
        
        # Guarda en el modelo Biometrico
        biometrico = form.save(commit=False)
        biometrico.fotografiaExtranjero.save(f'{image.name}_recortada.jpg', ContentFile(region_bytes), save=True)

        # Calcula el face encoding y guarda en el modelo UserFace1
        image_path = biometrico.fotografiaExtranjero.path
        image_array = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image_array)

        if face_encodings:
            biometrico.face_encoding = face_encodings[0].tolist()
            biometrico.save()
            user_face1 = UserFace1(extranjero=biometrico.Extranjero)
            user_face1.face_encoding = face_encodings[0].tolist()
            user_face1.save()
     else:
        # Muestra un mensaje al usuario
        messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, sube una imagen con un rostro visible.")
        return super().form_invalid(form)
    
    # Procesa el segundo formulario (DescripcionForm)
     descripcion_form = descripcionForms(self.request.POST)
    
     if descripcion_form.is_valid():
        descripcion = descripcion_form.save(commit=False)
        # Asigna cualquier relación necesaria para el segundo formulario aquí
        # Por ejemplo, si necesitas relacionar con el biometrico
        descripcion.biometrico = biometrico  # Asegúrate de ajustar esto según tu modelo real
        descripcion.save()
     else:
        messages.error(self.request, "Error en el segundo formulario. Por favor, verifica los datos.")
        return super().form_invalid(form)

     return super().form_valid(form)
    
class EditarBiometricoVP(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_biometrico',
    }
    model = Biometrico
    form_class = BiometricoFormVP
    template_name = 'puestaVP/editBiometricosVP.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Biometrico editado creado con éxito.')

        return reverse('listarExtranjerosVP', args=[extranjero.deLaPuestaVP.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaVP
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        descripcion_obj, created = descripcion.objects.get_or_create(delExtranjero=extranjero)
        # Pasar el formulario de Descripcion al contexto con la instancia correspondiente
        context['form1'] = descripcionForms(instance=descripcion_obj)
        return context
    
    def form_valid(self, form):
            # Lógica de recorte
            image = form.cleaned_data['fotografiaExtranjero']
            
            img_array = np.asarray(bytearray(image.read()), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(img, 1.3, 5)
            region = None  # Definición inicial de la variable "region"

            for (x,y,w,h) in faces:
                margen_vertical_arriba = int(0.4 * h)  # 10% arriba para que el recorte no sea exactamente desde el inicio del cabello
                margen_vertical_abajo = int(0.4 * h)  # 40% hacia abajo para incluir cuello y clavícula
                margen_horizontal = int(0.2 * w)
                    
                inicio_x = max(0, x - margen_horizontal)
                inicio_y = max(0, y - margen_vertical_arriba)
                fin_x = min(img.shape[1], x + w + margen_horizontal)
                fin_y = min(img.shape[0], y + h + margen_vertical_abajo)
                    
                region = img[inicio_y:fin_y, inicio_x:fin_x]

            if region is not None and region.size > 0:
                is_success, im_buf_arr = cv2.imencode(".jpg", region)
                region_bytes = im_buf_arr.tobytes()
                
                biometrico = form.save(commit=False)
                biometrico.fotografiaExtranjero.save(f'{image.name}_recortada.jpg', ContentFile(region_bytes), save=False)
                
                # Actualiza el face_encoding del objeto Biometrico
                image_path = biometrico.fotografiaExtranjero.path
                image_array = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image_array)
                
                if face_encodings:
                    biometrico.face_encoding = face_encodings[0].tolist()
                    biometrico.save()
                    
                    # Actualiza o crea el objeto UserFace1 correspondiente
                    user_face1, created = UserFace1.objects.update_or_create(
                        extranjero=biometrico.Extranjero,
                        defaults={'face_encoding': face_encodings[0].tolist()}
                    )
            else:
                messages.error(self.request, "No se detectó un rostro en la imagen. Por favor, sube una imagen con un rostro visible.")
                return super().form_invalid(form)
        

            return super().form_valid(form)
        
    
class createAcompananteVP(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsVP    
    template_name = 'puestaVP/createAcompananteVP.html' 

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal del contexto
        messages.success(self.request, 'Extranjero creado con éxito.')

        return reverse('listAcompanantesVP', args=[extranjero_principal_id, puesta_id])
    

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionVP.objects.get(id=puesta_id)
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass

        return {'deLaPuestaVP': puesta, 'deLaEstacion':estacion, 'viajaSolo':viaja_solo} 

    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionVP.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        if estacion:
            estacion.capacidad -= 1
            estacion.save()     
        nuevo_consecutivo = 1   
        status_proceso = 'Activo'
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            numero_identificador = estacion.identificador
        except Usuario.DoesNotExist:
            pass
        with transaction.atomic():
            extranjero = form.save(commit=False)
            extranjero.puesta = puesta

            # Guarda el objeto para obtener un ID asignado
            extranjero.save()

            # Asigna el númeroExtranjero basado en el ID del registro
            year_actual = extranjero.fechaRegistro.year  # Obtiene el año actual
            nomenclatura = usuario_data.estancia.identificador  # Tu nomenclatura personalizada
            numero_extranjero = f"{year_actual}/{nomenclatura}/{extranjero.id}"
            extranjero.numeroExtranjero = numero_extranjero

            nup = f"{extranjero.fechaRegistro.year}-{extranjero.id}-{nuevo_consecutivo}"

            # Crea un registro en la tabla NoProceso
            no_proceso = NoProceso(
                agno=extranjero.fechaRegistro,
                extranjero=extranjero,
                consecutivo=nuevo_consecutivo,
                status = status_proceso,
                comparecencia = False,
                nup=nup
            )
            no_proceso.save()

            # Crea un registro en la tabla Proceso
            proceso = Proceso(
                estacionInicio=estacion,
                fechaInicio=extranjero.fechaRegistro,
                nup=no_proceso  # Establece la relación con el registro de NoProceso recién creado
            )
            proceso.save()

            instance = form.save(commit=False)

        def handle_file(file_field_name):
            file = self.request.FILES.get(file_field_name)
            if file:
                # Se separa el nombre del archivo y la extensión
                name, ext = os.path.splitext(file.name)
                
                # Verifica si el archivo es un PDF
                if ext.lower() == '.pdf':
                    # Si es un PDF, simplemente lo guarda sin convertir
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        file
                    )
                else:
                    # Si no es un PDF, lo convierte a PDF antes de guardar
                    getattr(instance, file_field_name).save(
                        f"{file_field_name}_{instance.id}.pdf",
                        image_to_pdf(file)
                    )

        # Manejo de los archivos
        handle_file('documentoIdentidad')
        
        return super().form_valid(form)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionVP.objects.get(id=puesta_id)
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal
        context['extranjero_principal_id'] = extranjero_principal_id  # Pasa el ID al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa

        return context
    

class AgregarAcompananteViewVP(CreateView):
    model = Acompanante
    form_class = AcompananteForm
    template_name = 'modal/acompananteVP.html'

    def get_success_url(self):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        messages.success(self.request, 'Acompañante creado con éxito.')
        return reverse_lazy('listAcompanantesVP', kwargs={'extranjero_id': extranjero_principal.id, 'puesta_id': extranjero_principal.deLaPuestaVP.id})
    
    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']
        form.instance.delExtranjero_id = extranjero_principal_id
        form.instance.delAcompanante_id = extranjero_id
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']
        context['extranjero_principal'] = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        context['extranjero'] = get_object_or_404(Extranjero, pk=extranjero_id)
        return context

class DeleteAcompananteVP(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteVP.html'

    def get_success_url(self):
        acompanante = self.object
        extranjero_id = acompanante.delExtranjero.id
        puesta_id = acompanante.delExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Acompañante eliminado con éxito.')

        return reverse_lazy('listAcompanantesVP', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
class DeleteAcompananteVP1(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteVP1.html'

    def get_success_url(self):
        acompanante = self.object
        extranjero_id = acompanante.delAcompanante.id
        puesta_id = acompanante.delAcompanante.deLaPuestaVP.id
        messages.success(self.request, 'Acompañante eliminado con éxito.')
        return reverse_lazy('listAcompanantesVP', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    

class listarTraslado(ListView):
    model = Extranjero
    template_name = "traslados/inicioTraslado.html"
    context_object_name = 'traslado'

    def get_queryset(self):
    # Obtener el perfil del usuario logueado y su estación.
        user_profile = self.request.user
        user_estacion = user_profile.estancia

        # Filtrar todos los extranjeros de la estación con estatus 'Activo'.
        queryset = Extranjero.objects.filter(deLaEstacion=user_estacion, estatus='Activo')

        # Anotar cada objeto en el queryset con el número de relaciones en ExtranjeroTraslado.
        queryset = queryset.annotate(num_traslados=Count('extranjerotraslado'))

        # Filtrar por aquellos que no tienen relaciones con ExtranjeroTraslado.
        queryset = queryset.filter(num_traslados=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        traslado_id = self.kwargs.get('traslado_id', None)
        destino_id = self.kwargs.get('destino_id', None)
        
        # Obtiene la estación destino con el ID
        estacion_destino = Estacion.objects.get(pk=destino_id)
        traslado1 = Traslado.objects.get(pk=traslado_id )
        # Agrega la estación destino al contexto
        context['estacion_destino'] = estacion_destino
        context['traslado1'] = traslado1
        camiones = traslado1.numero_camiones
        capacidad_total = camiones
        context['capacidad_total'] = capacidad_total
        context['navbar'] = 'traslado'
        context['seccion'] = 'traslado'
        
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        estaciones = Estacion.objects.exclude(pk=user_estacion.pk)
        context['estaciones'] = estaciones
        return context
    


def solicitar_traslado(request,self, traslado_id):
    if request.method == 'POST':
        if 'extranjeros[]' in request.POST:
            print("Manejando solicitud de traslado")

            extranjeros = request.POST.getlist('extranjeros[]')
            traslado_id = self.kwargs.get('traslado_id', None)  # Asume que tienes traslado_id en tu URL kwargs

            # Obtiene el objeto Traslado usando el traslado_id
            traslado = get_object_or_404(Traslado, pk=traslado_id)

            # Ahora, para cada extranjero, crea una entrada en ExtranjeroTraslado
            for id in extranjeros:
                extranjero = Extranjero.objects.get(pk=id)
                
                ExtranjeroTraslado.objects.create(
                    statusTraslado=0,  # Suponiendo que 0 es el valor por defecto para 'ACEPTADO'
                    delTraslado=traslado,
                    delExtranjero=extranjero
                )
            
            messages.success(request, 'Solicitudes de traslado realizadas con éxito.')
            return JsonResponse({'status': 'success', 'message': 'Solicitudes de traslado realizadas con éxito.', 'redirect_url': reverse('traslado')})

        messages.error(request, 'Solicitudes de traslado denegada')
        return JsonResponse({'status': 'error', 'message': 'Faltan datos para procesar la solicitud de traslado.','redirect_url': reverse('traslado')})

    return JsonResponse({'error': 'Método no permitido'}, status=405)



class TrasladoCreateView(CreateView):
    model = Traslado
    form_class = TrasladoForm
    template_name = 'traslados/traslado_form.html'  # Este será el nombre del archivo HTML que crearás a continuación.
    success_url = reverse_lazy('traslado')  # Ajusta este nombre según tu archivo urls.py

    def get_initial(self):
        initial = super().get_initial()
        initial['estacion_origen'] = self.kwargs['origen_id']
        initial['estacion_destino'] = self.kwargs['destino_id']
        return initial
    
def procesar_traslado(request):
    if request.method == "POST":
        if 'extranjeros[]' in request.POST:
            print("Manejando solicitud de traslado")

            extranjeros = request.POST.getlist('extranjeros[]')
            traslado_id = request.POST.get('traslado_id')
            print("Extranjeros IDs:", extranjeros)
            print("Traslado ID:", traslado_id)
            traslado_instance = Traslado.objects.get(pk=traslado_id)
         

            for id in extranjeros:
                extranjero = Extranjero.objects.get(pk=id)
                ExtranjeroTraslado.objects.create(
                    statusTraslado=0,
                    delTraslado=traslado_instance,  # Asigna la instancia de Traslado
                    delExtranjero=extranjero
                )

            messages.success(request, 'Solicitudes de traslado realizadas con éxito.')
            return JsonResponse({'status': 'success', 'message': 'Solicitudes de traslado realizadas con éxito.', 'redirect_url': reverse('listTraslado')})

        messages.error(request, 'Solicitudes de traslado denegada')
        return JsonResponse({'status': 'error', 'message': 'Faltan datos para procesar la solicitud de traslado.', 'redirect_url': reverse('listTraslado')})

    return JsonResponse({'error': 'Método no permitido'}, status=405)




# def compare_faces(request):
#     result = None

#     if request.method == "POST":
#         form = CompareFacesForm(request.POST, request.FILES)
#         if form.is_valid():
#             image1 = form.cleaned_data['image1']
#             image2 = form.cleaned_data['image2']

#             # Convertir las imágenes a arrays
#             img1_array = face_recognition.load_image_file(image1)
#             img2_array = face_recognition.load_image_file(image2)

#             # Obtener los encodings
#             encodings1 = face_recognition.face_encodings(img1_array)
#             encodings2 = face_recognition.face_encodings(img2_array)

#             if encodings1 and encodings2:  # Verificar que se detectaron rostros
#                 matches = face_recognition.compare_faces([encodings1[0]], encodings2[0])
#                 result = matches[0]
#             else:
#                 result = "No se detectó rostro en una o ambas imágenes."
#     else:
#         form = CompareFacesForm()

#     return render(request, 'compare_faces.html', {'form': form, 'result': result})

def compare_faces(request):
    result = None
    similarity = None  # Para guardar la similitud (distancia)

    if request.method == "POST":
        form = CompareFacesForm(request.POST, request.FILES)
        if form.is_valid():
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']

            # Convertir las imágenes a arrays
            img1_array = face_recognition.load_image_file(image1)
            img2_array = face_recognition.load_image_file(image2)

            # Obtener los encodings
            encodings1 = face_recognition.face_encodings(img1_array)
            encodings2 = face_recognition.face_encodings(img2_array)

            if encodings1 and encodings2:  # Verificar que se detectaron rostros
                matches = face_recognition.compare_faces([encodings1[0]], encodings2[0])
                result = matches[0]

                # Calcular la distancia (similitud)
                distance = face_recognition.face_distance([encodings1[0]], encodings2[0])
                similarity = f"Similitud: {100 - distance[0]*100:.2f}%"

            else:
                result = "No se detectó rostro en una o ambas imágenes."
    else:
        form = CompareFacesForm()

    return render(request, 'compare_faces.html', {'form': form, 'result': result, 'similarity': similarity})



class UserFaceCreateView(CreateView):
    model = UserFace
    form_class = UserFaceForm
    template_name = 'face_recognition/guardar_fotos.html'
    success_url = reverse_lazy('create_user_face')
    
    def form_valid(self, form):
        form.instance.image.save(form.instance.image.name, form.instance.image, save=True)
        image_path = form.instance.image.path

        # Verificar si la imagen se ha guardado correctamente
        if os.path.exists(image_path):
            print(f"Imagen guardada en {image_path}")
            
            # Carga la imagen
            image_array = face_recognition.load_image_file(image_path)
            
            # Obtén los encodings de la imagen
            face_encodings = face_recognition.face_encodings(image_array)
            
            if face_encodings:  # Verificar que se detectaron rostros
                print("Encoding calculado")
                encoding = face_encodings[0].tolist()
                
                # Guarda el encoding en el modelo y guarda el objeto en la base de datos
                self.object = form.save(commit=False)
                self.object.face_encoding = encoding
                self.object.save()
                
                print("Objeto guardado exitosamente")
                return super().form_valid(form)
            else:
                print("No se pudo calcular face_encodings")
        else:
            print("No se pudo guardar la imagen")

        return self.form_invalid(form)




def search_face(request):
    result = None
    
    if request.method == 'POST':
        form = SearchFaceForm(request.POST, request.FILES)
        
        if form.is_valid():
            start_time = time.time()  # Guarda el tiempo de inicio
            
            uploaded_image = form.cleaned_data['image']
            uploaded_image_array = face_recognition.load_image_file(uploaded_image)
            uploaded_encoding = face_recognition.face_encodings(uploaded_image_array)
            
            if not uploaded_encoding:  # Si no se detectó un rostro
                result = 'No se detectó rostro en la imagen subida.'
            else:
                uploaded_encoding = uploaded_encoding[0]  # Tomar el primer encoding si hay múltiples rostros
                
                for user_face in UserFace.objects.all():
                    saved_encoding = user_face.face_encoding  # El encoding guardado en el modelo
                    
                    if not saved_encoding:
                        continue  # Pasar al siguiente si no hay encoding
                    
                    distance = face_recognition.face_distance([saved_encoding], uploaded_encoding)
                    
                    if distance < 0.6:  # Puedes ajustar el umbral según tus necesidades
                        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                        result = (f'Coincidencia encontrada con {user_face.nombreExtranjero} '
                                  f'(Distancia: {distance[0]}). '
                                  f'Tiempo de búsqueda: {elapsed_time:.2f} segundos.')
                        break  # Salir del bucle si se encuentra una coincidencia
                else:  # Se ejecuta si no se rompió el bucle (no se encontró coincidencia)
                    elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                    result = f'No se encontraron coincidencias. Tiempo de búsqueda: {elapsed_time:.2f} segundos.'
    else:
        form = SearchFaceForm()
    
    return render(request, 'face_recognition/search_face.html', {'form': form, 'result': result})


@csrf_exempt
def manejar_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        puesta_id = request.POST.get('puesta_id')  # Obtén el puesta_id desde los datos del formulario


        try:
            # Conversion de la imagen subida
            imagen_bytes_io = BytesIO(imagen.read())
            imagen_pil = Image.open(imagen_bytes_io)

            if imagen_pil.mode != 'RGB':
                imagen_pil = imagen_pil.convert('RGB')

            imagen_array = np.array(imagen_pil)

            if not isinstance(imagen_array, np.ndarray):
                return JsonResponse({'error': 'Failed to load image'}, status=400)

            # Obteniendo los encodings de la imagen subida
            encodings_subido = face_recognition.face_encodings(imagen_array)

            if not encodings_subido:
                return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)

            uploaded_encoding = encodings_subido[0]
            tolerance = 0.5  # Puedes ajustar este valor

            # Buscar similitud en todas las imágenes almacenadas
            similar_face_id = None

            for biometrico in Biometrico.objects.all():
                face_encoding_almacenado = biometrico.face_encoding

                if not face_encoding_almacenado:
                    continue

                distance = face_recognition.face_distance([face_encoding_almacenado], uploaded_encoding)
                distance_value = float(distance[0])

                if distance_value < tolerance:
                    # Si se encuentra una coincidencia, guarda el ID del registro correspondiente
                    similar_face_id = biometrico.Extranjero_id
                    
                    
                    break  # No es necesario buscar más si se encuentra una coincidencia

            if similar_face_id is not None:
                    puesta_id = request.POST.get('puesta_id')
                    redirect_url = reverse('editarExtranjeroINMproceso', args=[similar_face_id, puesta_id])
                    return JsonResponse({'match': True, 'extranjero_id': similar_face_id, 'redirect_url': redirect_url})
            else:
                # Si no se encontraron coincidencias
                return JsonResponse({'match': False})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@csrf_exempt
def manejar_imagen2(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        puesta_id = request.POST.get('puesta_id')  # Obtén el puesta_id desde los datos del formulario


        try:
            # Conversion de la imagen subida
            imagen_bytes_io = BytesIO(imagen.read())
            imagen_pil = Image.open(imagen_bytes_io)

            if imagen_pil.mode != 'RGB':
                imagen_pil = imagen_pil.convert('RGB')

            imagen_array = np.array(imagen_pil)

            if not isinstance(imagen_array, np.ndarray):
                return JsonResponse({'error': 'Failed to load image'}, status=400)

            # Obteniendo los encodings de la imagen subida
            encodings_subido = face_recognition.face_encodings(imagen_array)

            if not encodings_subido:
                return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)

            uploaded_encoding = encodings_subido[0]
            tolerance = 0.5  # Puedes ajustar este valor

            # Buscar similitud en todas las imágenes almacenadas
            similar_face_id = None

            for biometrico in Biometrico.objects.all():
                face_encoding_almacenado = biometrico.face_encoding

                if not face_encoding_almacenado:
                    continue

                distance = face_recognition.face_distance([face_encoding_almacenado], uploaded_encoding)
                distance_value = float(distance[0])

                if distance_value < tolerance:
                    # Si se encuentra una coincidencia, guarda el ID del registro correspondiente
                    similar_face_id = biometrico.Extranjero_id
                    
                    
                    break  # No es necesario buscar más si se encuentra una coincidencia

            if similar_face_id is not None:
                    puesta_id = request.POST.get('puesta_id')
                    redirect_url = reverse('editarExtranjeroACproceso', args=[similar_face_id, puesta_id])
                    return JsonResponse({'match': True, 'extranjero_id': similar_face_id, 'redirect_url': redirect_url})
            else:
                # Si no se encontraron coincidencias
                return JsonResponse({'match': False})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def manejar_imagen3(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        puesta_id = request.POST.get('puesta_id')  # Obtén el puesta_id desde los datos del formulario


        try:
            # Conversion de la imagen subida
            imagen_bytes_io = BytesIO(imagen.read())
            imagen_pil = Image.open(imagen_bytes_io)

            if imagen_pil.mode != 'RGB':
                imagen_pil = imagen_pil.convert('RGB')

            imagen_array = np.array(imagen_pil)

            if not isinstance(imagen_array, np.ndarray):
                return JsonResponse({'error': 'Failed to load image'}, status=400)

            # Obteniendo los encodings de la imagen subida
            encodings_subido = face_recognition.face_encodings(imagen_array)

            if not encodings_subido:
                return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)

            uploaded_encoding = encodings_subido[0]
            tolerance = 0.5  # Puedes ajustar este valor

            # Buscar similitud en todas las imágenes almacenadas
            similar_face_id = None

            for biometrico in Biometrico.objects.all():
                face_encoding_almacenado = biometrico.face_encoding

                if not face_encoding_almacenado:
                    continue

                distance = face_recognition.face_distance([face_encoding_almacenado], uploaded_encoding)
                distance_value = float(distance[0])

                if distance_value < tolerance:
                    # Si se encuentra una coincidencia, guarda el ID del registro correspondiente
                    similar_face_id = biometrico.Extranjero_id
                    
                    
                    break  # No es necesario buscar más si se encuentra una coincidencia

            if similar_face_id is not None:
                    puesta_id = request.POST.get('puesta_id')
                    redirect_url = reverse('editarExtranjeroVPproceso', args=[similar_face_id, puesta_id])
                    return JsonResponse({'match': True, 'extranjero_id': similar_face_id, 'redirect_url': redirect_url})
            else:
                # Si no se encontraron coincidencias
                return JsonResponse({'match': False})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
def compare_faces(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        extranjero_id_str = request.POST.get('extranjero_id')

        # Verifica si el extranjero_id es None o si no es un número válido
        if extranjero_id_str is None or not extranjero_id_str.isdigit():
            return JsonResponse({'error': 'Invalid extranjero_id'}, status=400)

        extranjero_id = int(extranjero_id_str)  # Convertir a entero
        print(type(extranjero_id))  # <class 'int'>
        print(extranjero_id)  
        try:
            # Obtener el objeto Biometrico asociado con el Extranjero_id
      # Debería ser un número entero válido
            biometrico = Biometrico.objects.get(Extranjero=extranjero_id)
            # ...

            # Cargar face_encoding almacenado
            face_encoding_almacenado = biometrico.face_encoding

            # Convertir imagen subida a formato que face_recognition puede entender
            imagen = face_recognition.load_image_file(InMemoryUploadedFile(imagen))

            # Obtener los encodings de la imagen subida
            encodings_subido = face_recognition.face_encodings(imagen)
            
            if not encodings_subido:  # Verificar que se detectaron rostros en la imagen subida
                return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)
            
            # Comparar face_encoding_subido con face_encoding_almacenado
            matches = face_recognition.compare_faces([face_encoding_almacenado], encodings_subido[0])
            
            # También puedes calcular la distancia si lo necesitas
            distance = face_recognition.face_distance([face_encoding_almacenado], encodings_subido[0])
            similarity = f"Similitud: {100 - distance[0]*100:.2f}%"
            
            return JsonResponse({'match': matches[0], 'similarity': similarity})
        
        except Biometrico.DoesNotExist:
            return JsonResponse({'error': 'Biometrico does not exist for given extranjero_id'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    


class ResumenViewINM(DetailView):
    model = Extranjero
    template_name = 'puestaINM/resumenExtranjeroINM.html'
    context_object_name = 'extranjero'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero = self.object
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        context['puesta'] = extranjero.deLaPuestaIMN
        return context 



# Listar extranjeros de forma global por estacion

class listarExtranjerosEstacion(ListView):
    model = Extranjero
    template_name = 'extranjeros/listExtranjerosEstacion.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        # Obtener la estación del usuario actualmente autenticado.
        estacion_usuario = self.request.user.estancia

        estado = self.request.GET.get('estado_filtrado', 'activo')
        # Filtrar por estación del usuario y ordenar por nombre de extranjero.
        queryset = Extranjero.objects.filter(deLaEstacion=estacion_usuario).order_by('nombreExtranjero')

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset


    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        context['nombre_estacion'] = self.request.user.estancia.nombre

        ahora = timezone.now() # Hora Actual

        for extranjero in context['extranjeros']:
            tiempo_transcurrido = ahora - extranjero.horaRegistro
            horas_transcurridas, minutos_transcurridos = divmod(tiempo_transcurrido.total_seconds() / 3600, 1)
            horas_transcurridas = int(horas_transcurridas)
            minutos_transcurridos = int(minutos_transcurridos * 60)

            # Limitar a un máximo de 36 horas
            if horas_transcurridas > 36:
                horas_transcurridas = 36
                minutos_transcurridos = 0

            extranjero.horas_transcurridas = horas_transcurridas
            extranjero.minutos_transcurridos = minutos_transcurridos

            
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_notificacion = False
            if ultimo_nup:
                notificacion = NotificacionDerechos.objects.filter(no_proceso_id=ultimo_nup).first()
                if notificacion:
                    extranjero.tiene_notificacion_derechos = True
                    extranjero.fecha_aceptacion = notificacion.fechaAceptacion
                    extranjero.estacion_notificacion = notificacion.estacion
                else:
                    extranjero.tiene_notificacion_derechos = False
                    extranjero.fecha_aceptacion = None
                    extranjero.hora_aceptacion = None
                    extranjero.estacion_notificacion = None

            if ultimo_nup:
                notificacion = Notificacion.objects.filter(nup=ultimo_nup).first()
                if notificacion:
                    tiene_notificacion = True

            extranjero.tiene_notificacion = tiene_notificacion

        for extranjero in context['extranjeros']:
                ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
                tiene_enseres = False

                if ultimo_nup:
                    enseres = EnseresBasicos.objects.filter(nup=ultimo_nup).first()
                    if enseres:
                        tiene_enseres = True

                extranjero.tiene_enseres = tiene_enseres

        for extranjero in context['extranjeros']:
                ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
                tiene_inventario = False

                if ultimo_nup:
                    inventario = Inventario.objects.filter(nup=ultimo_nup).first()
                    if inventario:
                        tiene_inventario = True

                extranjero.tiene_inventario = tiene_inventario
        return context
     
    

class qrs(TemplateView):
    template_name='qr.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        qr_link = f"https://740a-187-187-225-64.ngrok-free.app/seguridad/crear_firma/{extranjero_id}"
        extranjero = get_object_or_404(Extranjero, id=extranjero_id)
        nombre = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero +" "+ extranjero.apellidoMaternoExtranjero
        context['initial_qr_link'] = qr_link
        context['nombre'] = nombre
        return context
    
def verificar_firma(request, extranjero_id):
    try:
        firma = Firma.objects.get(extranjero_id=extranjero_id)
        if firma.firma_imagen:
            return JsonResponse({"firmado": True})
        else:
            return JsonResponse({"firmado": False})
    except Firma.DoesNotExist:
        return JsonResponse({"firmado": False})
    

class FirmaCreateView(CreateView):
    model = Firma
    form_class = FirmaForm
    template_name = 'modal/firma.html'
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        
        # Verifica si el extranjero ya tiene una firma
        if hasattr(extranjero, 'firma'):
            # Aquí decides qué hacer si ya existe una firma
            # Por ejemplo, puedes redirigir al usuario a otra página o mostrar un mensaje de error
            return HttpResponse("El extranjero ya tiene una firma.")
        else:
            firma = form.save(commit=False)
            firma.extranjero = extranjero

            # Toma la cadena dataURL desde el formulario
            firma_data_url = form.cleaned_data.get('firma_imagen')
            format, imgstr = firma_data_url.split(';base64,')
            ext = format.split('/')[-1]

            # Crea un archivo de imagen desde la cadena dataURL
            firma_image = ContentFile(base64.b64decode(imgstr), name=f"firma_{firma.id}.{ext}")

            firma.firma_imagen.save(firma_image.name, firma_image)
            firma.save()

            return super().form_valid(form)

    def get_success_url(self):
        # Redirige a donde desees después de guardar la firma
        return reverse_lazy('menu')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extranjero_id'] = self.kwargs.get('extranjero_id')
        return context