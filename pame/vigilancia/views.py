from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Extranjero, PuestaDisposicionAC, PuestaDisposicionINM, Biometrico, Acompanante
from pertenencias.models import Inventario
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import extranjeroFormsAC, extranjeroFormsInm, puestDisposicionINMForm, puestaDisposicionACForm, BiometricoFormINM, BiometricoFormAC, AcompananteForm, editExtranjeroINMForm, editExtranjeroACForms
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalogos.models import Estacion, Relacion
from django.shortcuts import get_object_or_404
from django.db.models import Q


from django.http import JsonResponse
from django.views import View

class CreatePermissionRequiredMixin(UserPassesTestMixin):
    login_url = '/permisoDenegado/'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.permissions_required = kwargs.get('permissions_required', {})

    def test_func(self):
        user = self.request.user
        for permission, codename in self.permissions_required.items():
            if not user.has_perm(codename):
                raise PermissionDenied(f"No tienes el permiso necesario: {permission}")
        return True
   
    def test_func(self):
        return all(self.request.user.has_perm(perm) for perm in self.permission_required.values())
 
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            # Si el usuario está autenticado pero no tiene el permiso, redirige a una página de acceso denegado
            return redirect('permisoDenegado')  # Cambia 'acceso_denegado' a la URL adecuada
        else:
            # Si el usuario no está autenticado, redirige a la página de inicio de sesión
            return redirect(self.login_url)

   



# Create your views here.


def homeSeguridadGeneral(request):
    return render (request, "home/homeSeguridadGeneral.html",{'navbar':'home'})




def homeSeguridadResponsable(request):
    return render (request, "home/homeSeguridadResponsable.html")


def addAutoridadCompetente(request):
    return render(request, "addAutoridadCompetente.html")



def addHospedaje(request):
    return render(request, "addHospedaje.html")


def addTraslado(request):
    return render(request, "addTraslado.html")

def homePuestaINM (request):
    return render(request, "home/puestas/homePuestaINM.html")

def homePuestaVP (request):
    return render(request, "home/puestas/homePuestaVP.html")

#------------------------ Puesta por INM-----------------------------
class inicioINMList(ListView):
    model = PuestaDisposicionINM          
    template_name = "puestaINM/homePuestaINM.html" 
    context_object_name = 'puestasinm'

    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = PuestaDisposicionINM.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa

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

class createPuestaINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicioninm',
    }
    model = PuestaDisposicionINM               
    form_class = puestDisposicionINMForm      
    template_name = 'puestaINM/createPuestaINM.html'  
    success_url = reverse_lazy('homePuestaINM')

    def get_initial(self):
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            UsuarioId = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        # Generar el número con formato automáticamente
        ultimo_registro = PuestaDisposicionINM.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroOficio.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/INM/{estacion_id}/{UsuarioId}/{ultimo_numero + 1:04d}'

        initial['numeroOficio'] = nuevo_numero
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context

class createExtranjeroINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'puestaINM/crearExtranjeroINM.html' 
    # success_url = reverse_lazy('homePuestaINM')
    
    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        if self.object.viajaSolo:
            return reverse('agregar_biometricoINM', args=[extranjero_id])
        else:
            # return reverse('crearExtranjeroAC', args=[puesta_id])
            return reverse('listAcompanantesINM', args=[extranjero_id, puesta_id])
                
    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass

        ultimo_registro = Extranjero.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroExtranjero.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/EXT/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroExtranjero'] = nuevo_numero
        return {'deLaPuestaIMN': puesta, 'deLaEstacion':estacion, 'numeroExtranjero':nuevo_numero, 'viajaSolo':viaja_solo} 

    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        if estacion:
            estacion.capacidad -= 1
            estacion.save()     
        

        extranjero = form.save(commit=False)  # Crea una instancia de Extranjero sin guardarla en la base de datos
        extranjero.puesta = puesta
        extranjero.save()  #
        
        return super().form_valid(form)
    
    


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa

        return context

