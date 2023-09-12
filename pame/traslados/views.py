from django.shortcuts import render
from django.views.generic import CreateView, ListView,DetailView
from .models import Traslado, Extranjero
from vigilancia.models import Estacion
from django.http import JsonResponse
from .forms import TrasladoForm
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model


# Create your views here.
class ListTraslado(ListView):
    model = Traslado          
    template_name = "origen/listPuestasTraslado.html" 
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
    
class listarEstaciones(ListView):
    model = Extranjero
    template_name = "origen/selecEstacion.html"
    context_object_name = 'traslado'

    def get_queryset(self):
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        queryset = Extranjero.objects.filter(deLaEstacion=user_estacion, estatus='Activo')
        return queryset    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'traslado'  # Cambia esto según la página activa
        context['seccion'] = 'vertraslado'  # Cambia esto según la página activa
        user_profile = self.request.user
        user_estacion = user_profile.estancia
        estaciones = Estacion.objects.exclude(pk=user_estacion.pk)
        context['estaciones'] = estaciones
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)  # Esto imprimirá todo el contenido POST
     


        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            estacion_id = request.POST.get('estacion_id')
            try:
                estacion = Estacion.objects.get(pk=estacion_id)
                # Obtén el nombre del responsable de la estación
                responsable_nombre = f"{estacion.responsable.nombre} {estacion.responsable.apellidoPat} {estacion.responsable.apellidoMat}"
                estado_nombre = estacion.estado.estado  # Accede directamente al nombre del estado
                estancia_nombre = estacion.nombre
                email_nombre = estacion.email
                calle_nombre = estacion.calle
                noext_nombre = estacion.noext
                cp_nombre = estacion.cp
                colonia_nombre = estacion.colonia
                tel_reponsable = estacion.responsable.telefono
                email_responsable = estacion.responsable.email
                return JsonResponse({'capacidad': estacion.capacidad, 
                                     'responsable': responsable_nombre, 
                                     'estado': estado_nombre,
                                     'estancia':estancia_nombre,
                                     'email':email_nombre,
                                     'calle':calle_nombre,
                                     'no':noext_nombre,
                                     'cp':cp_nombre,
                                     'colonia':colonia_nombre,
                                     'telResponsable':tel_reponsable,
                                     'emailResponsable':email_responsable

                                     })
            except Estacion.DoesNotExist:
                return JsonResponse({'capacidad': 'N/A', 
                                     'responsable': 'N/A',
                                     'estado':'N/A',
                                     'estancia':'N/A',
                                     'email':'N/A',
                                     'calle':'N/A',
                                     'no':'N/A',
                                     'cp':'N/A',
                                     'colonia':'N/A',
                                     'telResponsable':'N/A',
                                     'emailResponsable':'N/A'

                                     })
        

        return super().post(request, *args, **kwargs)


# class TrasladoCreateView(CreateView):
#     model = Traslado
#     form_class = TrasladoForm
#     template_name = 'origen/crearPuestaTraslado.html'  # Este será el nombre del archivo HTML que crearás a continuación.
#     success_url = reverse_lazy('traslado')  # Ajusta este nombre según tu archivo urls.py

#     def get_initial(self):
#         initial = super().get_initial()
#         initial['estacion_origen'] = self.kwargs['origen_id']
#         initial['estacion_destino'] = self.kwargs['destino_id']
#         return initial

class TrasladoCreateView(CreateView):
    model = Traslado
    form_class = TrasladoForm
    template_name = 'modal/crearPuestaTraslado.html'  # Este será el nombre del archivo HTML que crearás a continuación.
    success_url = reverse_lazy('traslado')  # Ajusta este nombre según tu archivo urls.py
    def form_valid(self, form):
        # Obtener los valores de origen_id y destino_id de la URL
        origen_id = self.kwargs['origen_id']
        destino_id = self.kwargs['destino_id']
        
        # Asignar los valores a las instancias de estacion_origen y estacion_destino
        form.instance.estacion_origen_id = origen_id
        form.instance.estacion_destino_id = destino_id

        return super().form_valid(form)
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass

        ultimo_registro = Traslado.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroUnicoProceso.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/TRASLADO/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroUnicoProceso'] = nuevo_numero
        initial['estacion_origen'] = self.kwargs['origen_id']
        initial['estacion_destino'] = self.kwargs['destino_id']
        return initial

       