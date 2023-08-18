from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Extranjero, PuestaDisposicionAC, PuestaDisposicionINM, Biometrico, Acompanante
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import extranjeroFormsAC, extranjeroFormsInm, puestDisposicionINMForm, puestaDisposicionACForm, BiometricoFormINM, BiometricoFormAC, acompananteForms
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalogos.models import Estacion
from django.shortcuts import get_object_or_404


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

   



# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "home/homeSeguridadGeneral.html",{'navbar':'home'})




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

        return context


class createPuestaINM(CreatePermissionRequiredMixin,CreateView):
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
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        # Generar el número con formato automáticamente
        ultimo_registro = PuestaDisposicionINM.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroOficio.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INM/{estacion_id}/{UsuarioId}/{ultimo_numero + 1:04d}'

        initial['numeroOficio'] = nuevo_numero
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context

class createExtranjeroINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'puestaINM/crearExtranjeroINM.html' 
    # success_url = reverse_lazy('homePuestaINM')
    
    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']

        extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        
        if self.object.viajaSolo:
            return reverse('agregar_biometricoINM', args=[extranjero_id])
        else:
            return reverse('createAcompananteINM')
    
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
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass

        ultimo_registro = Extranjero.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroExtranjero.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/EXT/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroExtranjero'] = nuevo_numero
        return {'deLaPuestaIMN': puesta, 'deLaEstacion':estacion, 'numeroExtranjero':nuevo_numero, 'viajaSolo':viaja_solo} 

    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        extranjero = form.save(commit=False)  # Crea una instancia de Extranjero sin guardarla en la base de datos
        extranjero.puesta = puesta
        extranjero.save()  #
        
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
        return Extranjero.objects.filter(deLaPuestaIMN_id=puesta_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)  # Asegúrate de reemplazar 'Puesta' con el nombre correcto de tu modelo
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class EditarExtranjeroINM(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = extranjeroFormsInm
    template_name = 'puestaINM/editarExtranjeroINM.html'

    def get_success_url(self):
        return reverse('listarExtranjeros', args=[self.object.deLaPuestaIMN.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta'] = self.object.deLaPuestaIMN
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
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context

class EditarBiometricoINM(UpdateView):
    model = Biometrico
    form_class = BiometricoFormINM
    template_name = 'puestaINM/editBiometricosINM.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
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
        return context


class DeleteExtranjeroINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Extranjero
    template_name = 'puestaINM/eliminarExtranjeroINM.html'
    
    def get_success_url(self):
        puesta_id = self.object.deLaPuestaIMN.id
        return reverse('listarExtranjeros', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class acompananteCreateINM(CreateView):
    model = Acompanante
    form_class = acompananteForms
    template_name = 'puestaINM/acompanantesINM.html'
    success_url = reverse_lazy('homePuestaINM')

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        return Extranjero.objects.filter(deLaPuestaIMN_id=puesta_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        
        # Filtrar extranjeros por la puesta actual
        extranjeros = self.get_queryset()
        
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        
        context['puesta'] = puesta
        context['extranjeros'] = extranjeros  # Pasar los extranjeros filtrados al contexto
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        
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

        return context
    
class createPuestaAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicionac',
    }
    model = PuestaDisposicionAC               
    form_class = puestaDisposicionACForm      
    template_name = 'puestaAC/createPuestaAC.html'  
    success_url = reverse_lazy('homePuestaAC')

    def get_initial(self):
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
        except Usuario.DoesNotExist:
            pass
         # Generar el número con formato automáticamente
        ultimo_registro = PuestaDisposicionAC.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroOficio.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/AC/{estacion_id}/{usuario_id}/{ultimo_numero + 1:04d}'

        initial['numeroOficio'] = nuevo_numero
        return initial

        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
    
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
            return reverse('agregar_biometricoAC', args=[extranjero_id])
        else:
            # return reverse('crearExtranjeroAC', args=[puesta_id])
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
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        ultimo_registro = Extranjero.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroExtranjero.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/EXT/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroExtranjero'] = nuevo_numero
        viaja_solo = True
        initial['viajaSolo'] = viaja_solo
        return {'deLaPuestaAC': puesta, 'deLaEstacion':estacion, 'numeroExtranjero':nuevo_numero, 'viajaSolo': viaja_solo } 
     
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        extranjero = form.save(commit=False)  # Crea una instancia de Extranjero sin guardarla en la base de datos
        extranjero.puesta = puesta
        extranjero.save()  #
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
        return Extranjero.objects.filter(deLaPuestaAC_id=puesta_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)  # Asegúrate de reemplazar 'Puesta' con el nombre correcto de tu modelo
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class EditarExtranjeroAC(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = extranjeroFormsAC
    template_name = 'puestaAC/editarExtranjeroAC.html'

    def get_success_url(self):
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

class AgregarBiometricoAC(CreateView):
    model = Biometrico
    form_class = BiometricoFormAC
    template_name = 'puestaAC/createBiometricosAC.html'  # Cambiar a la ruta correcta

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    
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
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaAC
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context

class EditarBiometricoAC(UpdateView):
    model = Biometrico
    form_class = BiometricoFormAC
    template_name = 'puestaAC/editBiometricosAC.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaAC
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context

class DeleteExtranjeroAC(DeleteView):
    model = Extranjero
    template_name = 'puestaAC/eliminarExtranjeroAC.html'
    
    def get_success_url(self):
        puesta_id = self.object.deLaPuestaAC.id
        return reverse('listarExtranjeroAC', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaAC.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class createAcompananteAC(CreateView):
    model = Acompanante          
    form_class = acompananteForms      
    template_name = 'puestaAC/createAcompananteAC.html'  
    success_url = reverse_lazy('homePuestaAC')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
    
class ListAcompanantesAC(ListView):
    model = Extranjero
    template_name= 'puestaAC/listAcompanantesAC.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)

        # Obtener la lista de extranjeros de la misma puesta
        extranjeros_puesta = Extranjero.objects.filter(deLaPuestaAC_id=puesta_id).exclude(pk=extranjero_principal_id)

        context['extranjero_principal'] = extranjero_principal
        context['extranjeros_puesta'] = extranjeros_puesta

        return context