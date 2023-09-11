from django.shortcuts import render
from django.views.generic import CreateView, ListView,DetailView
from .models import Traslado, Extranjero
# Create your views here.
class ListTraslado(ListView):
    model = Traslado          
    template_name = "listPuestasTraslado.html" 
    context_object_name = 'puestasTraslado'

    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = Traslado.objects.filter(estacion_origen=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa

        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia

        puestas_count = self.get_queryset().count() 
        context['puestas_count'] = puestas_count

        #extranjeros_total = Extranjero.objects.filter(deLaEstacion=user_estacion).count() #OBTENER EL NUMERO TOTAL DE EXTRANJERO POR LA ESTACION 
        extranjeros_total = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion, estatus='Activo').count()
        context['extranjeros_total'] = extranjeros_total
        nacionalidades_count = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion).values('nacionalidad').distinct().count()
        context['nacionalidades_count'] = nacionalidades_count

        hombres_count = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion, genero=0, estatus='Activo').count()
        mujeres_count = Extranjero.objects.filter(deLaPuestaIMN__deLaEstacion=user_estacion, genero=1, estatus='Activo').count()
        context['mujeres_count'] = mujeres_count
        context['hombres_count'] = hombres_count
        capacidad_actual = user_estacion.capacidad
        context['capacidad_actual'] = capacidad_actual

        return context

class estadisticasPuestaINM(ListView):
    model=Traslado
    template_name =  "listPuestasTraslado.html" 
    context_object_name = 'puestainm'

    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = Traslado.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'traslado'  # Cambia esto según la página activa
        return context
    