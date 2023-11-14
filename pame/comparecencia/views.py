from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from vigilancia.models import NoProceso, Extranjero, AutoridadesActuantes, AsignacionRepresentante
# Create your views here.
from django.db.models import OuterRef, Subquery,Exists
from django.shortcuts import get_object_or_404

from .models import Comparecencia
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy
from .forms import ComparecenciaForm
from django.db.models import Q
from django.http import JsonResponse
from catalogos.models import Traductores
def homeComparecencia(request):
    return render(request,"homeComparecencia.html")



class listExtranjerosComparecencia(ListView):
    model=NoProceso
    template_name="comparecencia/listExtranjerosComparecencia.html"
    context_object_name = "extranjeros"

    def get_queryset(self):
        estacion_usuario = self.request.user.estancia
        estado = self.request.GET.get('estado_filtrado', 'activo')
        
        representantes_asignados = AsignacionRepresentante.objects.filter(
            no_proceso=OuterRef('pk')
        )
        
        extranjeros_filtrados = Extranjero.objects.filter(deLaEstacion=estacion_usuario)
        if estado == 'activo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Activo')
        elif estado == 'inactivo':
            extranjeros_filtrados = extranjeros_filtrados.filter(estatus='Inactivo')

        ultimo_no_proceso = NoProceso.objects.filter(
            extranjero_id=OuterRef('pk')
        ).order_by('-consecutivo')
        
        extranjeros_filtrados = extranjeros_filtrados.annotate(
            ultimo_nup_id=Subquery(ultimo_no_proceso.values('nup')[:1])
        )

        queryset = NoProceso.objects.filter(
            nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id],
            extranjero__deLaEstacion=estacion_usuario

        ).annotate(
            tiene_asignacion=Exists(representantes_asignados)
        )

        # Filtrar solo aquellos NoProceso que tienen un representante asignado
        queryset = queryset.filter(tiene_asignacion=True)

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
    success_url = reverse_lazy('lisExtranjerosComparecencia')  

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        nup_id = self.kwargs.get('nup_id')
        no_proceso = NoProceso.objects.get(nup=nup_id)
        extranjero = no_proceso.extranjero
        autoridades = AutoridadesActuantes.objects.none()  

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
            autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)

        form.fields['autoridadActuante'].queryset = autoridades
        form.fields['traductor'].queryset = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)

        return form
    def get_initial(self):
        initial = super(CrearComparecencia, self).get_initial()
        nup_id = self.kwargs.get('nup_id')
        no_proceso = get_object_or_404(NoProceso, nup=nup_id)
        extranjero = no_proceso.extranjero
        initial['nup'] = no_proceso
        initial['estadoCivil'] = extranjero.estado_Civil
        initial['escolaridad'] = extranjero.grado_academico
        initial['ocupacion'] = extranjero.ocupacion
        initial['nacionalidad'] = extranjero.nacionalidad.nombre  
        initial['nombrePadre'] = extranjero.nombreDelPadre
        initial['nombreMadre'] = extranjero.nombreDelaMadre
        initial['nacionalidadPadre'] = extranjero.nacionalidad_Padre.nombre if extranjero.nacionalidad_Padre else ''
        initial['nacionalidadMadre'] = extranjero.nacionalidad_Madre.nombre if extranjero.nacionalidad_Madre else ''
        return initial
    def form_valid(self, form):
        form.instance.nup = get_object_or_404(NoProceso, nup=self.kwargs.get('nup_id'))
        return super(CrearComparecencia, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            nup_id = self.kwargs.get('nup_id')
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            context['extranjero'] = no_proceso.extranjero
            context['navbar'] = 'comparecencia'  
            context['seccion'] = 'comparecencia'
            return context
    

class CrearComparecenciaAjax(View):
    def post(self, request, nup_id, *args, **kwargs):
        form = ComparecenciaForm(request.POST)
        if form.is_valid():
            comparecencia = form.save(commit=False)
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            comparecencia.nup = no_proceso
            comparecencia.save()
            data = {'success': True, 'message': 'Comparecencia creada con éxito.'}
            return JsonResponse(data, status=200)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)

    def get(self, request, nup_id, *args, **kwargs):
            no_proceso = get_object_or_404(NoProceso, nup=nup_id)
            extranjero = no_proceso.extranjero

            # Crear el formulario y establecer valores iniciales
            form = ComparecenciaForm(initial={
                'estadoCivil': extranjero.estado_Civil,
                'escolaridad': extranjero.grado_academico,
                'ocupacion': extranjero.ocupacion,
                'nacionalidad': extranjero.nacionalidad.nombre,
                'nombrePadre': extranjero.nombreDelPadre,
                'nombreMadre': extranjero.nombreDelaMadre,
                'nacionalidadPadre': extranjero.nacionalidad_Padre.nombre if extranjero.nacionalidad_Padre else '',
                'nacionalidadMadre': extranjero.nacionalidad_Madre.nombre if extranjero.nacionalidad_Madre else ''
            })

            # Filtrar las autoridades actuantes según la lógica proporcionada
            autoridades = AutoridadesActuantes.objects.none()
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
                autoridades = AutoridadesActuantes.objects.filter(estacion=extranjero.deLaEstacion)

            # Establecer el queryset de autoridades actuantes y traductor
            form.fields['autoridadActuante'].queryset = autoridades
            form.fields['traductor'].queryset = Traductores.objects.filter(estacion=extranjero.deLaEstacion)

            # Preparar el contexto para la plantilla
            context = {
                'form': form,
                'nup_id': nup_id,
                'extranjero': extranjero,
                'navbar': 'comparecencia',
                'seccion': 'comparecencia',
            }
            return render(request, 'comparecencia/crearComparecencia1.html', context)
        
