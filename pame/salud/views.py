from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from vigilancia.models import Extranjero, NoProceso
from .models import DocumentosReferencia,CertificadoMedico, PerfilMedico, Consulta, constanciaNoLesiones, CertificadoMedicoEgreso, ReferenciaMedica, FirmaMedico, DocumentosExternos
from catalogos.models import Estacion
from .forms import certificadoMedicoForms, perfilMedicoforms, consultaForms, lesionesForm, certificadoMedicoEgresoForms, referenciaMedicaforms, DocumentosReferenciaForm, FirmaMedicoForm, DocumentosExternosForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from io import BytesIO
from PIL import Image  # Asegúrate de importar Image de PIL o Pillow
import numpy as np 
from vigilancia.models import Biometrico
from django.core.files.uploadedfile import InMemoryUploadedFile
import face_recognition
from django.db.models import Max
from django.db.models import Exists, OuterRef
from django.shortcuts import get_object_or_404
from django.conf import settings
import os
from django.shortcuts import redirect
from django.core.files.base import ContentFile
import base64
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from usuarios.models import Usuario
from generales.mixins import HandleFileMixin

# Create your views here.
 
def homeMedico(request):
    return render(request, "home.html")


def homeMedicoGeneral(request):
    return render(request, "home/homeMedicoGeneral.html")



def homeMedicoResponsable(request):
    return render(request, "home/homeMedicoResponsable.html")

class listaExtranjerosEstacion(LoginRequiredMixin, ListView):
    model = Extranjero
    template_name='servicioInterno/extranjeroEstacion.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  
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
        tiene_perfil_medico = PerfilMedico.objects.filter(usuario=self.request.user).exists()
        context['tiene_perfil_medico'] = tiene_perfil_medico
        
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_certificadoMedico = False

            if ultimo_nup:
                certificado = CertificadoMedico.objects.filter(nup=ultimo_nup).first()
                if certificado:
                    tiene_certificadoMedico = True
                    fecha =certificado.fechaHoraCertificado
                    estacion = certificado.delaEstacion
                    context['fecha'] = fecha  # Cambia esto según la página activa
                    context['estacion'] = estacion  # Cambia esto según la página activa


            extranjero.tiene_certificadoMedico = tiene_certificadoMedico
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_constanciaLesiones = False

            if ultimo_nup:
                constancia = constanciaNoLesiones.objects.filter(nup=ultimo_nup).first()
                if constancia:
                    tiene_constanciaLesiones = True
                    fecha =constancia.fechaHoraCertificado
                    estacion = constancia.delaEstacion
                    context['fecha'] = fecha  # Cambia esto según la página activa
                    context['estacion'] = estacion  # Cambia esto según la página activa


            extranjero.tiene_constanciaLesiones = tiene_constanciaLesiones
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_egreso = False

            if ultimo_nup:
                egreso = CertificadoMedicoEgreso.objects.filter(nup=ultimo_nup).first()
                if egreso:
                    tiene_egreso = True
                    fecha =egreso.fechaHoraCertificado
                    estacion = egreso.delaEstacion
                    context['fecha'] = fecha  # Cambia esto según la página activa
                    context['estacion'] = estacion  # Cambia esto según la página activa


            extranjero.tiene_egreso = tiene_egreso
        context['navbar'] = 'medico'  # Cambia esto según la página activa
        context['seccion'] = 'interno'  # Cambia esto según la página activa
        context['nombre_estacion'] = self.request.user.estancia.nombre

        return context
    
    
