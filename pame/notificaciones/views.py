from datetime import timezone
from typing import Any
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from weasyprint import HTML
from vigilancia.models import Extranjero
from vigilancia.views import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Defensorias,Relacion
from .forms import NotificacionesAceptadasForm,modalnotificicacionForm
from django.urls import reverse_lazy
from vigilancia.models import Extranjero
from django.utils import timezone
from django.template.loader import render_to_string, get_template

class notificar(LoginRequiredMixin,ListView):
    model = Defensorias
    template_name='notificacion.html'
    context_object_name = 'defensorias'
    login_url = '/permisoDenegado/'  
    def get_queryset(self):
        queryset =  Defensorias.objects.all()
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        apellido = extranjero.apellidoPaternoExtranjero
        nacionalidad = extranjero.nacionalidad
        apellidom = extranjero.apellidoMaternoExtranjero
        estacion = extranjero.deLaEstacion
        fechanacimiento = extranjero.fechaNacimiento
        numeroextranjero = extranjero.numeroExtranjero
        context['extranjero']=extranjero
        context['numeroextranjero']=numeroextranjero
        context['fechanacimiento']=fechanacimiento
        context['estacion']=estacion
        context['apellidom']=apellidom
        context['nacionalidad']=nacionalidad
        context['apellido']=apellido 
        context['nombre']= nombre
        context['navbar'] = 'notificaciones'
        context['seccion'] = 'defensoria'
        context['nombre_estacion'] = self.request.user.estancia.nombre
        return context

    
class defensoria(LoginRequiredMixin, ListView):
    model = Extranjero
    template_name='defensoria.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/'  
    def get_queryset(self):
        estacion_usuario = self.request.user.estancia

        estado = self.request.GET.get('estado_filtrado', 'activo')
        queryset = Extranjero.objects.filter(deLaEstacion=estacion_usuario).order_by('nombreExtranjero')

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset
        
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'notificaciones'
        context['seccion'] = 'notificaciones'
        context['nombre_estacion'] = self.request.user.estancia.nombre

        ahora = timezone.now() # Hora Actual

        for extranjero in context['extranjeros']:
            # Obtener el último NoProceso asociado a este extranjero
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()

            if ultimo_nup:
                # Obtener la hora de registro del último NoProceso
                hora_registro_nup = ultimo_nup.horaRegistroNup

                tiempo_transcurrido = ahora - hora_registro_nup
                horas_transcurridas, minutos_transcurridos = divmod(tiempo_transcurrido.total_seconds() / 3600, 1)
                horas_transcurridas = int(horas_transcurridas)
                minutos_transcurridos = int(minutos_transcurridos * 60)

                # Limitar a un máximo de 36 horas
                if horas_transcurridas > 36:
                    horas_transcurridas = 36
                    minutos_transcurridos = 0

                extranjero.horas_transcurridas = horas_transcurridas
                extranjero.minutos_transcurridos = minutos_transcurridos
            else:
                extranjero.horas_transcurridas = 0
                extranjero.minutos_transcurridos = 0
                
        return context
     


# views.py
from django.shortcuts import render, redirect
from .forms import DefensorForm

def defensores(request):
    if request.method == 'POST':
        form = DefensorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listdefensores')
    else:
        form = DefensorForm()

    context = {
        'form': form,
        'navbar': 'catalogos',
        'seccion': 'defensorias',
    }

    return render(request, 'defensorias.html', context)



class tabladefensores(LoginRequiredMixin,ListView):
    model = Defensorias
    template_name = 'tabladefensores.html'
    context_object_name = 'defensorias'
    login_url = '/permisoDenegado/' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'defensorias'    
        return context

    
from .models import notificacionesAceptadas, Defensorias

# views.py
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import notificacionesAceptadas, Defensorias
from .forms import NotificacionesAceptadasForm
from django.contrib import messages

class SubirArchivo(LoginRequiredMixin,CreateView):
    template_name = 'modal.html'
    form_class = NotificacionesAceptadasForm
    model = notificacionesAceptadas
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Archivo subido exitosamente')

        return reverse_lazy('defensoria')
    


class modalnotificar(LoginRequiredMixin,CreateView):
    template_name = 'modalnotificar.html'
    form_class = modalnotificicacionForm
    model = Relacion
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Notificacion creada exitosamente')

        return reverse_lazy('defensoria')
    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        defen_id = self.kwargs.get('defensoria_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        ultimo_proceso = extranjero.noproceso_set.latest('consecutivo')
        proceso_id = ultimo_proceso.nup
        initial['nup']= proceso_id
        defen = Defensorias.objects.get(id=defen_id)
        initial['defensoria']= defen
        initial['extranjero'] = extranjero
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero = self.kwargs['extranjero_id']
        defenso = self.kwargs['defensoria_id']
        context['extranjero']= get_object_or_404(Extranjero, pk=extranjero)
        context['defensoria'] = get_object_or_404(Defensorias, pk=defenso)   
        return context