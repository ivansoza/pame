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
from django.urls import reverse


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context

class createExtranjeroINM(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'puestaINM/crearExtranjeroINM.html' 
    success_url = reverse_lazy('homePuestaINM')

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        return {'deLaPuestaIMN': puesta} 

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
         'perm1': 'vigilancia.change_puestadisposicioninm',
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
class DeleteExtranjeroINM(DeleteView):
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

#------------------------ Fin Puesta por INM-----------------------------

#------------------------  Puesta por AC -----------------------------
class inicioACList(ListView):
    model = PuestaDisposicionAC
    template_name = "puestaAC/homePuestaAC.html" 
    context_object_name = 'puestaAC'
    
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
    
class createExtranjeroAC(CreateView):
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'puestaAC/createExtranjeroAC.html' 
    success_url = reverse_lazy('homePuestaAC')

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        return {'deLaPuestaAC': puesta} 
      
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
         'perm1': 'vigilancia.change_puestadisposicioninm',
    }
    model = Extranjero
    form_class = extranjeroFormsAC
    template_name = 'puestaAC/editarExtranjeroAC.html'

    def get_success_url(self):
        return reverse('listarExtranjeroAC', args=[self.object.deLaPuestaAC.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta'] = self.object.deLaPuestaAC
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
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
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