class listarExtranjeros(ListView):
    model = Extranjero
    template_name = 'puestaINM/listExtranjeros.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        estado = self.request.GET.get('estado_filtrado', 'activo') 
        queryset = Extranjero.objects.filter(deLaPuestaIMN_id=puesta_id)

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)  # Asegúrate de reemplazar 'Puesta' con el nombre correcto de tu modelo
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
     
class EditarExtranjeroINM(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroINMForm
    template_name = 'puestaINM/editarExtranjeroINM.html'

    def get_success_url(self):
        return reverse('listarExtranjeros', args=[self.object.deLaPuestaIMN.id])
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)  # Obtén el extranjero original antes de modificar

        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta'] = self.object.deLaPuestaIMN
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class AgregarBiometricoINM(CreateView):
    model = Biometrico
    form_class = BiometricoFormINM
    template_name = 'puestaINM/createBiometricosINM.html'  # Cambiar a la ruta correcta

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeros', args=[extranjero.deLaPuestaIMN.id])
    
    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        initial['Extranjero'] = extranjero
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del extranjero del argumento en la URL
        extranjero_id = self.kwargs.get('extranjero_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context

class EditarBiometricoINM(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_biometrico',
    }
    model = Biometrico
    form_class = BiometricoFormINM
    template_name = 'puestaINM/editBiometricosINM.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeros', args=[extranjero.deLaPuestaIMN.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaIMN
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context


class DeleteExtranjeroINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Extranjero
    template_name = 'modal/eliminarExtranjeroINM.html'

    def get_success_url(self):
        puesta_id = self.object.deLaPuestaIMN.id
        return reverse('listarExtranjeros', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context

class acompananteList(ListView):
    model = Extranjero
    template_name = "puestaINM/listAcompananteINM.html" 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)

        # Obtener la lista de extranjeros de la misma puesta
        extranjeros_puesta = Extranjero.objects.filter(deLaPuestaIMN_id=puesta_id, estatus ='Activo').exclude(pk=extranjero_principal_id)

        # Filtrar extranjeros no relacionados
        extranjeros_no_relacionados = extranjeros_puesta.exclude(
            Q(acompanantes_delExtranjero__delAcompanante=extranjero_principal) |
            Q(acompanantes_delAcompanante__delExtranjero=extranjero_principal)
        )

        # Filtrar las relaciones donde el extranjero principal es delExtranjero y no está relacionado como delAcompanante
        relaciones_del_extranjero = Acompanante.objects.filter(delExtranjero=extranjero_principal).exclude(delAcompanante=extranjero_principal)
        
        # Filtrar las relaciones donde el extranjero principal es delAcompanante y no está relacionado como delExtranjero
        relaciones_del_acompanante = Acompanante.objects.filter(delAcompanante=extranjero_principal).exclude(delExtranjero=extranjero_principal)

        context['extranjero_principal'] = extranjero_principal
        context['extranjeros_no_relacionados'] = extranjeros_no_relacionados
        context['relaciones_del_extranjero'] = relaciones_del_extranjero
        context['relaciones_del_acompanante'] = relaciones_del_acompanante
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    
class AgregarAcompananteViewINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_acompanante',
    }
    model = Acompanante
    form_class = AcompananteForm
    template_name = 'modal/acompananteINM.html'

    def get_success_url(self):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        return reverse_lazy('listAcompanantesINM', kwargs={'extranjero_id': extranjero_principal.id, 'puesta_id': extranjero_principal.deLaPuestaIMN.id})
    
    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']

        form.instance.delExtranjero_id = extranjero_principal_id
        form.instance.delAcompanante_id = extranjero_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']
        context['extranjero_principal'] = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        context['extranjero'] = get_object_or_404(Extranjero, pk=extranjero_id)
        return context
    
class DeleteAcompananteINM(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteINM.html'

    def get_success_url(self):
        acompanante = self.object

        # Obtener los IDs necesarios
        extranjero_id = acompanante.delExtranjero.id
        puesta_id = acompanante.delExtranjero.deLaPuestaIMN.id

        # Generar la URL con los IDs
        return reverse_lazy('listAcompanantesINM', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
class DeleteAcompananteINM1(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteINM1.html'

    def get_success_url(self):
        acompanante = self.object

        # Obtener los IDs necesarios
        extranjero_id = acompanante.delAcompanante.id
        puesta_id = acompanante.delAcompanante.deLaPuestaIMN.id

        # Generar la URL con los IDs
        return reverse_lazy('listAcompanantesINM', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        
        return context
    

class DeleteAcompananteAC(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteAC.html'

    def get_success_url(self):
        acompanante = self.object

        # Obtener los IDs necesarios
        extranjero_id = acompanante.delExtranjero.id
        puesta_id = acompanante.delExtranjero.deLaPuestaAC.id

        # Generar la URL con los IDs
        return reverse_lazy('listAcompanantesAC', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
class DeleteAcompananteAC1(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Acompanante
    template_name = 'modal/eliminarAcompananteAC1.html'

    def get_success_url(self):
        acompanante = self.object

        # Obtener los IDs necesarios
        extranjero_id = acompanante.delAcompanante.id
        puesta_id = acompanante.delAcompanante.deLaPuestaAC.id

        # Generar la URL con los IDs
        return reverse_lazy('listAcompanantesAC', args=[extranjero_id, puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['puesta_id'] = self.object.deLaPuestaIMN.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context
    
    
    
class createExtranjeroAcomINM(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsInm    
    template_name = 'puestaINM/crearAcompananteINM.html' 
    # success_url = reverse_lazy('homePuestaINM')
    
    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        # extranjero_id = self.object.id  
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal del contexto

        # Obtén el ID del extranjero recién creado
            # return reverse('crearExtranjeroAC', args=[puesta_id])

        return reverse('listAcompanantesINM', args=[extranjero_principal_id, puesta_id])
        
    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
            viaja_solo = True
            initial['viajaSolo']= viaja_solo
        except Usuario.DoesNotExist:
            pass

        ultimo_registro = Extranjero.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroExtranjero.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/EXT/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroExtranjero'] = nuevo_numero
        return {'deLaPuestaIMN': puesta, 'deLaEstacion':estacion, 'numeroExtranjero':nuevo_numero, 'viajaSolo':viaja_solo} 

    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionINM.objects.get(id=puesta_id)
        extranjero = form.save(commit=False)  # Crea una instancia de Extranjero sin guardarla en la base de datos
        extranjero.puesta = puesta
        extranjero.save()  #
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionINM.objects.get(id=puesta_id)
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal
        context['extranjero_principal_id'] = extranjero_principal_id  # Pasa el ID al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa

        return context

#------------------------ Fin Puesta por INM-----------------------------

#------------------------  Puesta por AC -----------------------------
class inicioACList(ListView):
    model = PuestaDisposicionAC
    template_name = "puestaAC/homePuestaAC.html" 
    context_object_name = 'puestaAC'
    
    def get_queryset(self):
        # Filtrar las puestas por estación del usuario logueado
        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia
        queryset = PuestaDisposicionAC.objects.filter(deLaEstacion=user_estacion)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        user_profile = self.request.user  # Ajusta según cómo se llama la relación en tu modelo de usuario
        user_estacion = user_profile.estancia

        puestas_count = self.get_queryset().count() 
        context['puestas_count'] = puestas_count

        #extranjeros_total = Extranjero.objects.filter(deLaEstacion=user_estacion).count() #OBTENER EL NUMERO TOTAL DE EXTRANJERO POR LA ESTACION 
        extranjeros_total = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion, estatus='Activo').count()
        context['extranjeros_total'] = extranjeros_total
        nacionalidades_count = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion).values('nacionalidad').distinct().count()
        context['nacionalidades_count'] = nacionalidades_count

        hombres_count = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion, genero=0, estatus='Activo').count()
        mujeres_count = Extranjero.objects.filter(deLaPuestaAC__deLaEstacion=user_estacion, genero=1, estatus='Activo').count()
        context['mujeres_count'] = mujeres_count
        context['hombres_count'] = hombres_count
        capacidad_actual = user_estacion.capacidad
        context['capacidad_actual'] = capacidad_actual

        return context
    
class createPuestaAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_puestadisposicionac',
    }
    model = PuestaDisposicionAC               
    form_class = puestaDisposicionACForm      
    template_name = 'puestaAC/createPuestaAC.html'  
    success_url = reverse_lazy('homePuestaAC')

    def get_initial(self):
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id = usuario_data.id
            estacion_id = usuario_data.estancia_id
            estado = usuario_data.estancia.estado.estado
            estacionM = usuario_data.estancia.nombre
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
         # Generar el número con formato automáticamente
        ultimo_registro = PuestaDisposicionAC.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroOficio.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/AC/{estacion_id}/{usuario_id}/{ultimo_numero + 1:04d}'

        initial['numeroOficio'] = nuevo_numero
        initial['entidadFederativa'] = estado
        initial['dependencia'] = estacionM
        return initial

        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
    
class createExtranjeroAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'puestaAC/createExtranjeroAC.html' 

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        if self.object.viajaSolo:
            return reverse('agregar_biometricoAC', args=[extranjero_id])
        else:
            # return reverse('crearExtranjeroAC', args=[puesta_id])
            return reverse('listAcompanantesAC', args=[extranjero_id, puesta_id])

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
       
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id= usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        ultimo_registro = Extranjero.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroExtranjero.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/EXT/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroExtranjero'] = nuevo_numero
        viaja_solo = True
        initial['viajaSolo'] = viaja_solo
        return {'deLaPuestaAC': puesta, 'deLaEstacion':estacion, 'numeroExtranjero':nuevo_numero, 'viajaSolo': viaja_solo } 
     
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        estacion = form.cleaned_data['deLaEstacion']
        
        if estacion:
            estacion.capacidad -= 1
            estacion.save()

        extranjero = form.save(commit=False)
        extranjero.puesta = puesta
        extranjero.save()

        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class listarExtranjerosAC(ListView):
    model = Extranjero
    template_name = 'puestaAC/listExtranjerosAC.html'
    context_object_name = 'extranjeros'

    def get_queryset(self):
        puesta_id = self.kwargs['puesta_id']
        estado = self.request.GET.get('estado_filtrado', 'activo') 
        queryset = Extranjero.objects.filter(deLaPuestaAC_id=puesta_id)

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)  # Asegúrate de reemplazar 'Puesta' con el nombre correcto de tu modelo
        context['puesta'] = puesta
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class EditarExtranjeroAC(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
         'perm1': 'vigilancia.change_extranjero',
    }
    model = Extranjero
    form_class = editExtranjeroACForms
    template_name = 'puestaAC/editarExtranjeroAC.html'
    def form_valid(self, form):
        extranjero = form.save(commit=False)
        old_extranjero = Extranjero.objects.get(pk=extranjero.pk)  # Obtén el extranjero original antes de modificar

        if old_extranjero.estatus == 'Activo' and extranjero.estatus == 'Inactivo':
            # Cambio de estatus de Activo a Inactivo
            estacion = extranjero.deLaEstacion
            if estacion:
                estacion.capacidad += 1
                estacion.save()

        elif old_extranjero.estatus == 'Inactivo' and extranjero.estatus == 'Activo':
            # Cambio de estatus de Inactivo a Activo
            estacion = extranjero.deLaEstacion
            if estacion and estacion.capacidad > 0:
                estacion.capacidad -= 1
                estacion.save()

        extranjero.save()

        return super().form_valid(form)
    

    def get_success_url(self):
        return reverse('listarExtranjeroAC', args=[self.object.deLaPuestaAC.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
        extranjero = Extranjero.objects.get(id=extranjero_id)
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['puesta'] = self.object.deLaPuestaAC
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context    

class AgregarBiometricoAC(CreateView):
    model = Biometrico
    form_class = BiometricoFormAC
    template_name = 'puestaAC/createBiometricosAC.html'  # Cambiar a la ruta correcta

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    
    def get_initial(self):
        initial = super().get_initial()
        extranjero_id = self.kwargs.get('extranjero_id')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        initial['Extranjero'] = extranjero
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén el ID del extranjero del argumento en la URL
        extranjero_id = self.kwargs.get('extranjero_id')
        # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaAC
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context

class EditarBiometricoAC(CreatePermissionRequiredMixin,UpdateView):
    permission_required = {
        'perm1': 'vigilancia.change_biometrico',
    }
    model = Biometrico
    form_class = BiometricoFormAC
    template_name = 'puestaAC/editBiometricosAC.html' 

    def get_success_url(self):
        extranjero_id = self.object.Extranjero.id  # Obtén el ID del extranjero del objeto biometrico
        extranjero = Extranjero.objects.get(id=extranjero_id)
        return reverse('listarExtranjeroAC', args=[extranjero.deLaPuestaAC.id])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    # Obtén el ID del extranjero del argumento en el URL
        extranjero_id = self.kwargs.get('pk')  # Cambia 'extranjero_id' a 'pk'
    # Obtén la instancia del extranjero correspondiente al ID
        extranjero = Extranjero.objects.get(id=extranjero_id)
        puesta = extranjero.deLaPuestaAC
        context['puesta'] = puesta
        context['extranjero'] = extranjero  # Agregar el extranjero al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context

class DeleteExtranjeroAC(DeleteView):
    permission_required = {
        'perm1': 'vigilancia.delete_extranjero',
    }
    model = Extranjero
    template_name = 'modal/eliminarExtranjeroAC.html'
    
    def get_success_url(self):
        puesta_id = self.object.deLaPuestaAC.id
        return reverse('listarExtranjeroAC', args=[puesta_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['puesta_id'] = self.object.deLaPuestaAC.id
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context

class createAcompananteAC(CreatePermissionRequiredMixin,CreateView):
    permission_required = {
        'perm1': 'vigilancia.add_extranjero',
    }
    model =Extranjero             
    form_class = extranjeroFormsAC    
    template_name = 'puestaAC/createAcompananteAC.html' 

    def get_success_url(self):
        puesta_id = self.kwargs['puesta_id']
        # extranjero_id = self.object.id  # Obtén el ID del extranjero recién creado
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal del contexto

        return reverse('listAcompanantesAC', args=[extranjero_principal_id, puesta_id])
    

    def get_initial(self):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
       
        initial = super().get_initial()

        # Acceder al usuario autenticado y sus datos en la base de datos
        Usuario = get_user_model()
        usuario = self.request.user
        try:
            usuario_data = Usuario.objects.get(username=usuario.username)
            # Obtener la instancia de Estacion correspondiente al ID de la estación del usuario
            usuario_id= usuario_data.id
            estacion_id = usuario_data.estancia_id
            estacion = Estacion.objects.get(pk=estacion_id)
            initial['deLaEstacion'] = estacion
        except Usuario.DoesNotExist:
            pass
        ultimo_registro = Extranjero.objects.order_by('-id').first()
        ultimo_numero = int(ultimo_registro.numeroExtranjero.split(f'/')[-1]) if ultimo_registro else 0
        nuevo_numero = f'2023/EXT/{estacion_id}/{usuario_id}/{ultimo_numero + 1:06d}'
        initial['numeroExtranjero'] = nuevo_numero
        viaja_solo = True
        initial['viajaSolo'] = viaja_solo
        return {'deLaPuestaAC': puesta, 'deLaEstacion':estacion, 'numeroExtranjero':nuevo_numero, 'viajaSolo': viaja_solo } 
     
    def form_valid(self, form):
        puesta_id = self.kwargs['puesta_id']
        puesta = PuestaDisposicionAC.objects.get(id=puesta_id)
        extranjero = form.save(commit=False)  # Crea una instancia de Extranjero sin guardarla en la base de datos
        extranjero.puesta = puesta
        extranjero.save()  #
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        puesta_id = self.kwargs['puesta_id']
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)
        extranjero_principal_id = self.kwargs.get('extranjero_principal_id')  # Obtén el ID del extranjero principal
        context['extranjero_principal_id'] = extranjero_principal_id  # Pasa el ID al contexto
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa

        return context
    
class ListAcompanantesAC(ListView):
    model = Extranjero
    template_name = 'puestaAC/listAcompanantesAC.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        extranjero_principal_id = self.kwargs.get('extranjero_id')
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta'] = PuestaDisposicionAC.objects.get(id=puesta_id)

        # Obtener datos del extranjero principal
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)

        # Obtener la lista de extranjeros de la misma puesta
        extranjeros_puesta = Extranjero.objects.filter(deLaPuestaAC_id=puesta_id, estatus='Activo').exclude(pk=extranjero_principal_id)
        
        # Filtrar extranjeros no relacionados
        extranjeros_no_relacionados = extranjeros_puesta.exclude(
            Q(acompanantes_delExtranjero__delAcompanante=extranjero_principal) |
            Q(acompanantes_delAcompanante__delExtranjero=extranjero_principal)
        )

        # Filtrar las relaciones donde el extranjero principal es delExtranjero y no está relacionado como delAcompanante
        relaciones_del_extranjero = Acompanante.objects.filter(delExtranjero=extranjero_principal).exclude(delAcompanante=extranjero_principal)
        
        # Filtrar las relaciones donde el extranjero principal es delAcompanante y no está relacionado como delExtranjero
        relaciones_del_acompanante = Acompanante.objects.filter(delAcompanante=extranjero_principal).exclude(delExtranjero=extranjero_principal)

        context['extranjero_principal'] = extranjero_principal
        context['extranjeros_no_relacionados'] = extranjeros_no_relacionados
        context['relaciones_del_extranjero'] = relaciones_del_extranjero
        context['relaciones_del_acompanante'] = relaciones_del_acompanante
        context['navbar'] = 'seguridad' 
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        
        return context


class AgregarAcompananteViewAC(CreateView):
    model = Acompanante
    form_class = AcompananteForm
    # template_name = 'puestaAC/agregar_acompananteAC.html'
    template_name = 'modal/acompananteAC.html'

    def get_success_url(self):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        return reverse_lazy('listAcompanantesAC', kwargs={'extranjero_id': extranjero_principal.id, 'puesta_id': extranjero_principal.deLaPuestaAC.id})
    
    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']

        form.instance.delExtranjero_id = extranjero_principal_id
        form.instance.delAcompanante_id = extranjero_id

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_id = self.kwargs['extranjero_id']
        context['extranjero_principal'] = get_object_or_404(Extranjero, pk=extranjero_principal_id)
        context['extranjero'] = get_object_or_404(Extranjero, pk=extranjero_id)
        return context
    



class CrearRelacionAcompananteAC(CreateView):
    model = Acompanante
    form_class = AcompananteForm
    template_name= 'puestaAC/listAcompanantesAC.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        kwargs['extranjero_principal_id'] = extranjero_principal_id
        return kwargs

    def form_valid(self, form):
        extranjero_principal_id = self.kwargs['extranjero_principal_id']
        extranjero_principal = Extranjero.objects.get(pk=extranjero_principal_id)

        self.object = form.save(commit=False)
        self.object.delExtranjero = extranjero_principal
        self.object.save()

        puesta_id = extranjero_principal.deLaPuestaAC_id
        return redirect('listAcompanantesAC', extranjero_principal.id, puesta_id)
    
class CrearRelacionView(View):
    def post(self, request, extranjero_id, relacion_id):
        extranjero_principal = Extranjero.objects.get(pk=extranjero_id)
        relacion = Relacion.objects.get(pk=relacion_id)

        # Crea la relación
        nueva_relacion = Acompanante(delExtranjero=extranjero_principal, relacion=relacion)
        nueva_relacion.save()

        return JsonResponse({'success': True})