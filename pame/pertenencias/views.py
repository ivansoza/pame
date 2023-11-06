from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from vigilancia.models import Extranjero, PuestaDisposicionINM, PuestaDisposicionAC,PuestaDisposicionVP, NoProceso
from .forms import InventarioForm, PertenenciaForm, ValoresForm, EnseresForm, EditPertenenciaForm,EditarValoresForm,pertenenciaselectronicasForm, valoresefectivoForm,valorejoyasForm, EditarelectronicosForm,documentospertenenciasForm,pertenenciaselectronicasACForm,valorejoyasACForm,valoresefectivoACForm,documentospertenenciasACForm, documentospertenenciasVPForm, valorejoyasVPForm, valoresefectivoVPForm, pertenenciaselectronicasVPForm, EnseresFormUpdate
from .models import Pertenencias, Inventario, Valores, EnseresBasicos, Pertenencia_aparatos, valoresefectivo,valoresjoyas,documentospertenencias
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django import forms
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from vigilancia.models import Biometrico
# Create your views here.
from django import forms
from .helpers import image_to_pdf
import os
import face_recognition
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from django.contrib.auth.decorators import login_required  # Importa el decorador login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from io import BytesIO
from PIL import Image  # Asegúrate de importar Image de PIL o Pillow
import numpy as np 
from datetime import date

#aqui empiezan las pertenencias de VP ------------------------>>>>>>>

# aqui cominezan las pertenencias electronicas ----------------->>>>
class CreatePermissionRequiredMixin(UserPassesTestMixin):
    login_url = '/permisoDenegado/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions_required = kwargs.get('permissions_required', {})

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            # Si el usuario no está autenticado, redirige a la página de inicio de sesión
            return redirect('permisoDenegado')  # Cambia 'acceso_denegado' a la URL adecuada

        for permission, codename in self.permissions_required.items():
            if not user.has_perm(codename):
                raise PermissionDenied(f"No tienes el permiso necesario: {permission}")
        return True

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # Si el usuario está autenticado pero no tiene el permiso, redirige a una página de acceso denegado
            return redirect('permisoDenegado')  # Cambia 'acceso_denegado' a la URL adecuada
        else:
            # Si el usuario no está autenticado, redirige a la página de inicio de sesión
            return redirect(self.login_url)

