from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView
from django.views import View
from catalogos.models import Estacion
from .models import LlamadasTelefonicas, Notificacion
from vigilancia.models import Extranjero, PuestaDisposicionINM, PuestaDisposicionAC, PuestaDisposicionVP, Biometrico, NoProceso
from .forms import LlamadasTelefonicasForm, notifificacionLlamada
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import face_recognition
from io import BytesIO
import numpy as np
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Max
from django.contrib import messages
from acuerdos.views import constancia_llamada
from acuerdos.models import Documentos, Repositorio, TiposDoc

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
     ultimo_no_proceso = llamada.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
     ultimo_no_proceso_id = ultimo_no_proceso.nup

     print(f"ID del último NoProceso: {ultimo_no_proceso_id}") 
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
     context['nup'] = ultimo_no_proceso_id

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
    

  

#-------------------------LISTA DE LLLAMADAS PARA LA PUESTA DE INM 
class ListLlamadas(ListView):
    model= LlamadasTelefonicas
    template_name = 'LtIMN/LtIMN.html'

    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        extranjero = Extranjero.objects.get(pk=llamada_id)
        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']
        queryset = LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id, nup__consecutivo=ultimo_nup)
        return queryset
    
    
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
        extranjero = Extranjero.objects.get(pk=llamada_id)


    # Obtener el último nup registrado del extranjero
        ultimo_nup = extranjero.noproceso_set.latest('consecutivo')
        tipo_doc_constancia = TiposDoc.objects.get(descripcion="ConstanciaLlamada")
        repositorio = Repositorio.objects.filter(nup=ultimo_nup, delTipo=tipo_doc_constancia).order_by('-fechaGeneracion').first()
        if repositorio and repositorio.archivo:
            url_oficio_llamada = repositorio.archivo.url
        else:
            url_oficio_llamada = None

        context['url_oficio_llamada'] = url_oficio_llamada

        

        context['extranjero_id'] = llamada_id  # ID del extranjero
        context['puesta_id'] = llamada.deLaPuestaIMN.id  
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
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        initial['nup'] = ultimo_no_proceso_id
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
        context['nombre_extranjero2'] = nombre_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
#-----------------------LISTA DE LLAMADAS PARA LA PUESTA AC ------------------------------------------------------------- 
class ListLlamadasAC(ListView):
    model= LlamadasTelefonicas
    template_name = 'LtAC/LtAC.html'

    
    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        extranjero = Extranjero.objects.get(pk=llamada_id)
        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']
        queryset = LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id, nup__consecutivo=ultimo_nup)        
        return queryset
    
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
           # Obtener el último nup registrado del extranjero
        extranjero = Extranjero.objects.get(pk=llamada_id)
        ultimo_nup = extranjero.noproceso_set.latest('consecutivo')
        tipo_doc_constancia = TiposDoc.objects.get(descripcion="ConstanciaLlamada")
        repositorio = Repositorio.objects.filter(nup=ultimo_nup, delTipo=tipo_doc_constancia).order_by('-fechaGeneracion').first()
        if repositorio and repositorio.archivo:
            url_oficio_llamada = repositorio.archivo.url
        else:
            url_oficio_llamada = None

        context['url_oficio_llamada'] = url_oficio_llamada

        context['extranjero_id'] = llamada_id  # ID del extranjero
        context['puesta_id'] = llamada.deLaPuestaAC.id  
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
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        initial['nup'] = ultimo_no_proceso_id
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
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['nombre_extranjero2'] = nombre_extranjero
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
#---------------------------------------------------------------------------------------------------------------------
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
        extranjero = Extranjero.objects.get(pk=llamada_id)
        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']
        queryset = LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id, nup__consecutivo=ultimo_nup)        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        llamada_id = self.kwargs['llamada_id']
        llamada = Extranjero.objects.get(pk=llamada_id)
        nombre_extranjero = llamada.nombreExtranjero
        estancia_extranjero = llamada.deLaEstacion
        apellido_paterno = llamada.apellidoPaternoExtranjero
        apellido_materno = llamada.apellidoMaternoExtranjero
        no_puesta = llamada.numeroExtranjero
        puesta_id = self.kwargs.get('puesta_id')
        extranjero = Extranjero.objects.get(pk=llamada_id)


        # Obtener el último nup registrado del extranjero
        ultimo_nup = extranjero.noproceso_set.latest('consecutivo')
        tipo_doc_constancia = TiposDoc.objects.get(descripcion="ConstanciaLlamada")
        repositorio = Repositorio.objects.filter(nup=ultimo_nup, delTipo=tipo_doc_constancia).order_by('-fechaGeneracion').first()
        if repositorio and repositorio.archivo:
            url_oficio_llamada = repositorio.archivo.url
        else:
            url_oficio_llamada = None
        context['url_oficio_llamada'] = url_oficio_llamada
        context['extranjero_id'] = llamada_id  # ID del extranjero
        context['puesta_id'] = llamada.deLaPuestaVP.id
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
    template_name = 'modals/crearLlamadaVP.html'
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
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
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
    
