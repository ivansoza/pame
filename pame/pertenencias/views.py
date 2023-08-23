from django.shortcuts import render
from django.views.generic import ListView, CreateView
from vigilancia.models import Extranjero, PuestaDisposicionINM
from .forms import InventarioForm, PertenenciaForm
from .models import Pertenencias, Inventario
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
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
        extranjero_id = self.object.noExtranjero.id
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN.id
        
        return reverse('listPertenenciasINM',args=[extranjero_id, puesta])
    
     def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones = extranjero.deLaEstacion.id
        ultimo_registro = Inventario.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.foloInventario.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INV/{estaciones}/{extranjero_id}/{ultimo_numero + 1:06d}'
        initial['foloInventario'] = nuevo_numero
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



#IVAN
class CrearInventarioView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pertenenciasINM/agregarInventarioINM.html'

    def form_valid(self, form):
        extranjero_id = self.kwargs['extranjero_id']
        form.instance.noExtranjero_id = extranjero_id
        return super().form_valid(form)
    def get_initial(self):
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        estaciones_id = extranjero.deLaEstacion.id
        estaciones = extranjero.deLaEstacion.nombre
        ultimo_registro = Inventario.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.foloInventario.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INV/{estaciones_id}/{extranjero_id}/{ultimo_numero + 1:06d}'

        return {'noExtranjero': extranjero_id, 'foloInventario':nuevo_numero, 'unidadMigratoria':estaciones}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)

        context['extranjero_id'] = extranjero_id
        return context

    def get_success_url(self):
        inventario_id = self.object.id  # Obtiene el ID del inventario recién creado
        puesta_id = self.kwargs.get('puesta_id')  # Obtiene el ID de la puesta
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
#IVAN
class ListaPertenenciasView(ListView):
    model = Pertenencias
    template_name = 'pertenenciasINM/listPertenencias.html'

    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Pertenencias.objects.filter(delInventario_id=inventario_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
        return context
    #IVAN
class CrearPertenenciasView(CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'pertenenciasINM/crearPertenenciasINM.html'

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

        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventario_id = self.kwargs['inventario_id']
        inventario = Inventario.objects.get(pk=inventario_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['inventario'] = inventario
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
        inventario_id = self.kwargs.get('extranjero_id')
        inventario = Inventario.objects.get(id=inventario_id)
        extranjero = inventario.noExtranjero 
        elementos = Inventario.objects.all()
        context['elementos'] = elementos
        context['extranjero_principal'] = extranjero_principal
      
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        
        return context
    
class crearPertenenciaINM(CreateView):
    model=Pertenencias
    form_class = PertenenciaForm
    template_name = "pertenenciasINM/agregarPertenenciaINM.html"
    
    def get_success_url(self):
        extranjero_id = self.object.noExtranjero.id
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN.id
        return reverse('listPertenenciasINM',args=[extranjero_id, puesta])
    
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
    
     extranjero_principal_id = self.kwargs.get('extranjero_id')
     

     # Obtener datos del extranjero principal
     extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
    
     # Filtrar las pertenencias del extranjero principal
     pertenencias_del_extranjero = Inventario.objects.filter(noExtranjero_id=extranjero_principal)

     context['extranjero_principal'] = extranjero_principal
     context['pertenencias_del_extranjero'] = pertenencias_del_extranjero
     context['navbar'] = 'seguridad' 
     context['seccion'] = 'seguridadINM'
    
     return context 
   