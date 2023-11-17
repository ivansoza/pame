from django.shortcuts import render
from .forms import ResponsableForm, AutoridadesForms, AutoridadesActuantesForms, TraductoresForms, RepresentanteLegalForm, RepresentanteLegalStatusForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.urls import reverse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
# Create your views here.
from .models import Responsable, Autoridades, AutoridadesActuantes, Estacion, Traductores, RepresentantesLegales
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.shortcuts import redirect

from vigilancia.models import NoProceso, Extranjero, AsignacionRepresentante
from vigilancia.forms import AsignacionRepresentanteForm
from django.db.models import OuterRef, Subquery, Exists, Value
from django.contrib.auth.decorators import login_required 
from django.db.models.functions import Concat
from django.utils.text import format_lazy

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
        messages.success(self.request, 'Autoridad creada con éxito.')
        return reverse('listaAutoridad')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'autoridades'        
        return context
    
class editarAutoridad(UpdateView):
    template_name='Autoridades/editarAutoridades.html'
    model = Autoridades
    form_class = AutoridadesForms
    def get_success_url(self):
        messages.success(self.request, 'Datos de la autoridad editados con éxito.')
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
        context['actuantes'] = AutoridadesActuantes.objects.filter(estacion=user_estacion, estatus='Activo')
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
        
    
class listaTraductores(ListView):
    template_name = 'Traductores/listaTraductores.html'
    model = Traductores
    context_object_name ='traductores'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        context['estacion'] = estacion
        context['navbar'] = 'catalogos'
        context['seccion'] = 'traductores'        
        return context

class crearTraductor(CreateView):
    template_name = 'Traductores/crearTraductor.html'
    model = Traductores
    form_class = TraductoresForms
    def get_success_url(self):
        messages.success(self.request, 'Traductor agregado correctamente.')
        return reverse('listaTraductores')
    def get_initial(self):
        initial = super().get_initial()
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        initial['estacion'] = estacion
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'traductores'        
        return context
    
class editarTraductor(UpdateView):
    template_name='Traductores/editarTraductor.html'
    model = Traductores
    form_class = TraductoresForms
    def get_success_url(self):
        messages.success(self.request, 'Datos del traductor editados con éxito.')
        return reverse('listaTraductores')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['seccion'] = 'traductores'        
        return context

class editarEstatusActuante(UpdateView):
    template_name = 'Autoridades/estatusAutoridadActuante.html'
    model = AutoridadesActuantes
    form_class = AutoridadesActuantesForms
    def get_success_url(self):
        messages.success(self.request, 'Autoridad Actuante rebocada.')
        return reverse('agregaraAutoridadActuante')
    def get_initial(self):
        initial = super().get_initial()
        initial['estatus']='Inactivo'
        return initial
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['navbar'] = 'catalogos'
        context['seccion'] = 'actuantes'        
        return context
    

class RepresentantesLegalesListView(ListView):
    model = RepresentantesLegales
    template_name = 'Representantes/representantes_legales_list.html'  # Nombre del template que debes crear
    context_object_name = 'representantes_legales'  # Nombre del contexto en el template

    def get_queryset(self):
        user = self.request.user
        user_estacion = user.estancia
        return RepresentantesLegales.objects.filter(estacion=user_estacion)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        context['estacion'] = estacion
        context['navbar'] = 'catalogos'
        context['navbar1'] = 'representante'
        context['seccion'] = 'legal'
        context['seccion1'] = 'legales'
        return context
    
class RepresentanteLegalCreateView(CreateView):
    model = RepresentantesLegales
    form_class = RepresentanteLegalForm
    template_name = 'Representantes/representantes_legales_create.html'  # Nombre del template que debes crear
    success_url = reverse_lazy('representantes-legales-list')  # URL a la que redirigir después de un formulario válido

    def form_valid(self, form):
        form.instance.estacion = self.request.user.estancia  # Asigna la estación del usuario al representante legal
        messages.success(self.request, 'Representante legal creado con éxito.')

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        context['estacion'] = estacion
        context['navbar'] = 'catalogos'
        context['navbar1'] = 'representante'
        context['seccion'] = 'legal'
        context['seccion1'] = 'legales'
        return context
    
class RepresentanteLegalCreateViewComparecencia(CreateView):
    model = RepresentantesLegales
    form_class = RepresentanteLegalForm
    template_name = 'Representantes/representantes_legales_create_comparecencia.html'  # Nombre del template que debes crear
    success_url = format_lazy("{}?con_representante=no", reverse_lazy('lisExtranjerosComparecencia'))

    def form_valid(self, form):
        form.instance.estacion = self.request.user.estancia  # Asigna la estación del usuario al representante legal
        messages.success(self.request, 'Representante legal creado con éxito.')

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Usuario = get_user_model()
        usuario = self.request.user
        usuario_data = Usuario.objects.get(username=usuario.username)
        estacion_id = usuario_data.estancia_id
        estacion = Estacion.objects.get(pk=estacion_id)
        usuario_data = self.request.user 
        context['estacion'] = estacion
        context['navbar'] = 'catalogos'
        context['navbar1'] = 'representante'
        context['seccion'] = 'legal'
        context['seccion1'] = 'legales'
        return context
    
