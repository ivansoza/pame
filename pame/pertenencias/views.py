from django.shortcuts import render
from django.views.generic import ListView, CreateView
from vigilancia.models import Extranjero, PuestaDisposicionINM
from .forms import InventarioForm
from .models import Pertenencias, Inventario
from django.shortcuts import get_object_or_404
from django.urls import reverse
# Create your views here.

def homePertenencias (request):
    return render (request, "homePertenencias.html")

class pertenenciasINM(ListView):
    model= Extranjero
    template_name = "pertenenciasINM/listPertenenciasINM.html" 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        context['extranjero_principal'] = extranjero_principal
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridaINM'  # Cambia esto según la página activa
        
        return context
    
class crearFolioInventarioINM(CreateView):
     model= Inventario
     form_class = InventarioForm
     template_name = "pertenenciasINM/agregarFolioINM.html"
     def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeros')
    
     def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones = extranjero.deLaEstacion
        initial['noExtranjero'] = extranjero
        initial['unidadMigratoria'] = estaciones
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

class listPertenenciasINM(ListView):
    model = Extranjero
    template_name = "pertenenciasINM/listPertenenciasINM.html" 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        

        # Filtrar las relaciones donde el extranjero principal es delExtranjero y no está relacionado como delAcompanante
        pertenencias_del_extranjero = Pertenencias.objects.filter(delInventario_id=extranjero_principal_id)

        context['extranjero_principal'] = extranjero_principal
        context['pertenencias_del_extranjero'] = pertenencias_del_extranjero
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context