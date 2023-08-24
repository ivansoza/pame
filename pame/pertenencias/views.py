from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView
from vigilancia.models import Extranjero, PuestaDisposicionINM, PuestaDisposicionAC
from .forms import InventarioForm, PertenenciaForm, ValoresForm
from .models import Pertenencias, Inventario, Valores
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
# Create your views here.

def homePertenencias (request):
    return render (request, "homePertenencias.html")
#------------------------INVENTARIO INM -----------------

#IVAN
class CrearInventarioViewINM(CreateView):
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
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'

        context['extranjero_id'] = extranjero_id
        return context

    def get_success_url(self):
        inventario_id = self.object.id  # Obtiene el ID del inventario recién creado
        puesta_id = self.kwargs.get('puesta_id')  # Obtiene el ID de la puesta
        return reverse('ver_pertenenciasINM', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    

class ListaPertenenciasViewINM(ListView):
    model = Pertenencias
    template_name = 'pertenenciasINM/listPertenenciasINM.html'

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
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context

class CrearPertenenciasViewINM(CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciasINM.html'

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
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context

class DeletePertenenciasINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencias
    template_name = 'modals/eliminarPertenenciaINM.html'

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context

class ListaPertenenciasValorViewINM(ListView):
    model = Valores
    template_name = 'pertenenciasINM/listPertenenciasValorINM.html'

    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Valores.objects.filter(delInventario_id=inventario_id)
    
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
    
class CrearPertenenciasValoresViewINM(CreateView):
    model = Valores
    form_class = ValoresForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciasValorINM.html'

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

class DeletePertenenciasIValorNM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    template_name = 'modals/eliminarPertenenciaValorINM.html'

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        return reverse('ver_pertenencias_valorINM', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    #-------------------------------------
#------------------------INVENTARIO AC -----------------
class CrearInventarioViewAC(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'pertenenciasAC/agregarInventarioAC.html'

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
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'

        context['extranjero_id'] = extranjero_id
        return context

    def get_success_url(self):
        inventario_id = self.object.id  # Obtiene el ID del inventario recién creado
        puesta_id = self.kwargs.get('puesta_id')  # Obtiene el ID de la puesta
        return reverse('ver_pertenenciasAC', kwargs={'inventario_id': inventario_id, 'puesta_id': puesta_id})
    

class ListaPertenenciasViewAC(ListView):
    model = Pertenencias
    template_name = 'pertenenciasAC/listPertenenciasAC.html'

    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Pertenencias.objects.filter(delInventario_id=inventario_id)
    
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

class CrearPertenenciasViewAC(CreateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciasAC.html'

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
    

#-------------------------------FIN --------------------------------