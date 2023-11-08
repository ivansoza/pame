from django.shortcuts import render
from .forms import ResponsableForm, AutoridadesForms, AutoridadesActuantesForms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView
# Create your views here.
from .models import Responsable, Autoridades, AutoridadesActuantes, Estacion
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.shortcuts import redirect

def home(request):
    return render(request,"index.html")

@login_required
def responsableCrear(request):
    form= ResponsableForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,"Producto Agregado Exitosamente")
        return HttpResponseRedirect("/")
    context ={
        "form":form
    }
    return render(request,"addResponsable.html",context)

class listAutoridades(ListView):
    template_name = 'Autoridades/listaAutoridades.html'
    model = Autoridades
    context_object_name ='autoridades'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'autoridades'        
        return context


class crearAutoridad(CreateView):
    template_name = 'Autoridades/registroAutoridades.html'
    model = Autoridades
    form_class = AutoridadesForms
    def get_success_url(self):
        messages.success(self.request, 'Extranjero Creado.')
        return reverse('listaAutoridad')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'autoridades'        
        return context

class agregarAutoridadActuante(ListView):
    template_name = 'Autoridades/autoridadActuante.html'
    model = Autoridades
    context_object_name ='autoridades'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'actuantes'    
        context['autoridades'] = Autoridades.objects.filter(estado__in=['Libre', 'Vigente'])
        user = self.request.user
        user_estacion = user.estancia
        # Filtrar los objetos de AutoridadesActuantes por la estación asociada al usuario
        context['actuantes'] = AutoridadesActuantes.objects.filter(estacion=user_estacion)  
        return context
    
class crearAutoridadActuante(CreateView):
    template_name = 'Autoridades/modalAsignarAutoridad.html'
    model = AutoridadesActuantes
    form_class = AutoridadesActuantesForms
    def get_success_url(self):
        messages.success(self.request, 'Autoridad Actuante Asignada.')
        return reverse('agregaraAutoridadActuante')
    def form_valid(self, form):
        # Llama al método form_valid predeterminado para guardar el nuevo registro
        response = super().form_valid(form)

        # Cambia el estado de la autoridad relacionada a 'Asignado'
        autoridad = get_object_or_404(Autoridades, pk=self.kwargs['autoridad_id'])
        autoridad.estado = 'Asignado'
        autoridad.save()

        messages.success(self.request, 'Autoridad Actuante Asignada.')

        return response
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['estacion'] = estacion
        autoridad_id = self.kwargs['autoridad_id']
        aut= get_object_or_404(Autoridades, pk=autoridad_id)

        initial['autoridad'] = aut
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        autoridad_id = self.kwargs['autoridad_id']
        aut= get_object_or_404(Autoridades, pk=autoridad_id)

        context['autoridad'] = aut
        context['navbar'] = 'catalogos'
        context['seccion'] = 'actuantes'        
        return context
    
class quitarAutoridadActuante(DeleteView):
    model = AutoridadesActuantes
    template_name = 'Autoridades/quitarAutoridad.html'
    success_url = reverse_lazy('agregaraAutoridadActuante')

    def delete(self, request, *args, **kwargs):
        with transaction.atomic():
            autoridad_actuante = self.get_object()

            # Obtén la autoridad relacionada
            autoridad = autoridad_actuante.autoridad

            # Cambia el estado de la autoridad relacionada a 'Libre'
            autoridad.estado = 'Libre'
            autoridad.save()

            # Elimina el registro de AutoridadesActuantes
            autoridad_actuante.delete()

            messages.success(self.request, 'Autoridad Actuante Deshabilitada.')

            return redirect(self.success_url)
    

