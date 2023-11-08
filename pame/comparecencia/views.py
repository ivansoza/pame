from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from vigilancia.models import NoProceso, Extranjero
# Create your views here.
from django.db.models import OuterRef, Subquery

from .models import Comparecencia
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import ComparecenciaForm
def homeComparecencia(request):
    return render(request,"homeComparecencia.html")



class listExtranjerosComparecencia(ListView):

    model=NoProceso
    template_name="comparecencia/listExtranjerosComparecencia.html"
    context_object_name = "extranjeros"

    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        estado = self.request.GET.get('estado_filtrado','activo')
        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
        if estado == 'activo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
        elif estado == 'inactivo':
                extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

            # Obtener el último NoProceso para cada extranjero filtrado
        ultimo_no_proceso = NoProceso.objects.filter(
                extranjero_id=OuterRef('pk')
            ).order_by('-consecutivo')

        extranjeros_filtrados = extranjeros_filtrados.annotate(
                ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
            )

            # Ahora filtramos NoProceso basado en estos últimos registros
        queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id]
            )

        return queryset
    
    def get_context_data(self, **kwargs): 
            context = super().get_context_data(**kwargs)
            context['navbar'] = 'comparecencia'  # Cambia esto según la página activa
            context['seccion'] = 'comparecencia'
    
            return context
    

class CrearComparecencia(CreateView):
    model = Comparecencia
    form_class = ComparecenciaForm

    template_name = 'comparecencia/crearComparecencia.html'
    success_url = reverse_lazy('lisExtranjerosComparecencia')  # Reemplazar con el nombre de tu URL de lista de comparecencias

    def get_initial(self):
        nup_id = self.kwargs.get('nup_id')
        # Asegúrate de que 'nup' es el campo correcto en tu modelo NoProceso
        no_proceso = NoProceso.objects.get(nup=nup_id)
        return {
            'nup': no_proceso,
            # ... otros campos iniciales
        }
