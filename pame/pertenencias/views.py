from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from vigilancia.models import Extranjero, PuestaDisposicionINM, PuestaDisposicionAC
from .forms import InventarioForm, PertenenciaForm, ValoresForm, EnseresForm
from .models import Pertenencias, Inventario, Valores, EnseresBasicos
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.urls import reverse_lazy
# Create your views here.

def homePertenencias (request):
    return render (request, "homePertenencias.html")
#------------------------INVENTARIO INM -----------------

#Creacion del inventario 
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
    
#---------------------------------------------------------
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
    
class ListaEnseresViewINM(ListView):
    model = EnseresBasicos
    template_name = 'pertenenciasINM/listEnseresINM.html'
    context_object_name = 'enseresinm'
    def get_queryset(self):
        extranjero_id= self.kwargs['extranjero_id']
        return EnseresBasicos.objects.filter(noExtranjero=extranjero_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id= self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'
        return context

class CrearEnseresINM(CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'pertenenciasINM/crearEnseresINM.html'

    def get_success_url(self):
        extranjero_id = self.object.noExtranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeros', args=[extranjero.deLaPuestaIMN.id])
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero'] = Extranjero.objects.get(id=extranjero_id)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
    def get_initial(self):
        extranjero_id = self.kwargs.get('extranjero_id')
        initial = super().get_initial()
        initial['noExtranjero'] = extranjero_id
        return initial
    

    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        enseres = form.save(commit=False)
        enseres.noExtranjero = extranjero
        enseres.save()
        return super().form_valid(form)
    
class CrearEnseresModaINM(CreateView):
    model= EnseresBasicos
    form_class = EnseresForm
    template_name = 'modals/inm/crearEnseresModaINM.html'
    
    def get_success_url(self):
         enseres_id = self.object.noExtranjero.id
         puesta_id = self.object.noExtranjero.deLaPuestaIMN.id
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
        initial['noExtranjero'] = extranjero_id
        return initial
    

    def form_valid(self, form):
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        enseres = form.save(commit=False)
        enseres.noExtranjero = extranjero
        enseres.save()
        return super().form_valid(form)
    
class EditarEnseresViewINM(UpdateView):
    model = EnseresBasicos
    form_class = EnseresForm  # Usa tu formulario modificado
    template_name = 'modals/editarEnseresINM.html'

    def get_success_url(self):
         enseres_id = self.object.noExtranjero.id
         puesta_id = self.object.noExtranjero.deLaPuestaIMN.id
         return reverse_lazy('listarEnseresINM', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class DeleteEnseresINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = EnseresBasicos
    template_name = 'modals/inm/eliminarEnseres.html'

    def get_success_url(self):
         enseres_id = self.object.noExtranjero.id
         puesta_id = self.object.noExtranjero.deLaPuestaIMN.id
         return reverse_lazy('listarEnseresINM', args=[enseres_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
    
class EditarPertenenciasViewINM(UpdateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/editPertenenciasINM.html'  # Crea este template

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        return reverse_lazy('ver_pertenenciasINM', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadINM'
        return context
    
class EditarPertenenciasViewAC(UpdateView):
    model = Pertenencias
    form_class = PertenenciaForm  # Usa tu formulario modificado
    template_name = 'modals/editPertenenciasAC.html'  # Crea este template

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'
        context['seccion'] = 'seguridadAC'
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
    
class UpdatePertenenciasValorINM(UpdateView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    form_class = ValoresForm 
    template_name = 'modals/editarPertenenciaValorINM.html'

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaIMN.id
        return reverse('ver_pertenencias_valorINM', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class UpdatePertenenciasValorAC(UpdateView):
    permission_required = {
        'perm1': 'vigilancia.delete_valor',
    }
    model = Valores
    form_class = ValoresForm 

    template_name = 'modals/editarPertenenciaValorAC.html'

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        return reverse('ver_pertenencias_valorAC', args=[inventario_id, puesta_id])
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
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
    
class DeletePertenenciasAC(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Pertenencias
    template_name = 'modals/eliminarPertenenciaAc.html'

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        return reverse_lazy('ver_pertenenciasAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context

class ListaPertenenciasValorViewAC(ListView):
    model = Valores
    template_name = 'pertenenciasAC/listPertenenciasValorAC.html'

    def get_queryset(self):
        inventario_id = self.kwargs['inventario_id']
        return Valores.objects.filter(delInventario_id=inventario_id)
    
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
    
class CrearPertenenciasValoresViewAC(CreateView):
    model = Valores
    form_class = ValoresForm  # Usa tu formulario modificado
    template_name = 'modals/crearPertenenciaValorAC.html'

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
    
class DeletePertenenciasValoresAC(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_pertenencia',
    }
    model = Valores
    template_name = 'modals/eliminarPertenenciaValorAC.html'

    def get_success_url(self):
        inventario_id = self.object.delInventario.id
        puesta_id = self.object.delInventario.noExtranjero.deLaPuestaAC.id
        return reverse_lazy('ver_pertenencias_valorAC', args=[inventario_id, puesta_id])


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context

#-------------------------------FIN --------------------------------