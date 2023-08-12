from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Extranjero, PuestaDisposicionAC, PuestaDisposicionINM
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import extranjeroFormsAC, extranjeroFormsInm, puestDisposicionINMForm, puestaDisposicionACForm
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages

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

class inicioINMList(ListView):
    model = PuestaDisposicionINM          
    template_name = "home/puestas/homePuestaINM.html" 
    context_object_name = 'puestasinm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context


class inicioACList(ListView):
    model = PuestaDisposicionAC
    template_name = "home/puestas/homePuestaAC.html" 
    context_object_name = 'puestaAC'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context

class createPuestaINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicioninm',
    }
    model = PuestaDisposicionINM               
    form_class = puestDisposicionINMForm      
    template_name = 'home/puestas/createPuestaINM.html'  
    success_url = reverse_lazy('homePuestaINM')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context


class createPuestaAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicionac',
    }
    model = PuestaDisposicionAC
    form_class = puestaDisposicionACForm
    template_name = 'home/puestas/createPuestaAC.html'  
    success_url = reverse_lazy('homePuestaAC')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context



class createExtranjeroINM(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'home/puestas/crearExtranjeroINM.html' 
    success_url = reverse_lazy('homePuestaINM')

    def get_initial(self):
        initial = super().get_initial()
        initial['deLaPuestaIMN'] = self.kwargs['puesta_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.kwargs['puesta_id']
        context['navbar'] = 'seguridad'  # Agrega esto para el componente activo del navbar
        
        return context
    

    # def get_success_url(self):
    #     return f'//{self.kwargs["puesta_id"]}/'



class createExtranjeroAC(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'home/puestas/createExtranjeroAC.html' 
    success_url = reverse_lazy('homePuestaAC')

    def get_initial(self):
        initial = super().get_initial()
        initial['deLaPuestaAC'] = self.kwargs['puesta_id']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.kwargs['puesta_id']
        context['navbar'] = 'seguridad'  # Agrega esto para el componente activo del navbar

        return context
    
class listarExtranjeros(ListView):
    model = Extranjero
    template_name = 'home/puestas/listExtranjenros.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        queryset = Extranjero.objects.filter(deLaPuestaIMN=puesta)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad'  # Agrega esto para el componente activo del navbar

        return context
    
class listarExtranjerosAC(ListView):
    model = Extranjero
    template_name = 'home/puestas/listExtranjenrosAC.html'
    context_object_name = 'extranjerosAC'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        queryset = Extranjero.objects.filter(deLaPuestaAC=puesta)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad'  # Agrega esto para el componente activo del navbar

        return context
    
class EditarExtranjeroINM(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_puestadisposicioninm',
    }
    model = Extranjero
    form_class = extranjeroFormsInm
    template_name = 'home/puestas/editarEx.html'

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        return reverse_lazy('listarExtranjeros', kwargs={'puesta_id': puesta_id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context
    

class DeleteExtranjeroINM(DeleteView):
    model = Extranjero
    template_name = 'home/puestas/eliminarExtranjeroINM.html'
    success_url = reverse_lazy('homePuestaINM')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context
    
    
class EditarExtranjeroAC(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_puestadisposicioninm',
    }
    model = Extranjero
    form_class = extranjeroFormsAC
    template_name = 'home/puestas/createExtranjeroAC.html'
    success_url = reverse_lazy( 'homePuestaAC')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        return context