class RepresentanteLegalUpdateView(UpdateView):
    model = RepresentantesLegales
    form_class = RepresentanteLegalStatusForm
    template_name = 'Representantes/representantes_legales_update.html'  # Debes crear este template
    success_url = reverse_lazy('representantes-legales-list')  # Redirige aquí después de actualizar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Estatus de Representante Legal'
        context['representante_id'] = self.kwargs.get('pk')

        return context
    

class listExtranjerosRepresentantes(ListView):

    model = NoProceso
    template_name = 'Representantes/listExtranjerosRepresentante.html'
    context_object_name = "extranjeros"
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def get_queryset(self):
            estacion_usuario = self.request.user.estancia
            estado = self.request.GET.get('estado_filtrado', 'activo')

            con_representante = self.request.GET.get('con_representante')

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

            # Anotar con el ID de la asignación
            queryset = NoProceso.objects.filter(
                nup__in=[e.ultimo_nup_id for e in extranjeros_filtrados if e.ultimo_nup_id],
                extranjero__deLaEstacion=estacion_usuario
            ).annotate(
                tiene_asignacion=Exists(representantes_asignados),
                asignacion_id=Subquery(representantes_asignados.values('id')[:1]),
                nombre_representante=Subquery(
                representantes_asignados.annotate(
                    nombre_completo=Concat(
                        'representante_legal__nombre', Value(' '),
                        'representante_legal__apellido_paterno', Value(' '),
                        'representante_legal__apellido_materno'
                    )
                ).values('nombre_completo')[:1]
                )
            )

            if con_representante == 'si':
                queryset = queryset.filter(tiene_asignacion=True)
            elif con_representante == 'no':
                queryset = queryset.filter(tiene_asignacion=False)

            else:
                queryset = queryset.filter(tiene_asignacion=False)


            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar'] = 'catalogos'
        context['navbar1'] = 'representante'
        context['seccion'] = 'legal'
        context['seccion1'] = 'asignar'
        return context
    
class AsignacionRepresentanteCreateView(CreateView):
    model = AsignacionRepresentante
    form_class = AsignacionRepresentanteForm
    template_name = 'Representantes/asignar_representante.html'
    success_url = reverse_lazy('representante-legal-extranjeros')

    def form_valid(self, form):
            # Aquí capturas el `nup` desde la URL y lo asignas al objeto form.instance
            nup = self.kwargs.get('nup')
            form.instance.no_proceso = get_object_or_404(NoProceso, nup=nup)
            form.instance.estacion = self.request.user.estancia
            return super().form_valid(form)

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['estacion_usuario'] = self.request.user.estancia
            return kwargs
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            nup = self.kwargs.get('nup')
            context['nup'] = nup
            return context
    

class AsignacionRepresentanteComparecenciaCreateView(CreateView):
    model = AsignacionRepresentante
    form_class = AsignacionRepresentanteForm
    template_name = 'Representantes/asignar_representante_comparecencia.html'
    success_url = reverse_lazy('lisExtranjerosComparecencia')

    def form_valid(self, form):
            # Aquí capturas el `nup` desde la URL y lo asignas al objeto form.instance
            nup = self.kwargs.get('nup')
            form.instance.no_proceso = get_object_or_404(NoProceso, nup=nup)
            form.instance.estacion = self.request.user.estancia
            return super().form_valid(form)

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['estacion_usuario'] = self.request.user.estancia
            return kwargs
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            nup = self.kwargs.get('nup')
            context['nup'] = nup
            return context
    

class AsignacionRepresentanteUpdateView(UpdateView):
    model = AsignacionRepresentante
    form_class = AsignacionRepresentanteForm
    template_name = 'Representantes/editar_representante.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['estacion_usuario'] = self.request.user.estancia
        return kwargs
    def get_success_url(self):
        # Añadir parámetro de consulta al URL
        return reverse_lazy('representante-legal-extranjeros') + '?con_representante=si'

    def get_object(self, queryset=None):
        # Obtén el ID desde la URL
        asignacion_id = self.kwargs.get('id')
        # Busca y devuelve la AsignacionRepresentante asociada con este ID
        return get_object_or_404(AsignacionRepresentante, id=asignacion_id)

    def form_valid(self, form):
        # Aquí puedes añadir cualquier lógica adicional que necesites al guardar el formulario
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['asignacion_id'] = self.kwargs.get('id')

        # Agregar información adicional al contexto, si es necesario
        return context