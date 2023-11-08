from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from vigilancia.models import Extranjero
from .models import CertificadoMedico, PerfilMedico
from catalogos.models import Estacion
from .forms import certificadoMedicoForms, perfilMedicoforms
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse

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
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
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
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'interno'        
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
    
class CargaCertificadoMedico(LoginRequiredMixin, TemplateView):
    template_name = 'servicioExterno/cargaDeCertificados.html'
    login_url = '/permisoDenegado/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        context['nombre'] = nombre
        context['navbar'] = 'medico'  # Cambia esto según la página activa
        context['seccion'] = 'externo'  # Cambia esto según la página activa

        return context
    
class perfilMedicoInterno(LoginRequiredMixin, CreateView):
    template_name = 'servicioInterno/perfilMedico.html'
    login_url = '/permisoDenegado/'
    model = PerfilMedico # Utiliza el modelo para crear objetos
    form_class = perfilMedicoforms
    def get_success_url(self):
        messages.success(self.request, 'Datos del extranjero editados con éxito.')
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