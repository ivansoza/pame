from django.shortcuts import render
from django.views.generic import CreateView, ListView
from .forms import AlegatosForms, DocumentosAlegatosForms
from vigilancia.models import Extranjero, NoProceso
from .models import Alegatos, DocumentosAlegatos
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from catalogos.models import Estacion
from django.shortcuts import get_object_or_404
from generales.mixins import HandleFileMixin
from django.db.models import Max

class listaExtranjertoAlegatos(LoginRequiredMixin, ListView):
    model = Extranjero
    template_name ='alegato/ExtranjeroAlegato.html'
    context_object_name = 'extranjeros'
    login_url = '/permisoDenegado/' 
    def get_queryset(self):
        # Obtener la estación del usuario actualmente autenticado.
        estacion_usuario = self.request.user.estancia

        estado = self.request.GET.get('estado_filtrado', 'activo')
        # Filtrar por estación del usuario y ordenar por nombre de extranjero.
        queryset = Extranjero.objects.filter(deLaEstacion=estacion_usuario).order_by('nombreExtranjero')

        if estado == 'activo':
            queryset = queryset.filter(estatus='Activo')
        elif estado == 'inactivo':
            queryset = queryset.filter(estatus='Inactivo')
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'alegatos'  # Cambia esto según la página activa
        context['seccion'] = 'extranjerosa'  # Cambia esto según la página activa
        context['nombre_estacion'] = self.request.user.estancia.nombre
        extranjeros_ids = [extranjero.id for extranjero in context['extranjeros']]
        context['extranjeros_ids'] = extranjeros_ids
        # Agregar una lista de IDs de extranjeros al contexto
        return context
    
class creaAlegato(LoginRequiredMixin,CreateView):
    template_name = 'alegato/crearAlegato.html'
    model = Alegatos
    form_class = AlegatosForms
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Alegato creado con éxito.')
        return reverse('listaExtranjerosAlegatos')
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['lugarEmision'] = estacion
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_no_proceso = extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup      
        initial['nup'] = ultimo_no_proceso_id
        initial['extranjero'] = extranjero
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=extranjero_id)
        nombre = extranjero.nombreExtranjero
        ape1 = extranjero.apellidoPaternoExtranjero
        ape2 = extranjero.apellidoMaternoExtranjero
        context['nombre'] = nombre
        context['extranjero'] = extranjero
        context['ape1'] = ape1
        context['ape2'] = ape2
        context['navbar'] = 'medico'
        context['seccion'] = 'interno'    
        context['extranjero_id']= extranjero_id 
        return context

class subirDocumentosAlegatos(LoginRequiredMixin, CreateView, HandleFileMixin):
    template_name = 'alegato/subirDocumentos.html'
    model = DocumentosAlegatos
    form_class = DocumentosAlegatosForms
    login_url = '/permisoDenegado/'
    def get_success_url(self):
        messages.success(self.request, 'Documentos subidos con éxito.')
        return reverse('listaExtranjerosAlegatos')
    def get_initial(self):
        initial = super().get_initial()

        # Obtén el ID de la referencia y establece el valor inicial del campo deReferencia
        alegato_id = self.kwargs.get('alegato_id')
        alegato = get_object_or_404(Alegatos, id=alegato_id)
        extranjero = alegato.extranjero.pk
        ultimo_no_proceso = alegato.extranjero.noproceso_set.latest('consecutivo')
        ultimo_no_proceso_id = ultimo_no_proceso.nup  
        initial['extranjero']= extranjero    
        initial['nup'] = ultimo_no_proceso_id
        initial['delAlegato'] = alegato_id

        return initial
    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
        
        # Obtén el ID de la referencia
         alegato_id = self.kwargs.get('alegato_id')
         alegato = get_object_or_404(Alegatos, id=alegato_id)
         id = alegato.pk
         nombre = alegato.extranjero.nombreExtranjero
         ape1 = alegato.extranjero.apellidoPaternoExtranjero
         ape2 = alegato.extranjero.apellidoMaternoExtranjero
         context['nombre'] = nombre
         context['ape1'] = ape1
         context['ape2'] = ape2  
         context['navbar'] = 'alegatos'  # Cambia esto según la página activa
         context['seccion'] = 'extranjerosa'  # Cambia esto según la página activa    
         context['alegato_id'] = alegato_id  # Agrega el ID de la referencia al contexto
         context['alegato']= id

         return context
    def form_valid(self, form):
        instance = form.save()  
        self.handle_file(instance,'documento')
        return super(subirDocumentosAlegatos, self).form_valid(form)
    
class listaDocumentosAlegatos(LoginRequiredMixin, ListView):
    template_name = 'alegato/documentosAlegatos.html'
    model = DocumentosAlegatos
    context_object_name = 'documentos'
    login_url = '/permisoDenegado/'

    def get_queryset(self):
        extranjero_id = self.kwargs['pk']

        # Obtener el último NUP asociado al extranjero
        ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))['consecutivo__max']

        # Filtrar los documentos externos por el ID del extranjero y el último NUP
        queryset = DocumentosAlegatos.objects.filter(
            extranjero_id=extranjero_id,
            nup__consecutivo=ultimo_nup
        )

        return queryset

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     extranjero_id = self.kwargs['pk']
    
    # Filtra los documentos que están relacionados con la misma referencia médica
     documentos = DocumentosAlegatos.objects.filter(extranjero=extranjero_id)
     dd = documentos.last
     extranjero = Extranjero.objects.get(id=extranjero_id)
     nombre = extranjero.nombreExtranjero
     ape1 = extranjero.apellidoPaternoExtranjero
     ape2 = extranjero.apellidoMaternoExtranjero
     context['extranjero']=extranjero
     context['nombre'] = nombre
     context['ape1'] = ape1
     context['ape2'] = ape2
    # Obtener la referencia médica asociada a la consulta

     context['navbar'] = 'alegatos'  # Cambia esto según la página activa
     context['seccion'] = 'extranjerosa'
     return context