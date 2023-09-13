from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView
from django.views import View
from catalogos.models import Estacion
from .models import LlamadasTelefonicas
from vigilancia.models import Extranjero, PuestaDisposicionINM, PuestaDisposicionAC, PuestaDisposicionVP
from .forms import LlamadasTelefonicasForm
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

def homeLLamadasTelefonicas(request):
    return render(request,"LtIMN/LtIMN.html")


class notificacionLlamadaINM(TemplateView):
    template_name = 'LtIMN/notificacionLlamada.html'
    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    
    
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     llamada_id = self.kwargs['llamada_id']
    
     # Obtener la instancia del Extranjero correspondiente
     llamada = Extranjero.objects.get(pk=llamada_id)
    
     nombre_extranjero = llamada.nombreExtranjero
     estancia_extranjero = llamada.deLaEstacion
     apellido_paterno = llamada.apellidoPaternoExtranjero
     apellido_materno = llamada.apellidoMaternoExtranjero
    
    # Verificar y asignar espacio en blanco si los apellidos son None
     if apellido_paterno is None:
        apellido_paterno = ""
     if apellido_materno is None:
        apellido_materno = ""
    
     estancia_responsableN = llamada.deLaEstacion.responsable.nombre
     estancia_responsableAP = llamada.deLaEstacion.responsable.apellidoPat
     estancia_responsableAM = llamada.deLaEstacion.responsable.apellidoMat
     no_puesta = llamada.numeroExtranjero
     nn = llamada.pk
     puesta_id = self.kwargs.get('puesta_id')

     context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
     context['llamada'] = llamada
     context['nombre_extranjero'] = nombre_extranjero
     context['apellido_paterno'] = apellido_paterno
     context['apellido_materno'] = apellido_materno
     context['extranjero'] = nn
     context['no_puesta'] = no_puesta
     context['estancia_extranjero'] = estancia_extranjero
     context['nombreCompleto'] = nombre_extranjero + " " + apellido_paterno + " " + apellido_materno
     context['responsable'] = estancia_responsableN + " " + estancia_responsableAP + " " + estancia_responsableAM
     context['navbar'] = 'seguridad'
     context['seccion'] = 'seguridadINM'
    
     return context


class llamadasTelefonicas(View):
    template_name = 'LtIMN/LtIMN.html'

    def get(self, request):
        extranjero = Extranjero.objects.first()
        estancia = Extranjero.objects.first()

        nombre_extranjero = extranjero.nombreExtranjero
        estancia_extranjero = estancia.deLaEstacion
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        context = {
            'nombre_extranjero': nombre_extranjero,
            'estancia_extranjero': estancia_extranjero
            
        }
        return render(request, self.template_name, context)
    

  