class validarNotificacion(CreateView):
    template_name = 'modals/notificacionLlamada.html'
    form_class = notifificacionLlamada  # Aquí estás utilizando el formulario correctamente
    model = Notificacion

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        puesta=PuestaDisposicionINM.objects.get(id=puesta_id)
        return reverse('listarExtranjeros', args=[puesta.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup
        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['delExtranjero'] = extranjero        
        return initial

    def form_valid(self, form):
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = get_object_or_404(Extranjero, id=llamada_id)
        form.instance.noExtranjero = extranjero
        response = super().form_valid(form)
        constancia_llamada(self.request, extranjero_id=self.object.delExtranjero.id)
        return response
    
    
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

class validarNotificacionAC(CreateView):
    template_name = 'modals/notificacion_ac.html'
    form_class = notifificacionLlamada  # Aquí estás utilizando el formulario correctamente
    model = Notificacion

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        puesta=PuestaDisposicionAC.objects.get(id=puesta_id)
        return reverse('listarExtranjeroAC', args=[puesta.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['delExtranjero'] = extranjero        
        return initial

    def form_valid(self, form):
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = get_object_or_404(Extranjero, id=llamada_id)
        form.instance.noExtranjero = extranjero
        response = super().form_valid(form)
        constancia_llamada(self.request, extranjero_id=self.object.delExtranjero.id)

        return response
    
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
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
        return context
    
class validarNotificacionVP(CreateView):
    template_name = 'modals/notificar_vp.html'
    form_class = notifificacionLlamada  # Aquí estás utilizando el formulario correctamente
    model = Notificacion

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        puesta=PuestaDisposicionVP.objects.get(id=puesta_id)
        return reverse('listarExtranjerosVP', args=[puesta.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['delExtranjero'] = extranjero        
        return initial

    def form_valid(self, form):
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = get_object_or_404(Extranjero, id=llamada_id)
        form.instance.noExtranjero = extranjero
        response = super().form_valid(form)
        constancia_llamada(self.request, extranjero_id=self.object.delExtranjero.id)
        return response
    
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
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadVP'
        return context
    
@csrf_exempt
def manejar_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        extranjero_id_str = request.POST.get('llamada_id')
        print(imagen)
        print(extranjero_id_str)

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
    


# llamadas generales 

class ListLlamadasGenerales(ListView):
    model= LlamadasTelefonicas
    template_name = 'generales/listLlamadas.html'

    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        extranjero = Extranjero.objects.get(pk=llamada_id)

        # Obtén el último nup registrado del extranjero
        ultimo_nup = extranjero.noproceso_set.aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtra las llamadas que tengan el último nup registrado del extranjero
        queryset = LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id, nup__consecutivo=ultimo_nup)
        
        return queryset
    
    
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

        ultimo_nup = llamada.noproceso_set.latest('consecutivo')
    # Buscar la instancia Repositorio con ese nup
        try:
            repositorio = Repositorio.objects.get(nup=ultimo_nup)
            url_oficio_llamada = repositorio.archivo.url if repositorio.archivo else None
        except Repositorio.DoesNotExist:
            url_oficio_llamada = None

        context['url_oficio_llamada'] = url_oficio_llamada
        context['extranjero_id'] = llamada_id  # ID del extranjero
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['apellido_paterno'] = apellido_paterno
        context['apellido_materno'] = apellido_materno
        context['no_puesta'] = no_puesta
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        return context
    
class notificacionLlamadaGenerales(TemplateView):
    template_name = 'generales/notificacionLlamadaGen.html'
    def get_queryset(self):
        llamada_id = self.kwargs['llamada_id']
        return LlamadasTelefonicas.objects.filter(noExtranjero=llamada_id)
    
    
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     llamada_id = self.kwargs['llamada_id']
    
    
     # Obtener la instancia del Extranjero correspondiente
     llamada = Extranjero.objects.get(pk=llamada_id)
     ultimo_no_proceso = llamada.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
     ultimo_no_proceso_id = ultimo_no_proceso.nup

     print(f"ID del último NoProceso: {ultimo_no_proceso_id}") 
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
     estatus = llamada.estatus
     context['nup'] = ultimo_no_proceso_id

     context['llamada'] = llamada
     context['nombre_extranjero'] = nombre_extranjero
     context['apellido_paterno'] = apellido_paterno
     context['apellido_materno'] = apellido_materno
     context['extranjero'] = nn
     context['no_puesta'] = no_puesta
     context['estancia_extranjero'] = estancia_extranjero
     context['nombreCompleto'] = nombre_extranjero + " " + apellido_paterno + " " + apellido_materno
     context['responsable'] = estancia_responsableN + " " + estancia_responsableAP + " " + estancia_responsableAM
     context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
     if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
     else:
         context['seccion'] = 'verextranjero'
    
     return context


class validarNotificacionGenerales(CreateView):
    template_name = 'modals/notificacionLlamadaGen.html'
    form_class = notifificacionLlamada  # Aquí estás utilizando el formulario correctamente
    model = Notificacion

    def get_success_url(self):
     
        return reverse('listarExtranjerosEstacion')

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
        initial['delExtranjero'] = extranjero        
        return initial

    def form_valid(self, form):
        # Asigna la relación al campo noExtranjero
        llamada_id = self.kwargs.get('llamada_id')
        extranjero = Extranjero.objects.get(id=llamada_id)
        extranjero = get_object_or_404(Extranjero, id=llamada_id)

        form.instance.noExtranjero = extranjero
        messages.success(self.request, 'Notificación enviada con éxito.')

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
        estatus = llamada.estatus
        if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
        else:
         context['seccion'] = 'verextranjero'
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['estancia_extranjero'] = estancia_extranjero
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        return context
    
class crearLlamadasGenerales(CreateView):
    template_name = 'modals/crearLlamadaGenerales.html'
    form_class = LlamadasTelefonicasForm
    model = LlamadasTelefonicas

    def get_success_url(self):
        return reverse('listLLamadasGen', args=[self.object.noExtranjero.id])

    def get_initial(self):
        initial = super().get_initial()
        # Obtén el ID del extranjero desde la URL
        llamada_id = self.kwargs.get('llamada_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=llamada_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')

# Obtener el ID (nup) del último registro NoProceso
        ultimo_no_proceso_id = ultimo_no_proceso.nup

        # Rellena los campos en initial
        initial['nup'] = ultimo_no_proceso_id
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
        context['llamada'] = llamada
        context['nombre_extranjero'] = nombre_extranjero
        context['estancia_extranjero'] = estancia_extranjero
        context['nombre_extranjero2'] = nombre_extranjero
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        context['seccion'] = 'verextranjero'  # Cambia esto según la página activa
        return context