class CrearPertenenciasElectronicasViewVP(LoginRequiredMixin,CreateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasVPForm
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/pertenenciaselectronicasVP.html'

    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasVP', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context

class DeletePertenenciaselectronicasVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencia_aparatos
    template_name = 'pertenenciasVP/eliminarpertenenciaselectronicasVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión
    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class EditarPertenenciaselectronicasViewVP(LoginRequiredMixin,UpdateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/editarpertenenciaselectronicasVP.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    

# aqu terminan las pertenencias electrinicas ----------------->>>>
# aqui cominezan las pertenencias valores efectivo ----------------->>>>

class CrearvaloresefectivoViewVP(LoginRequiredMixin,CreateView):
    model = valoresefectivo
    form_class = valoresefectivoVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/crearvaloresefectivoVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasVP', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context
    
class eliminarvaloresefectivoVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresefectivo
    template_name = 'pertenenciasVP/eliminarvaloresefectivoVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresefectivoVP(LoginRequiredMixin,UpdateView):
    model = valoresefectivo
    form_class = valoresefectivoVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/editarvaloresefectivoVP.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    

# aqu terminan las pertenencias valores efectivo ----------------->>>>


# aqui cominezan las pertenencias valores joyas ----------------->>>>

class CrearvaloresjoyasViewVP(LoginRequiredMixin,CreateView):
    model = valoresjoyas
    form_class = valorejoyasVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/crearvaloresalhajasVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasVP', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context
    
class eliminarvaloresjoyasVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresjoyas
    template_name = 'pertenenciasVP/eliminarvaloresalhajasVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresjoyasVP(LoginRequiredMixin,UpdateView):
    model = valoresjoyas
    form_class = valorejoyasVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/editarvaloresalhajasVP.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    

# aqu terminan las pertenencias valores joyas ----------------->>>>


# # aqui cominezan las pertenencias documentos ----------------->>>>

class CrearvaloresdocumentosViewVP(LoginRequiredMixin,CreateView):
    model = documentospertenencias
    form_class = documentospertenenciasVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/creardocumentosVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasVP', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context
    
class eliminarvaloresdocumentosVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = documentospertenencias
    template_name = 'pertenenciasVP/eliminardocumentosVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresdocumentosVP(LoginRequiredMixin,UpdateView):
    model = documentospertenencias
    form_class = documentospertenenciasVPForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/editardocumentosVP.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context


# # aqu terminan las pertenencias documentos ----------------->>>>
#aqui terminan las pertenencias de VP ------------------------>>>>>>>





#aqui empiezan las pertenencias de AC ------------------------>>>>>>>

# aqui cominezan las pertenencias electronicas ----------------->>>>
class CrearPertenenciasElectronicasViewAC(LoginRequiredMixin,CreateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/pertenenciaselectronicasAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context

class DeletePertenenciaselectronicasAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencia_aparatos
    template_name = 'pertenenciasAC/eliminarpertenenciaselectronicasAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
class EditarPertenenciaselectronicasViewAC(LoginRequiredMixin,UpdateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/editarpertenenciaselectronicasAC.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    

# aqu terminan las pertenencias electrinicas ----------------->>>>
# aqui cominezan las pertenencias valores efectivo ----------------->>>>

class CrearvaloresefectivoViewAC(LoginRequiredMixin,CreateView):
    model = valoresefectivo
    form_class = valoresefectivoACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/agregarvaloresefectivo.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        return context
    
class eliminarvaloresefectivoAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresefectivo
    template_name = 'pertenenciasAC/eliminarvaloresefectivo.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresefectivoAC(LoginRequiredMixin,UpdateView):
    model = valoresefectivo
    form_class = valoresefectivoACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/editarvaloresefectivo.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    

# aqu terminan las pertenencias valores efectivo ----------------->>>>


# aqui cominezan las pertenencias valores joyas ----------------->>>>

class CrearvaloresjoyasViewAC(LoginRequiredMixin,CreateView):
    model = valoresjoyas
    form_class = valorejoyasACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/crearvaloresalhajas.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        return context
    
class eliminarvaloresjoyasAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresjoyas
    template_name = 'pertenenciasAC/eliminarvaloresalhajas.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresjoyasAC(LoginRequiredMixin,UpdateView):
    model = valoresjoyas
    form_class = valorejoyasACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/editarvaloresalhajas.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    

# aqu terminan las pertenencias valores joyas ----------------->>>>


# # aqui cominezan las pertenencias documentos ----------------->>>>

class CrearvaloresdocumentosViewAC(LoginRequiredMixin,CreateView):
    model = documentospertenencias
    form_class = documentospertenenciasACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/creardocumentosAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        return context
    
class eliminarvaloresdocumentosAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = documentospertenencias
    template_name = 'pertenenciasAC/eliminardocumentoAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresdocumentosAC(LoginRequiredMixin,UpdateView):
    model = documentospertenencias
    form_class = documentospertenenciasACForm  # Usa tu formulario modificado
    template_name = 'pertenenciasAC/editardocumentosAC.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context


# # aqu terminan las pertenencias documentos ----------------->>>>
#aqui terminan las pertenencias de AC ------------------------>>>>>>>






# aqui cominezan las pertenencias valores efectivo ----------------->>>>

class CrearvaloresefectivoViewINM(LoginRequiredMixin,CreateView):
    model = valoresefectivo
    form_class = valoresefectivoForm  # Usa tu formulario modificado
    template_name = 'modals/crearvaloresefectivoINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class eliminarvaloresefectivoINM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresefectivo
    template_name = 'modals/eliminarvaloresefectivoINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresefectivoINM(LoginRequiredMixin,UpdateView):
    model = valoresefectivo
    form_class = valoresefectivoForm  # Usa tu formulario modificado
    template_name = 'modals/editarvaloresefectivoINM.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    

# aqu terminan las pertenencias valores efectivo ----------------->>>>


# aqui cominezan las pertenencias valores joyas ----------------->>>>

class CrearvaloresjoyasViewINM(LoginRequiredMixin,CreateView):
    model = valoresjoyas
    form_class = valorejoyasForm  # Usa tu formulario modificado
    template_name = 'modals/crearvaloresjoyasINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class eliminarvaloresjoyasINM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresjoyas
    template_name = 'modals/eliminarvaloresjoyasINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresjoyasINM(LoginRequiredMixin,UpdateView):
    model = valoresjoyas
    form_class = valorejoyasForm  # Usa tu formulario modificado
    template_name = 'modals/editarvaloresjoyasINM.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    

# aqu terminan las pertenencias valores joyas ----------------->>>>


# # aqui cominezan las pertenencias documentos ----------------->>>>

class CrearvaloresdocumentosViewINM(LoginRequiredMixin,CreateView):
    model = documentospertenencias
    form_class = documentospertenenciasForm  # Usa tu formulario modificado
    template_name = 'modals/creardocumentosINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class eliminarvaloresdocumentosINM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = documentospertenencias
    template_name = 'modals/eliminardocumentosINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresdocumentosINM(LoginRequiredMixin,UpdateView):
    model = documentospertenencias
    form_class = documentospertenenciasForm  # Usa tu formulario modificado
    template_name = 'modals/editardocumentosINM.html'  # Crea este template

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context


# # aqu terminan las pertenencias documentos ----------------->>>>


class PermissionRequiredMixin(LoginRequiredMixin,UserPassesTestMixin):
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


def homePertenencias (request):
    return render (request, "homePertenencias.html")
#------------------------INVENTARIO INM -----------------



#Creacion del inventario 
class CrearInventarioViewINM(LoginRequiredMixin,CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'pertenencias.add_inventario',
    }
    model = Inventario
    form_class = InventarioForm
    template_name = 'pertenenciasINM/agregarInventarioINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones = extranjero.deLaEstacion.nombre
        form.instance.noExtranjero_id = extranjero_id
        form.instance.unidadMigratoria = estaciones
        return super().form_valid(form)


    def get_initial(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        estaciones_id = extranjero.deLaEstacion.id
        estaciones = extranjero.deLaEstacion.nombre
        ultimo_registro = Inventario.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.foloInventario.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INV/{estaciones_id}/{extranjero_id}/{ultimo_numero + 1:06d}'

        return {'noExtranjero': extranjero_id, 'foloInventario':nuevo_numero, 'unidadMigratoria':estaciones,'nup':ultimo_no_proceso_id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        puesta_id = self.kwargs.get('puesta_id')
        extranjero_id1 = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id1)
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero'] = extranjero
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'

        context['extranjero_id'] = extranjero_id
        return context

    def get_success_url(self):
        inventario_id = self.object.id  # Obtiene el ID del inventario recién creado
        puesta_id = self.kwargs.get('puesta_id')  # Obtiene el ID de la puesta
        messages.success(self.request, 'Inventario creado con éxito.')
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
#---------------------------------------------------------
class ListaPertenenciasViewINM(LoginRequiredMixin,ListView):
    model = Pertenencias
    template_name = 'pertenenciasINM/listPertenenciasINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        queryset =Pertenencias.objects.filter(delInventario_id=inventario_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')

        extranjero_id = inventario.noExtranjero.id

        # Obtén el último NUP del extranjero
        ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))
        ultimo_nup = ultimo_nup['consecutivo__max']

        # Filtra los datos según el último NUP
        aparatos = Pertenencia_aparatos.objects.filter(delInventario_id=inventario_id)
        efectivos = valoresefectivo.objects.filter(delInventario_id=inventario_id)
        joyas = valoresjoyas.objects.filter(delInventario_id=inventario_id)
        documentos = documentospertenencias.objects.filter(delInventario_id=inventario_id)

        
        context['document']=documentos
        context['efectivo']=efectivos
        context['joyas']=joyas
        context['aparato']=aparatos
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['puesta_id']=puesta_id
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class ListaEnseresViewINM(LoginRequiredMixin,ListView):
    model = EnseresBasicos
    template_name = 'pertenenciasINM/listEnseresINM.html'
    context_object_name = 'enseresinm'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_queryset(self):
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)

        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtra las llamadas que tengan el último nup registrado del extranjero
        queryset = EnseresBasicos.objects.filter(noExtranjero=extranjero_id, nup__consecutivo=ultimo_nup)
        
        today_enseres = queryset.filter(fechaEntrega=date.today())
        if today_enseres.exists():
            self.today_registered = True
        else:
            self.today_registered = False
        return queryset    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['extranjero_id'] = extranjero_id  # Agregar el extranjero al contexto
        context['puesta_id'] = puesta_id  # Agregar el extranjero al contexto
        context['today_registered'] = self.today_registered  # Agrega al contexto si se registró hoy

        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context

class CrearEnseresINM(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'pertenenciasINM/crearEnseresINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        extranjero_id = self.object.noExtranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Enseres creado con éxito.')
        return reverse('listarExtranjeros', args=[extranjero.deLaPuestaIMN.id])
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        context['extranjero_id'] = extranjero_id
        context['puesta_id'] = puesta_id

        return context
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        estacion = extranjero.deLaEstacion
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)

    
class CrearEnseresModaINM(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'modals/inm/crearEnseresModaINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Enseres creado con éxito.')

        return reverse_lazy('listarEnseresINM', args=[enseres_id, puesta_id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        return context
    
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial

    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)

class EditarEnseresViewINM(LoginRequiredMixin,UpdateView):
    model = EnseresBasicos
    form_class = EnseresFormUpdate  # Usa tu formulario modificado
    template_name = 'modals/inm/editarEnseresINM.html'
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

    
class DeleteEnseresINM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = EnseresBasicos
    template_name = 'modals/inm/eliminarEnseres.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Enseres eliminados con éxito.')
        return reverse_lazy('listarEnseresINM', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class CrearPertenenciasViewINM(LoginRequiredMixin,CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciasINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
class CrearPertenenciasElectronicasViewINM(LoginRequiredMixin,CreateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasForm  # Usa tu formulario modificado
    template_name = 'modals/pertenenciaselectronicasINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context

class DeletePertenenciasINM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencias
    template_name = 'modals/eliminarPertenenciaINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class EditarPertenenciasViewINM(LoginRequiredMixin,UpdateView):
    model = Pertenencias
    form_class = EditPertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/editPertenenciasINM.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
    
# aqui cominezan las pertenencias electronicas ----------------->>>>
class DeletePertenenciaselectronicasINM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencia_aparatos
    template_name = 'modals/eliminarpertenenciaselectronicasINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class EditarPertenenciaselectronicasViewINM(LoginRequiredMixin,UpdateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasForm  # Usa tu formulario modificado
    template_name = 'modals/editarpertenenciaselectronicasINM.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    

# aqu terminan las pertenencias electrinicas ----------------->>>>
class EditarPertenenciasViewAC(LoginRequiredMixin,UpdateView):
    model = Pertenencias
    form_class = EditPertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/editPertenenciasAC.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context

class ListaPertenenciasValorViewINM(LoginRequiredMixin,ListView):
    model = Valores
    template_name = 'pertenenciasINM/listPertenenciasValorINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Valores.objects.filter(delInventario_id=inventario_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class CrearPertenenciasValoresViewINM(LoginRequiredMixin,CreateView):
    model = Valores
    form_class = ValoresForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciasValorINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Valores agregados con éxito.')
        return reverse('ver_pertenencias_valorINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class UpdatePertenenciasValorINM(LoginRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    form_class = EditarValoresForm 
    template_name = 'modals/editarPertenenciaValorINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')
        return reverse('ver_pertenencias_valorINM', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class UpdatePertenenciasValorAC(LoginRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    form_class = EditarValoresForm 

    template_name = 'modals/editarPertenenciaValorAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse('ver_pertenencias_valorAC', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context

class DeletePertenenciasIValorNM(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    template_name = 'modals/eliminarPertenenciaValorINM.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        messages.success(self.request, 'Valores eliminados con éxito.')

        return reverse('ver_pertenencias_valorINM', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    #-------------------------------------
#------------------------INVENTARIO AC -----------------
class CrearInventarioViewAC(LoginRequiredMixin,CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pertenenciasAC/agregarInventarioAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        # Lógica relacionada con el extranjero y estaciones
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones = extranjero.deLaEstacion.nombre
        form.instance.noExtranjero_id = extranjero_id
        form.instance.unidadMigratoria = estaciones

        # Guarda el formulario pero no comitea a la base de datos aún
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
        handle_file('validacion')

        # Finalmente, guarda la instancia
        instance.save()

        return super().form_valid(form)  # Cambié "createPuestaAC" por "super()"


    def get_initial(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nExtranjero = extranjero.nombreExtranjero
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        estaciones_id = extranjero.deLaEstacion.id
        estaciones = extranjero.deLaEstacion.nombre
        ultimo_registro = Inventario.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.foloInventario.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INV/{estaciones_id}/{extranjero_id}/{ultimo_numero + 1:06d}'
        return {'noExtranjero': extranjero_id, 'foloInventario':nuevo_numero, 'unidadMigratoria':estaciones,'nup':ultimo_no_proceso_id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        extranjero_id1 = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id1)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        context['extranjero'] = extranjero
        context['extranjero_id'] = extranjero_id
        return context

    def get_success_url(self):
        inventario_id = self.object.id  # Obtiene el ID del inventario recién creado
        puesta_id = self.kwargs.get('puesta_id')  # Obtiene el ID de la puesta
        messages.success(self.request, 'Inventario creado con éxito.')
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    

class ListaPertenenciasViewAC(LoginRequiredMixin,ListView):
    model = Pertenencias
    template_name = 'pertenenciasAC/listPertenenciasAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Pertenencias.objects.filter(delInventario_id=inventario_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        extranjero_id = inventario.noExtranjero.id

        # Obtén el último NUP del extranjero
        ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))
        ultimo_nup = ultimo_nup['consecutivo__max']

        # Filtra los datos según el último NUP
        aparatos = Pertenencia_aparatos.objects.filter(delInventario_id=inventario_id)
        efectivos = valoresefectivo.objects.filter(delInventario_id=inventario_id)
        joyas = valoresjoyas.objects.filter(delInventario_id=inventario_id)
        documentos = documentospertenencias.objects.filter(delInventario_id=inventario_id)

        
        context['doc']=documentos
        context['alhajas']=joyas
        context['dinero']=efectivos
        context['electronicos']=aparatos
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        context['inventario'] = inventario
        return context

class CrearPertenenciasViewAC(LoginRequiredMixin,CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciasAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial


    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        return context
    
class DeletePertenenciasAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencias
    template_name = 'modals/eliminarPertenenciaAc.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')
        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context

class ListaPertenenciasValorViewAC(LoginRequiredMixin,ListView):
    model = Valores
    template_name = 'pertenenciasAC/listPertenenciasValorAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Valores.objects.filter(delInventario_id=inventario_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        
        electronicos = Pertenencia_aparatos.objects.filter(delInventario=inventario.noExtranjero.id)
        dinero = valoresefectivo.objects.filter(delInventario=inventario.noExtranjero.id)
        alhajas = valoresjoyas.objects.filter(delInventario=inventario.noExtranjero.id)
        doc = documentospertenencias.objects.filter(delInventario=inventario.noExtranjero.id)

        
        context['doc']=doc
        context['alhajas']=alhajas
        context['dinero']=dinero
        context['electronicos']=electronicos
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        context['inventario'] = inventario
        
        return context
    
class CrearPertenenciasValoresViewAC(LoginRequiredMixin,CreateView):
    model = Valores
    form_class = ValoresForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciaValorAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Valores agregados con éxito.')
        return reverse('ver_pertenencias_valorAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        return context
    
class DeletePertenenciasValoresAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Valores
    template_name = 'modals/eliminarPertenenciaValorAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Valores eliminadas con éxito.')
        return reverse_lazy('ver_pertenencias_valorAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context


class ListaEnseresViewAC(LoginRequiredMixin,ListView):
    model = EnseresBasicos
    template_name = 'pertenenciasAC/listEnseresAC.html'
    context_object_name = 'enseresac'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_queryset(self):
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)

        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtra las llamadas que tengan el último nup registrado del extranjero
        queryset = EnseresBasicos.objects.filter(noExtranjero=extranjero_id, nup__consecutivo=ultimo_nup)
        today_enseres = queryset.filter(fechaEntrega=date.today())
        if today_enseres.exists():
            self.today_registered = True
        else:
            self.today_registered = False
        return queryset   
        return queryset    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        context['today_registered'] = self.today_registered  # Agrega al contexto si se registró hoy

        context['extranjero_id'] = extranjero_id  # Agregar el extranjero al contexto
        context['puesta_id'] = puesta_id  # Agregar el extranjero al contexto
        return context
    
class CrearEnseresAC(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'pertenenciasAC/crearEnseresAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        extranjero_id = self.object.noExtranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Enseres creados con éxito.')
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        context['extranjero_id'] = extranjero_id
        context['puesta_id'] = puesta_id
        return context
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        estacion = extranjero.deLaEstacion
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial

    
class EditarEnseresViewAC(LoginRequiredMixin,UpdateView):
    model = EnseresBasicos
    form_class = EnseresFormUpdate  # Usa tu formulario modificado
    template_name = 'modals/ac/editarEnseresAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Enseres editados con éxito.')
        return reverse_lazy('listarEnseresAC', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context


    
class DeleteEnseresAC(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = EnseresBasicos
    template_name = 'modals/ac/eliminarEnseresAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Enseres eliminados con éxito.')
        return reverse_lazy('listarEnseresAC', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    

class CrearEnseresModaAC(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'modals/ac/crearEnseresModaAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaAC.id
        messages.success(self.request, 'Enseres creados con éxito.')
        return reverse_lazy('listarEnseresAC', args=[enseres_id, puesta_id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        return context
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial
#-------------------------------FIN --------------------------------


#--------------------------------VP--------------------------------


    
class CrearInventarioViewVP(LoginRequiredMixin,CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'pertenencias.add_inventario',
    }
    model = Inventario
    form_class = InventarioForm
    template_name = 'pertenenciasVP/agregarInventarioVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones = extranjero.deLaEstacion.nombre
        form.instance.noExtranjero_id = extranjero_id
        form.instance.unidadMigratoria = estaciones
        return super().form_valid(form)
    def get_initial(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        estaciones_id = extranjero.deLaEstacion.id
        estaciones = extranjero.deLaEstacion.nombre
        ultimo_registro = Inventario.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.foloInventario.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INV/{estaciones_id}/{extranjero_id}/{ultimo_numero + 1:06d}'
        return {'noExtranjero': extranjero_id, 'foloInventario':nuevo_numero, 'unidadMigratoria':estaciones,'nup':ultimo_no_proceso_id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        puesta_id = self.kwargs.get('puesta_id')
        extranjero_id1 = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id1)
        
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['extranjero'] = extranjero
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'

        context['extranjero_id'] = extranjero_id
        return context

    def get_success_url(self):
        inventario_id = self.object.id  # Obtiene el ID del inventario recién creado
        puesta_id = self.kwargs.get('puesta_id')  # Obtiene el ID de la puesta
        messages.success(self.request, 'Inventario creado con éxito.')

        return reverse('ver_pertenenciasVP', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
class ListaPertenenciasViewVP(LoginRequiredMixin,ListView):
    model = Pertenencias
    template_name = 'pertenenciasVP/listPertenenciasVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Pertenencias.objects.filter(delInventario_id=inventario_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        extranjero_id = inventario.noExtranjero.id
        aparatos = Pertenencia_aparatos.objects.filter(delInventario_id=inventario_id)
        dinero = valoresefectivo.objects.filter(delInventario_id=inventario_id)
        alhajas = valoresjoyas.objects.filter(delInventario_id=inventario_id)
        doc = documentospertenencias.objects.filter(delInventario_id=inventario_id)

        context['electro']=aparatos
        context['doc']=doc
        context['alhajas']=alhajas
        context['dinero']=dinero
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        context['inventario'] = inventario
        return context
    
class CrearPertenenciasViewVP(LoginRequiredMixin,CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/crearpertenenciasVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('ver_pertenenciasVP', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context
    
class DeletePertenenciasVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencias
    template_name = 'pertenenciasVP/eliminarpertenenciasVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias eliminadas con éxito.')
        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    

class EditarPertenenciasViewVP(LoginRequiredMixin,UpdateView):
    model = Pertenencias
    form_class = EditPertenenciaForm  # Usa tu formulario modificado
    template_name = 'pertenenciasVP/editarpertenenciasVP.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')

        return reverse_lazy('ver_pertenenciasVP', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context

class ListaPertenenciasValorViewVP(LoginRequiredMixin,ListView):
    model = Valores
    template_name = 'pertenenciasVP/listPertenenciasValorVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Valores.objects.filter(delInventario_id=inventario_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        return context
    
class CrearPertenenciasValoresViewVP(LoginRequiredMixin,CreateView):
    model = Valores
    form_class = ValoresForm  # Usa tu formulario modificado
    template_name = 'modals/vp/crearPertenenciasValorVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Valores agregados con éxito.')
        return reverse('ver_pertenencias_valor_vp', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context
    
class DeletePertenenciasValorVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    template_name = 'modals/vp/eliminarPertenenciaValorVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Valores eliminados con éxito.')

        return reverse('ver_pertenencias_valor_vp', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class UpdatePertenenciasValorVP(LoginRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    form_class = EditarValoresForm 
    template_name = 'modals/vp/editarPertenenciasValorVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')
        return reverse('ver_pertenencias_valor_vp', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa

        return context
    
class ListaEnseresViewUP(LoginRequiredMixin,ListView):
    model = EnseresBasicos
    template_name = 'pertenenciasVP/listEnseresVP.html'
    context_object_name = 'enseresvp'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_queryset(self):
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)

        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtra las llamadas que tengan el último nup registrado del extranjero
        queryset = EnseresBasicos.objects.filter(noExtranjero=extranjero_id, nup__consecutivo=ultimo_nup)
        today_enseres = queryset.filter(fechaEntrega=date.today())
        if today_enseres.exists():
            self.today_registered = True
        else:
            self.today_registered = False
        return queryset  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        context['today_registered'] = self.today_registered  # Agrega al contexto si se registró hoy

        context['extranjero_id'] = extranjero_id  # Agregar el extranjero al contexto
        context['puesta_id'] = puesta_id  # Agregar el extranjero al contexto
        return context
    
class CrearEnseresVP(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'pertenenciasVP/crearEnseresVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        extranjero_id = self.object.noExtranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Enseres creado con éxito.')
        return reverse('listarExtranjerosVP', args=[extranjero.deLaPuestaVP.id])
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        context['extranjero_id'] = extranjero_id
        context['puesta_id'] = puesta_id
        return context
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        estacion = extranjero.deLaEstacion
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial


class CrearEnseresModalVP(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'modals/vp/crearEnseresModalVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Enseres creado con éxito.')

        return reverse_lazy('listar_enseres_vp', args=[enseres_id, puesta_id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        return context
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        estacion = extranjero.deLaEstacion
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial
    
class DeleteEnseresVP(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = EnseresBasicos
    template_name = 'modals/vp/eliminarEnseresVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Enseres eliminados con éxito.')
        return reverse_lazy('listar_enseres_vp', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    
class EditarEnseresViewVP(LoginRequiredMixin,UpdateView):
    model = EnseresBasicos
    form_class = EnseresFormUpdate  # Usa tu formulario modificado
    template_name = 'modals/vp/editarEnseresVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        puesta_id = self.object.noExtranjero.deLaPuestaVP.id
        messages.success(self.request, 'Enseres editados con éxito.')

        return reverse_lazy('listar_enseres_vp', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    

@csrf_exempt
def manejar_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        extranjero_id_str = request.POST.get('extranjero_id')

        if extranjero_id_str is None or not extranjero_id_str.isdigit():
            return JsonResponse({'error': 'Invalid extranjero_id'}, status=400)

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
    
# ESTA SERA LA SECCION PARA TODOS LOS EXTRANJEROS 
# INICIA ENSERES

class ListaEnseresView(LoginRequiredMixin,ListView):
    model = EnseresBasicos
    template_name = 'pertenencias/listEnseres.html'
    context_object_name = 'enseres'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_queryset(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)

        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtra las llamadas que tengan el último nup registrado del extranjero
        queryset = EnseresBasicos.objects.filter(noExtranjero=extranjero_id, nup__consecutivo=ultimo_nup)

        # Agreguemos una verificación para ver si hay registros para hoy
        today_enseres = queryset.filter(fechaEntrega=date.today())
        if today_enseres.exists():
            self.today_registered = True
        else:
            self.today_registered = False

        return queryset  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        context['today_registered'] = self.today_registered  # Agrega al contexto si se registró hoy
        estatus = extranjero.estatus
        if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
        else:
         context['seccion'] = 'verextranjero'
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['extranjero_id'] = extranjero_id  # Agregar el extranjero al contexto
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        return context

class CrearEnseres(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'pertenencias/agregarEnseres.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Enseres creado con éxito.')
        estatus = extranjero.estatus
        if estatus == "Trasladado":
            return reverse('listarExtranjerosEstacion')
        else:
          return reverse('listTrasladados')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        estatus = extranjero.estatus
        if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
        else:
         context['seccion'] = 'verextranjero'
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['extranjero_id'] = extranjero_id

        return context
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        estacion = extranjero.deLaEstacion
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial
    
    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)

    
class CrearEnseresModa(LoginRequiredMixin,CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'modals/general/crearEnseresModal.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        messages.success(self.request, 'Enseres creado con éxito.')

        return reverse_lazy('listarEnseres', args=[enseres_id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        return context
    
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['unidadMigratoria'] = estacion
        initial['noExtranjero'] = extranjero_id
        return initial

    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estacion = extranjero.deLaEstacion
        form.instance.unidadMigratoria= estacion
        form.instance.noExtranjero= extranjero
        return super().form_valid(form)

class EditarEnseresView(LoginRequiredMixin,UpdateView):
    model = EnseresBasicos
    form_class = EnseresFormUpdate  # Usa tu formulario modificado
    template_name = 'modals/general/editarEnseres.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        messages.success(self.request, 'Enseres editados con éxito.')

        return reverse_lazy('listarEnseres', args=[enseres_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        return context

class DeleteEnseres(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = EnseresBasicos
    template_name = 'modals/general/eliminarEnseres.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.noExtranjero.id
        messages.success(self.request, 'Enseres eliminados con éxito.')
        return reverse_lazy('listarEnseres', args=[enseres_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        return context

#-------------------VistasGenerales-----------------------------------
class ListaPertenenciasViewGeneral(LoginRequiredMixin,ListView):
    model = Pertenencias
    template_name = 'pertenencias/listPertenencias.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        queryset =Pertenencias.objects.filter(delInventario_id=inventario_id)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')

        extranjero_id = inventario.noExtranjero.id

        # Obtén el último NUP del extranjero
        ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))
        ultimo_nup = ultimo_nup['consecutivo__max']

        # Filtra los datos según el último NUP
        aparatos = Pertenencia_aparatos.objects.filter(delInventario_id=inventario_id)
        efectivos = valoresefectivo.objects.filter(delInventario_id=inventario_id)
        joyas = valoresjoyas.objects.filter(delInventario_id=inventario_id)
        documentos = documentospertenencias.objects.filter(delInventario_id=inventario_id)
        estatus = inventario.noExtranjero.estatus # Asume que el campo es 'estatus', ajusta si es diferente
        if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
        else:
         context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        
        context['document']=documentos
        context['efectivo']=efectivos
        context['joyas']=joyas
        context['aparato']=aparatos
        context['extranjero_id'] = inventario.noExtranjero.id  # Añadiendo el ID del Extranjero al contexto
        context['puesta_id']=puesta_id
        context['inventario'] = inventario
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        return context

class CrearInventarioViewGeneral(LoginRequiredMixin,CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'pertenencias.add_inventario',
    }
    model = Inventario
    form_class = InventarioForm
    template_name = 'pertenencias/inventarioGeneral.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        messages.success(self.request, 'Inventario creado con éxito.')
        estatus = extranjero.estatus
        if estatus == "Trasladado":
            return reverse('listarExtranjerosEstacion')
        else:
          return reverse('listTrasladados')


    def form_valid(self, form):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones = extranjero.deLaEstacion.nombre
        form.instance.noExtranjero_id = extranjero_id
        form.instance.unidadMigratoria = estaciones
        return super().form_valid(form)


    def get_initial(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        estaciones_id = extranjero.deLaEstacion.id
        estaciones = extranjero.deLaEstacion.nombre
        ultimo_registro = Inventario.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.foloInventario.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INV/{estaciones_id}/{extranjero_id}/{ultimo_numero + 1:06d}'

        return {'noExtranjero': extranjero_id, 'foloInventario':nuevo_numero, 'unidadMigratoria':estaciones,'nup':ultimo_no_proceso_id}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        puesta_id = self.kwargs.get('puesta_id')
        extranjero_id1 = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id1)
        estatus = extranjero.estatus
        if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
        else:
         context['seccion'] = 'verextranjero'

        context['extranjero'] = extranjero
        context['navbar'] = 'extranjeros' 

        context['extranjero_id'] = extranjero_id
        return context
    
class CrearPertenenciasViewGeneral(LoginRequiredMixin,CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/agregarPertenenciasPersonales.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.kwargs['inventario_id']
        puesta_id = self.kwargs.get('puesta_id')
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class EditarPertenenciasViewGenerales(LoginRequiredMixin,UpdateView):
    model = Pertenencias
    form_class = EditPertenenciaForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/editarPertenenciasPersonal.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        enseres_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencias editadas con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': enseres_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class DeletePertenenciasGeneral(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencias
    template_name = 'pertenencias/modals/eliminarPertenenciasPersonales.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class CrearPertenenciasElectronicasVieGeneral(LoginRequiredMixin,CreateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasACForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/agregarElectro.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    
    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencias creadas con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
    
class EditarPertenenciaselectronicasViewGeneral(LoginRequiredMixin,UpdateView):
    model = Pertenencia_aparatos
    form_class = pertenenciaselectronicasACForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/editarElectro.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencias editada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    
class DeletePertenenciaselectronicasGenerales(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencia_aparatos
    template_name = 'pertenencias/modals/eliminarElectro.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia eliminada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
class CrearvaloresefectivoViewGeneral(LoginRequiredMixin,CreateView):
    model = valoresefectivo
    form_class = valoresefectivoACForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/crearEfectivo.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia creada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'
        return context
    
class eliminarvaloresefectivoGeneral(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresefectivo
    template_name = 'pertenencias/modals/eliminarEfectivo.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia eliminada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresefectivoGeneral(LoginRequiredMixin,UpdateView):
    model = valoresefectivo
    form_class = valoresefectivoForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/editarEfectivo.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia Editada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class CrearvaloresjoyasViewGeneral(LoginRequiredMixin,CreateView):
    model = valoresjoyas
    form_class = valorejoyasVPForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/agregarJoyas.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia creada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadVP'
        return context
    
class eliminarvaloresjoyasGeneral(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = valoresjoyas
    template_name = 'pertenencias/modals/eliminarJoyas.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia eliminada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresjoyasGeneral(LoginRequiredMixin,UpdateView):
    model = valoresjoyas
    form_class = valorejoyasVPForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/editarJoyas.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia Editada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    
class CrearvaloresdocumentosViewGeneral(LoginRequiredMixin,CreateView):
    model = documentospertenencias
    form_class = documentospertenenciasForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/agregarDocumento.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def form_valid(self, form):
        inventario_id = self.kwargs['inventario_id']
        form.instance.delInventario_id = inventario_id
        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        inventario_id = self.kwargs['inventario_id']
        initial['delInventario'] = inventario_id
        return initial
    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia creada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['inventario'] = inventario
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context
    
class eliminarvaloresdocumentosGeneral(LoginRequiredMixin,DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = documentospertenencias
    template_name = 'pertenencias/modals/eliminarDocumento.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia eliminada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class editarvaloresdocumentosGeneral(LoginRequiredMixin,UpdateView):
    model = documentospertenencias
    form_class = documentospertenenciasForm  # Usa tu formulario modificado
    template_name = 'pertenencias/modals/editarDocumento.html'  # Crea este template
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión


    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        messages.success(self.request, 'Pertenencia Editada con éxito.')
        return reverse('listPertenenciasGeneral', kwargs={'inventario_id': inventario_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context