class ListLlamadas(ListView):
    model= LlamadasTelefonicas
    template_name = 'LtIMN/LtIMN.html'

    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        # Obtener la instancia del Extranjero correspondiente
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        estancia_extranjero = llamada.deLaEstacion
        apellido_paterno = llamada.apellidoPaternoExtranjero
        apellido_materno = llamada.apellidoMaternoExtranjero
        no_puesta = llamada.numeroExtranjero
        puesta_id = self.kwargs.get('puesta_id')

        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['apellido_paterno'] = apellido_paterno
        context['apellido_materno'] = apellido_materno
        context['no_puesta'] = no_puesta
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class crearLlamadas(CreateView):
    template_name = 'modals/crearLlamada.html'
    form_class = LlamadasTelefonicasForm
    model = LlamadasTelefonicas

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        puesta=PuestaDisposicionINM.objects.get(id=puesta_id)
        return reverse('ver_llamadasIMN', args=[self.object.noExtranjero.id, puesta.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        
        # Rellena los campos en initial
        initial['noExtranjero'] = extranjero
        initial['estacionMigratoria'] = extranjero.deLaEstacion
        
        return initial

    def form_valid(self, form):
        # Asigna la relación al campo noExtranjero
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        extranjero = get_object_or_404(Extranjero, id=llamada_id)

        form.instance.noExtranjero = extranjero
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        # Obtener la instancia del Extranjero correspondiente
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        estancia_extranjero = llamada.deLaEstacion
        ape = llamada.apellidoPaternoExtranjero
        ame = llamada.apellidoMaternoExtranjero
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class ListLlamadasAC(ListView):
    model= LlamadasTelefonicas
    template_name = 'LtAC/LtAC.html'

    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        # Obtener la instancia del Extranjero correspondiente
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        estancia_extranjero = llamada.deLaEstacion
        apellido_paterno = llamada.apellidoPaternoExtranjero
        apellido_materno = llamada.apellidoMaternoExtranjero
        folio = llamada.numeroExtranjero
        puesta_id = self.kwargs.get('puesta_id') 
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['apellido_paterno'] = apellido_paterno
        context['apellido_materno'] = apellido_materno
        context['folio'] = folio
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    
class crearLlamadasAC(CreateView):
    template_name = 'LtAC/crearLlamadaAC.html'
    form_class = LlamadasTelefonicasForm
    model = LlamadasTelefonicas

    def get_success_url(self):
        return reverse('ver_llamadasAC', args=[self.object.noExtranjero.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        
        # Rellena los campos en initial
        initial['noExtranjero'] = extranjero
        initial['estacionMigratoria'] = extranjero.deLaEstacion
        
        return initial

    def form_valid(self, form):
        # Asigna la relación al campo noExtranjero
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        extranjero = get_object_or_404(Extranjero, id=llamada_id)

        form.instance.noExtranjero = extranjero
        return super().form_valid(form)

class crearLlamadas_AC(CreateView):
    template_name = 'modals/crearLlamadaAC.html'
    form_class = LlamadasTelefonicasForm
    model = LlamadasTelefonicas

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        puesta=PuestaDisposicionAC.objects.get(id=puesta_id)
        return reverse('ver_llamadasAC', args=[self.object.noExtranjero.id, puesta.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        
        # Rellena los campos en initial
        initial['noExtranjero'] = extranjero
        initial['estacionMigratoria'] = extranjero.deLaEstacion
        
        return initial

    def form_valid(self, form):
        # Asigna la relación al campo noExtranjero
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        extranjero = get_object_or_404(Extranjero, id=llamada_id)

        form.instance.noExtranjero = extranjero
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        # Obtener la instancia del Extranjero correspondiente
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        ape = llamada.apellidoPaternoExtranjero
        ame = llamada.apellidoMaternoExtranjero
        estancia_extranjero = llamada.deLaEstacion
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['nombre_extranjero2'] = nombre_extranjero+" "+ape+" "+ame
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class notificacionLlamadaAC(TemplateView):
    template_name = 'LtAC/notificacionLlamadaAC.html'
    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    
    
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     llamada_id = self.kwargs['llamada_id']
    
     # Obtener la instancia del Extranjero correspondiente
     llamada = Extranjero.objects.get(pk=llamada_id)
    
     nombre_extranjero = llamada.nombreExtranjero
     estancia_extranjero = llamada.deLaEstacion
     apellido_paterno = llamada.apellidoPaternoExtranjero
     apellido_materno = llamada.apellidoMaternoExtranjero
    
    # Verificar y asignar espacio en blanco si los apellidos son None
     if apellido_paterno is None:
        apellido_paterno = ""
     if apellido_materno is None:
        apellido_materno = ""
    
     estancia_responsableN = llamada.deLaEstacion.responsable.nombre
     estancia_responsableAP = llamada.deLaEstacion.responsable.apellidoPat
     estancia_responsableAM = llamada.deLaEstacion.responsable.apellidoMat
     no_puesta = llamada.numeroExtranjero
     nn = llamada.pk
     puesta_id = self.kwargs.get('puesta_id')

     context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)
     context['llamada'] = llamada
     context['nombre_extranjero'] = nombre_extranjero
     context['apellido_paterno'] = apellido_paterno
     context['apellido_materno'] = apellido_materno
     context['extranjero'] = nn
     context['no_puesta'] = no_puesta
     context['estancia_extranjero'] = estancia_extranjero
     context['nombreCompleto'] = nombre_extranjero + " " + apellido_paterno + " " + apellido_materno
     context['responsable'] = estancia_responsableN + " " + estancia_responsableAP + " " + estancia_responsableAM
     context['navbar'] = 'seguridad'
     context['seccion'] = 'seguridadAC'
    
     return context

class notificacionLlamadaVP(TemplateView):
    template_name = 'LtVP/notificacionLlamadaVP.html'
    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     llamada_id = self.kwargs['llamada_id']
    
     # Obtener la instancia del Extranjero correspondiente
     llamada = Extranjero.objects.get(pk=llamada_id)
    
     nombre_extranjero = llamada.nombreExtranjero
     estancia_extranjero = llamada.deLaEstacion
     apellido_paterno = llamada.apellidoPaternoExtranjero
     apellido_materno = llamada.apellidoMaternoExtranjero
    
    # Verificar y asignar espacio en blanco si los apellidos son None
     if apellido_paterno is None:
        apellido_paterno = ""
     if apellido_materno is None:
        apellido_materno = ""
    
     estancia_responsableN = llamada.deLaEstacion.responsable.nombre
     estancia_responsableAP = llamada.deLaEstacion.responsable.apellidoPat
     estancia_responsableAM = llamada.deLaEstacion.responsable.apellidoMat
     no_puesta = llamada.numeroExtranjero
     nn = llamada.pk
     puesta_id = self.kwargs.get('puesta_id')

     context['puesta'] = PuestaDisposicionVP.objects.get(id=puesta_id)
     context['llamada'] = llamada
     context['nombre_extranjero'] = nombre_extranjero
     context['apellido_paterno'] = apellido_paterno
     context['apellido_materno'] = apellido_materno
     context['extranjero'] = nn
     context['no_puesta'] = no_puesta
     context['estancia_extranjero'] = estancia_extranjero
     context['nombreCompleto'] = nombre_extranjero + " " + apellido_paterno + " " + apellido_materno
     context['responsable'] = estancia_responsableN + " " + estancia_responsableAP + " " + estancia_responsableAM
     context['navbar'] = 'seguridad'
     context['seccion'] = 'seguridadVP'
    
     return context
    
class ListLlamadasVP(ListView):
    model= LlamadasTelefonicas
    template_name = 'LtVP/LtVP.html'

    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        # Obtener la instancia del Extranjero correspondiente
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        estancia_extranjero = llamada.deLaEstacion
        apellido_paterno = llamada.apellidoPaternoExtranjero
        apellido_materno = llamada.apellidoMaternoExtranjero
        no_puesta = llamada.numeroExtranjero
        puesta_id = self.kwargs.get('puesta_id')

        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['apellido_paterno'] = apellido_paterno
        context['apellido_materno'] = apellido_materno
        context['no_puesta'] = no_puesta
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    
class crearLlamadasVP(CreateView):
    template_name = 'modals/crearLlamada.html'
    form_class = LlamadasTelefonicasForm
    model = LlamadasTelefonicas

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        puesta=PuestaDisposicionVP.objects.get(id=puesta_id)
        return reverse('ver_llamadas_vp', args=[self.object.noExtranjero.id, puesta.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        
        # Rellena los campos en initial
        initial['noExtranjero'] = extranjero
        initial['estacionMigratoria'] = extranjero.deLaEstacion
        
        return initial

    def form_valid(self, form):
        # Asigna la relación al campo noExtranjero
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        extranjero = get_object_or_404(Extranjero, id=llamada_id)

        form.instance.noExtranjero = extranjero
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        # Obtener la instancia del Extranjero correspondiente
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        estancia_extranjero = llamada.deLaEstacion
        ape = llamada.apellidoPaternoExtranjero
        ame = llamada.apellidoMaternoExtranjero
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['estancia_extranjero'] = estancia_extranjero
        context['nombre_extranjero2'] = nombre_extranjero+" "+ape+" "+ame
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context