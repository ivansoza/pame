from django.shortcuts import render
from .forms import ResponsableForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Puesta, Extranjero
from .forms import PuestaForm, ExtranjeroForm
from django.views.generic import ListView, CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy
from django.urls import reverse


# Create your views here.
from .models import Responsable


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

class PuestaListView(ListView):
    model = Puesta
    template_name = 'listPuesta.html'  # Reemplaza con el nombre de tu plantilla de lista de puestas
    context_object_name = 'puestas' 

class PuestaCreateView(CreateView):
    model = Puesta
    form_class = PuestaForm
    template_name = 'createPuesta.html'  # Reemplaza con el nombre de tu plantilla
    success_url = reverse_lazy('lista_puestas')  # Reemplaza con la URL de la lista de puestas


class ExtranjeroCreateView(CreateView):
    model = Extranjero
    form_class = ExtranjeroForm
    template_name = 'createExtranjero.html'  # Reemplaza con el nombre de tu plantilla
    success_url = reverse_lazy('lista_puestas')  # Reemplaza con la URL de la lista de puestas

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = Puesta.objects.get(id=puesta_id)
        return {'puesta': puesta}  # Inicializa el campo de puesta en el formulario
    
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = Puesta.objects.get(id=puesta_id)
        
        extranjero = form.save(commit=False)  # Crea una instancia de Extranjero sin guardarla en la base de datos
        extranjero.puesta = puesta
        extranjero.save()  # Ahora guarda la instancia con la relación establecida
        
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = Puesta.objects.get(id=puesta_id)
        return context
    
class ExtranjeroListView(ListView):
    model = Extranjero
    template_name = 'listExtranjeros.html'  # Reemplaza con el nombre de tu plantilla de lista de extranjeros
    context_object_name = 'extranjeros'
    
    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        return Extranjero.objects.filter(puesta__id=puesta_id)
    
class ExtranjeroUpdateView(UpdateView):
    model = Extranjero
    form_class = ExtranjeroForm
    template_name = 'editarExtranjero.html'  # Nombre de tu plantilla de edición de extranjero
    
    def get_success_url(self):
        return reverse('lista_extranjeros', args=[self.object.puesta.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta'] = self.object.puesta
        return context
    
class ExtranjeroDeleteView(DeleteView):
    model = Extranjero
    template_name = 'eliminarExtranjero.html'
    
    def get_success_url(self):
        puesta_id = self.object.puesta.id
        return reverse('lista_extranjeros', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.puesta.id
        return context
