from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from vigilancia.models import NoProceso, Extranjero, AutoridadesActuantes
# Create your views here.
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404

from .models import Comparecencia
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import ComparecenciaForm
from django.db.models import Q

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

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        nup_id = self.kwargs.get('nup_id')
        no_proceso = NoProceso.objects.get(nup=nup_id)
        extranjero = no_proceso.extranjero

        # Verificar si existe una puesta IMN o AC asociada al extranjero y obtener las autoridades correspondientes.
        autoridades = AutoridadesActuantes.objects.none()  # Queryset vacío por defecto

        if extranjero.deLaPuestaIMN:
            autoridades = AutoridadesActuantes.objects.filter(
                Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaUno_id) |
                Q(id=extranjero.deLaPuestaIMN.nombreAutoridadSignaDos_id)
            )
        elif extranjero.deLaPuestaAC:
            autoridades = AutoridadesActuantes.objects.filter(
                Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaUno_id) |
                Q(id=extranjero.deLaPuestaAC.nombreAutoridadSignaDos_id)
            )
        else:
            # Si no hay puesta IMN o AC, se podrían listar todas las autoridades de la estación.
            autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)

        # Establecer el queryset para los campos del formulario.
        form.fields['autoridadActuante'].queryset = autoridades
        form.fields['traductor'].queryset = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)

        return form
    def get_initial(self):
        initial = super(CrearComparecencia, self).get_initial()
        nup_id = self.kwargs.get('nup_id')
        # Asegúrate de que 'nup' es el campo correcto en tu modelo NoProceso
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero

        initial['nup'] = no_proceso
        initial['estadoCivil'] = extranjero.estado_Civil
        initial['escolaridad'] = extranjero.grado_academico
        initial['ocupacion'] = extranjero.ocupacion
        initial['nacionalidad'] = extranjero.nacionalidad.nombre  # Asumiendo que nacionalidad es una relación ForeignKey y queremos el nombre
        initial['nombrePadre'] = extranjero.nombreDelPadre
        initial['nombreMadre'] = extranjero.nombreDelaMadre
        initial['nacionalidadPadre'] = extranjero.nacionalidad_Padre.nombre if extranjero.nacionalidad_Padre else ''
        initial['nacionalidadMadre'] = extranjero.nacionalidad_Madre.nombre if extranjero.nacionalidad_Madre else ''

        return initial
    def form_valid(self, form):
        # Asegúrate de que la instancia de 'Comparecencia' tiene una referencia al 'NoProceso' correcto
        form.instance.nup = get_object_or_404(NoProceso, nup=self.kwargs.get('nup_id'))
        return super(CrearComparecencia, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            nup_id = self.kwargs.get('nup_id')
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            context['extranjero'] = no_proceso.extranjero
            context['navbar'] = 'comparecencia'  # Cambia esto según la página activa
            context['seccion'] = 'comparecencia'
            return context