class certificadoMedico(LoginRequiredMixin, CreateView):
    template_name = 'servicioInterno/certificadoMedico.html'
    model = CertificadoMedico # Utiliza el modelo para crear objetos
    form_class = certificadoMedicoForms
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        extranjero_id = self.kwargs.get('pk')

        messages.success(self.request, 'Certificado medico creado con éxito.')
        if self.object.tratamiento:
            # Si el tratamiento es verdadero, redirige a la plantilla correspondiente
            return reverse('consulta',kwargs={'pk': extranjero_id})  # Reemplaza 'nombre_de_tu_plantilla_verdadera' con el nombre correcto
        else:
            # Si el tratamiento es falso, redirige a otra plantilla
            return reverse('listExtranjeroEstacion')
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['delaEstacion'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup      
        perfil_medico = PerfilMedico.objects.get(usuario=usuario)
        initial['delMedico'] = perfil_medico  
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'interno'    
        context['extranjero_id']= extranjero_id 
        return context
    
class certificadoEgreso(LoginRequiredMixin, CreateView):
    template_name = 'servicioInterno/certificadoEgreso.html'
    model = CertificadoMedicoEgreso # Utiliza el modelo para crear objetos
    form_class = certificadoMedicoEgresoForms
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Certificado medico de egreso creado con éxito.')
        return reverse('listExtranjeroEstacion')
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['delaEstacion'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup      
        perfil_medico = PerfilMedico.objects.get(usuario=usuario)
        initial['delMedico'] = perfil_medico  
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'interno'    
        context['extranjero_id']= extranjero_id 
        return context
class listarExtranjerosServicioExterno(LoginRequiredMixin, ListView):
    model = Extranjero
    template_name='servicioExterno/listaExtranjeroEstacion.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  
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
        context['navbar'] = 'medico'  # Cambia esto según la página activa
        context['seccion'] = 'externo'  # Cambia esto según la página activa
        context['nombre_estacion'] = self.request.user.estancia.nombre

        return context
    
    
class perfilMedicoInterno(LoginRequiredMixin, CreateView):
    template_name = 'servicioInterno/perfilMedico.html'
    login_url = '/permisoDenegado/'
    model = PerfilMedico # Utiliza el modelo para crear objetos
    form_class = perfilMedicoforms
    def get_success_url(self):
        messages.success(self.request, 'Perfil medico creado con éxito.')
        return reverse('listExtranjeroEstacion')
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            usuario_data = self.request.user  # El usuario logeado
            initial['usuario'] = usuario_data.pk
            initial['nombreMedico'] = usuario_data.first_name
            initial['apellidosMedico'] = usuario_data.last_name
            # Agrega más campos según sea necesario
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            usuario_data = self.request.user  # El usuario logeado
            context['nombreMedico'] = usuario_data.first_name
            context['apellidosMedico'] = usuario_data.last_name
        context['navbar'] = 'medico'
        context['seccion'] = 'Medicointerno'      
        return context
class consultaMedica(LoginRequiredMixin, CreateView):
    template_name = 'servicioInterno/consultaMedica.html'
    model = Consulta # Utiliza el modelo para crear objetos
    form_class = consultaForms
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        extranjero_id = self.kwargs.get('pk')
        messages.success(self.request, 'Consulta medica registrada con éxito.')
        if self.object.referencia:
            # Si el tratamiento es verdadero, redirige a la plantilla correspondiente
            return reverse('referenciaMedica',kwargs={'pk': extranjero_id})  # Reemplaza 'nombre_de_tu_plantilla_verdadera' con el nombre correcto
        else:
            # Si el tratamiento es falso, redirige a otra plantilla
           return reverse('listConsultas',kwargs={'pk': extranjero_id})  # Reemplaza 'nombre_de_tu_plantilla_verdadera' con el nombre correcto
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['delaEstacion'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup      
        perfil_medico = PerfilMedico.objects.get(usuario=usuario)
        initial['delMedico'] = perfil_medico  
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'consulta'    
        context['extranjero_id']= extranjero_id 
        return context
       
class datosDelMedico(TemplateView):
    template_name = 'servicioInterno/datosMedico.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        perfil_medico = PerfilMedico.objects.get(usuario=usuario)
        nombre = perfil_medico.nombreMedico
        ape1 = perfil_medico.apellidosMedico
        cedula = perfil_medico.cedula
        context['nombre'] = nombre # Cambia esto según la página activa
        context['ape1'] = ape1  # Cambia esto según la página activa
        context['cedula'] = cedula  # Cambia esto según la página activa

        context['navbar'] = 'medico'  # Cambia esto según la página activa
        context['seccion'] = 'Medicointerno'        

        return context
    

class listaExtranjerosConsulta(LoginRequiredMixin, ListView):
    model = Extranjero
    template_name='consulta/listaExtranjeros.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  
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
        tiene_perfil_medico = PerfilMedico.objects.filter(usuario=self.request.user).exists()
        context['tiene_perfil_medico'] = tiene_perfil_medico
        
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_certificadoMedico = False

            if ultimo_nup:
                certificado = CertificadoMedico.objects.filter(nup=ultimo_nup).first()
                if certificado:
                    tiene_certificadoMedico = True
                    fecha =certificado.fechaHoraCertificado
                    estacion = certificado.delaEstacion
                    context['fecha'] = fecha  # Cambia esto según la página activa
                    context['estacion'] = estacion  # Cambia esto según la página activa


            extranjero.tiene_certificadoMedico = tiene_certificadoMedico
        context['navbar'] = 'medico'  # Cambia esto según la página activa
        context['seccion'] = 'consulta'  # Cambia esto según la página activa
        context['nombre_estacion'] = self.request.user.estancia.nombre

        return context
    
class listaConsultasExtranjero(LoginRequiredMixin,ListView):
    template_name = 'consulta/histroialConsultas.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    model=Consulta
    context_object_name = 'extranjeros'
    def get_queryset(self):
        extranjero_id = self.kwargs['pk']
        extranjero = Extranjero.objects.get(pk=extranjero_id)

        # Obtener el último nup del extranjero
        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtrar las consultas por el extranjero y el nup más reciente
        queryset = Consulta.objects.filter(extranjero=extranjero_id, nup__consecutivo=ultimo_nup)
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        ultimo_nup = Extranjero.objects.get(pk=extranjero_id).noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'consulta'    
        context['extranjero_id']= extranjero_id 
        context['extranjeros'] = Consulta.objects.filter(extranjero=extranjero_id, nup__consecutivo=ultimo_nup).annotate(
            tiene_referencia_medica=Exists(ReferenciaMedica.objects.filter(consulta=OuterRef('pk'))),
            # Añadir otras anotaciones si es necesario
        )
        return context
    
class constanciaLesiones(LoginRequiredMixin, CreateView):
    template_name='servicioInterno/lesiones.html'
    model = constanciaNoLesiones
    form_class = lesionesForm
    login_url ='/permisoDenegado/'
    def get_success_url(self):

        messages.success(self.request, 'Constancia de no lesiones creada con éxito.')
        return reverse('listExtranjeroEstacion')
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['delaEstacion'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup      
        perfil_medico = PerfilMedico.objects.get(usuario=usuario)
        initial['delMedico'] = perfil_medico  
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'interno'    
        return context
class referencia(LoginRequiredMixin, CreateView):
    template_name='servicioInterno/referenciaMedica.html'
    model = ReferenciaMedica
    form_class = referenciaMedicaforms
    login_url ='/permisoDenegado/'
    def get_success_url(self):
        extranjero_id = self.kwargs.get('pk')
        messages.success(self.request, 'Referencia medica registrada con éxito.')
        return reverse('listConsultas',kwargs={'pk': extranjero_id}) 
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['delaEstacion'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultima_consulta = Consulta.objects.filter(extranjero=extranjero_id).latest('fechaHoraConsulta')

        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup      
        perfil_medico = PerfilMedico.objects.get(usuario=usuario)
        initial['delMedico'] = perfil_medico  
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        initial['consulta'] = ultima_consulta.id

        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'interno'    
        return context
class documentosReferencia(LoginRequiredMixin, CreateView, HandleFileMixin):
    template_name='servicioInterno/cargaDocumentos.html'
    model = DocumentosReferencia
    form_class = DocumentosReferenciaForm
    login_url ='/permisoDenegado/'
    def get_success_url(self):
        referencia_id = self.kwargs.get('referencia_id')
        referencia = get_object_or_404(ReferenciaMedica, id=referencia_id)
        extranjero_id = referencia.extranjero.pk

        messages.success(self.request, 'Documentos subidos con éxito.')
        return reverse('listConsultas',kwargs={'pk': extranjero_id}) 
    def form_valid(self, form):
        # Obtiene la referencia
        referencia_id = self.kwargs.get('referencia_id')
        referencia = get_object_or_404(ReferenciaMedica, id=referencia_id)

        # Guarda cada archivo en una instancia diferente de documentosReferencia
        for file in self.request.FILES.getlist('documento'):
            documento_referencia = form.save(commit=False)
            documento_referencia.documento = file
            documento_referencia.deReferencia = referencia
            documento_referencia.save()

        instance = form.save()  
        self.handle_file(instance,'documento')
        return super(documentosReferencia, self).form_valid(form)
    def get_initial(self):
        initial = super().get_initial()

        # Obtén el ID de la referencia y establece el valor inicial del campo deReferencia
        referencia_id = self.kwargs.get('referencia_id')
        initial['deReferencia'] = referencia_id

        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtén el ID de la referencia
        referencia_id = self.kwargs.get('referencia_id')
        referencia = get_object_or_404(ReferenciaMedica, id=referencia_id)
        nombre = referencia.extranjero.nombreExtranjero
        context['navbar'] = 'medico'
        context['seccion'] = 'consulta'    
        context['referencia_id'] = referencia_id  # Agrega el ID de la referencia al contexto
        context['referencia']= referencia

        return context

class listaDocumentos(LoginRequiredMixin, ListView):
    template_name = 'servicioInterno/listaDocumentos.html'
    model = DocumentosReferencia
    context_object_name = 'documentos'
    login_url = '/permisoDenegado/'

    def get_queryset(self):
        consulta_id = self.kwargs['consulta_id']

        # Obtener la referencia médica asociada a la consulta
        referencia_medica = get_object_or_404(ReferenciaMedica, consulta_id=consulta_id)
        # Filtra los documentos que están relacionados con la misma referencia médica
        doc = DocumentosReferencia.objects.filter(deReferencia=referencia_medica)
        queryset = doc
        return queryset

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     consulta_id = self.kwargs['consulta_id']
     context['consulta_id'] = consulta_id

     referencia_medica = get_object_or_404(ReferenciaMedica, consulta_id=consulta_id)
     context['referencia_medica'] = referencia_medica
    
    # Filtra los documentos que están relacionados con la misma referencia médica
     documentos = DocumentosReferencia.objects.filter(deReferencia=referencia_medica)
     dd = documentos.last
  

    # Obtener la referencia médica asociada a la consulta
     if referencia_medica:
        context['extranjero'] = referencia_medica.extranjero
        context['consulta'] = referencia_medica.consulta
     context['navbar'] = 'medico'
     context['seccion'] = 'consulta'
     return context
class QrsMedico(LoginRequiredMixin, TemplateView):
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    template_name = 'qrMedico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user
        
        qr_link = f"http://192.168.1.129:8082/salud/crear_firma_Medico/{usuario.id}"

        context['initial_qr_link'] = qr_link
        context['nombre'] = usuario.first_name
        context['apellidoP'] = usuario.last_name

        return context
def verificar_firma(request, pk):
    try:
        firma = FirmaMedico.objects.get(medico=pk)
        if firma.firma_imagen:
            # Construye la URL completa para la imagen
            url_imagen = os.path.join(settings.MEDIA_URL, str(firma.firma_imagen))
            return JsonResponse({"firmado": True, "url_imagen_firma": url_imagen})
        else:
            return JsonResponse({"firmado": False})
    except FirmaMedico.DoesNotExist:
        return JsonResponse({"firmado": False})
class FirmaCreateMedicoView(CreateView):
    model = FirmaMedico
    form_class = FirmaMedicoForm
    template_name = 'firmaMedico.html'
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('pk')

        extranjero = Usuario.objects.get(pk=extranjero_id)
        
        # Verifica si el extranjero ya tiene una firma
        if hasattr(extranjero, 'firma'):
            # Aquí decides qué hacer si ya existe una firma
            # Por ejemplo, puedes redirigir al usuario a otra página o mostrar un mensaje de error
          return redirect(reverse('firma_existente'))
        else:
            firma = form.save(commit=False)
            firma.medico = extranjero

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
        return reverse_lazy('firma_exitosa')
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs.get('pk')
        return context
    
class documentosExternos(LoginRequiredMixin, CreateView, HandleFileMixin):
    template_name='servicioExterno/cargaDeCertificados.html'
    model = DocumentosExternos
    form_class = DocumentosExternosForm
    login_url ='/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Documentos subidos con éxito.')
        return reverse('listExtranjeroExterno') 
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['deLaEstacion'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup       
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'externo'    

        return context
    def form_valid(self, form):
        instance = form.save()  
        self.handle_file(instance,'documento')
        return super(documentosExternos, self).form_valid(form)
    
class listaDExternos(LoginRequiredMixin, ListView):
    template_name = 'servicioExterno/listaDocumentosExternos.html'
    model = DocumentosExternos
    context_object_name = 'documentos'
    login_url = '/permisoDenegado/'   
    def get_queryset(self):
        extranjero_id = self.kwargs['pk']

        # Obtener el último NUP asociado al extranjero
        ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtrar los documentos externos por el ID del extranjero y el último NUP
        queryset = DocumentosExternos.objects.filter(
            extranjero_id=extranjero_id,
            nup__consecutivo=ultimo_nup
        )

        return queryset

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     extranjero_id = self.kwargs['pk']
    
    # Filtra los documentos que están relacionados con la misma referencia médica
     documentos = DocumentosExternos.objects.filter(extranjero=extranjero_id)
     dd = documentos.last
     extranjero = Extranjero.objects.get(id=extranjero_id)
     nombre = extranjero.nombreExtranjero
     ape1 = extranjero.apellidoPaternoExtranjero
     ape2 = extranjero.apellidoMaternoExtranjero
     context['extranjero']=extranjero
     context['nombre'] = nombre
     context['ape1'] = ape1
     context['ape2'] = ape2
    # Obtener la referencia médica asociada a la consulta

     context['navbar'] = 'medico'
     context['seccion'] = 'externo'
     return context

def manejar_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        extranjero_id_str = request.POST.get('extranjero_id')
     
        if extranjero_id_str is None or not extranjero_id_str.isdigit():
            return JsonResponse({'error': 'Invalid llamada_id'}, status=400)

        extranjero_id = int(extranjero_id_str)

        try:
            biometrico = Biometrico.objects.get(Extranjero=extranjero_id)
            face_encoding_almacenado = biometrico.face_encoding

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

            distance = face_recognition.face_distance([face_encoding_almacenado], uploaded_encoding)
            distance_value = float(distance[0])
            
            if distance_value < tolerance:
                similarity_str = f"Similitud: {(1 - distance_value) * 100:.2f}%"
                return JsonResponse({'match': True, 'similarity': similarity_str, 'distance': distance_value})
            else:
                return JsonResponse({'match': False, 'similarity': None, 'distance': distance_value})

        except Biometrico.DoesNotExist:
            return JsonResponse({'error': 'Biometrico does not exist for given extranjero_id'}, status=400)
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
