from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView
from .forms import AlegatosForms, DocumentosAlegatosForms, FirmaAutoridadActuanteForm1, FirmaRepresentanteLegalForm1, FirmaTestigoForm1, FirmaTestigo2Form1
from vigilancia.models import Extranjero, NoProceso
from .models import Alegatos, DocumentosAlegatos, FirmaAlegato
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from catalogos.models import Estacion, AutoridadesActuantes
from django.shortcuts import get_object_or_404, redirect
from generales.mixins import HandleFileMixin
from django.db.models import Max
from django.http import HttpResponse, HttpResponseNotFound
import qrcode
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.urls import reverse_lazy
from django.core.files.uploadedfile import InMemoryUploadedFile
import base64
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q

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
        for extranjero in context['extranjeros']:
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            tiene_alegato = False

            if ultimo_nup:
                prueba = Alegatos.objects.filter(nup=ultimo_nup).first()
                if prueba:
                    tiene_alegato = True
                    fecha =prueba.fechaHora
                    estacion = prueba.lugarEmision
                    context['fecha'] = fecha  # Cambia esto según la página activa
                    context['estacion'] = estacion  # Cambia esto según la página activa


            extranjero.tiene_alegato = tiene_alegato
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
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        nup_id = self.kwargs.get('pk')
        extranjero = Extranjero.objects.get(id=nup_id)
        
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

        return form
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
class modlaes(TemplateView):
    template_name='modal/modalfirma.html'
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     extranjero_id = self.kwargs['pk']
     ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))['consecutivo__max']

     ultimo_alegato = Alegatos.objects.filter(extranjero_id=extranjero_id, nup__consecutivo=ultimo_nup).order_by('-fechaHora').first()

     if ultimo_alegato:
            # Obtener el id del último alegato
            ultimo_alegato_id = ultimo_alegato.id
     else:
            # No hay alegatos asociados al último NUP
            ultimo_alegato_id = None
    # Filtra los documentos que están relacionados con la misma referencia médica
     documentos = DocumentosAlegatos.objects.filter(extranjero=extranjero_id)
     dd = documentos.last
     extranjero = Extranjero.objects.get(id=extranjero_id)
     nombre = extranjero.nombreExtranjero
     ape1 = extranjero.apellidoPaternoExtranjero
     ape2 = extranjero.apellidoMaternoExtranjero
     context['ale']=ultimo_alegato_id
     context['extranjero']=extranjero
     context['nombre'] = nombre
     context['ape1'] = ape1
     context['ape2'] = ape2
     self.request.session['alegato_id'] = ultimo_alegato_id

     
    # Obtener la referencia médica asociada a la consulta
     context['navbar'] = 'alegatos'  # Cambia esto según la página activa
     context['seccion'] = 'extranjerosa'
     return context
    
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
     ultimo_nup = NoProceso.objects.filter(extranjero_id=extranjero_id).aggregate(Max('consecutivo'))['consecutivo__max']

     ultimo_alegato = Alegatos.objects.filter(extranjero_id=extranjero_id, nup__consecutivo=ultimo_nup).order_by('-fechaHora').first()

     if ultimo_alegato:
            # Obtener el id del último alegato
            ultimo_alegato_id = ultimo_alegato.id
     else:
            # No hay alegatos asociados al último NUP
            ultimo_alegato_id = None
    # Filtra los documentos que están relacionados con la misma referencia médica
     documentos = DocumentosAlegatos.objects.filter(extranjero=extranjero_id)
     dd = documentos.last
     extranjero = Extranjero.objects.get(id=extranjero_id)
     nombre = extranjero.nombreExtranjero
     ape1 = extranjero.apellidoPaternoExtranjero
     ape2 = extranjero.apellidoMaternoExtranjero
     context['ale']=ultimo_alegato_id
     context['extranjero']=extranjero
     context['nombre'] = nombre
     context['ape1'] = ape1
     context['ape2'] = ape2
     self.request.session['alegato_id'] = ultimo_alegato_id

     
    # Obtener la referencia médica asociada a la consulta
     context['navbar'] = 'alegatos'  # Cambia esto según la página activa
     context['seccion'] = 'extranjerosa'
     return context
    
def generar_qr_firmas_alegato(request, alegato_id, tipo_firma):
    base_url = settings.BASE_URL

    if tipo_firma == "autoridadActuante":
        url = f"{base_url}alegatos/firma_autoridad_actuante_alegato/{alegato_id}/"
    elif tipo_firma == "representanteLegal":
        url = f"{base_url}alegatos/firma_representante_legal_alegato/{alegato_id}/"
    elif tipo_firma == "testigo1":
        url = f"{base_url}alegatos/firma_testigo1_alegato/{alegato_id}/"
    elif tipo_firma == "testigo2":
        url = f"{base_url}alegatos/firma_testigo2_alegato/{alegato_id}/"
    else:
        return HttpResponseBadRequest("Tipo de firma no válido")

    img = qrcode.make(url)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def firma_autoridad_actuante_alegato(request, alegato_id):
    alegato = get_object_or_404(Alegatos, pk=alegato_id)
    firma, created = FirmaAlegato.objects.get_or_create(alegato=alegato)  # Usar comparecencia aquí

    if firma.firmaAutoridadActuante:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    if request.method == 'POST':
        form = FirmaAutoridadActuanteForm1(request.POST, request.FILES)
        if form.is_valid():
            # Procesamiento similar para guardar la firma...
            data_url = form.cleaned_data['firmaAutoridadActuante']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaAutoridadActuante_{alegato_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaAutoridadActuante.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaAutoridadActuanteForm1()
    return render(request, 'firma/firma_autoridad_actuante_alegato1.html', {'form': form, 'alegato_id': alegato_id})

def firma_representante_legal_alegato(request, alegato_id):
    alegato = get_object_or_404(Alegatos, pk=alegato_id)
    firma, created = FirmaAlegato.objects.get_or_create(alegato=alegato)  # Usar comparecencia aquí
    if firma.firmaRepresentanteLegal:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaRepresentanteLegalForm1(request.POST, request.FILES)
        if form.is_valid():
        
            data_url = form.cleaned_data['firmaRepresentanteLegal']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaRepresentanteLegal_{alegato_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaRepresentanteLegal.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaRepresentanteLegalForm1()

    return render(request, 'firma/firma_representante_legal_alegato1.html', {'form': form, 'alegato_id': alegato_id})

def firma_testigo1_alegato(request, alegato_id):
    alegato = get_object_or_404(Alegatos, pk=alegato_id)
    firma, created = FirmaAlegato.objects.get_or_create(alegato=alegato)  # Usar colegamparecencia aquí
    if firma.firmaTestigo1:
        # Redirigir o manejar el caso de que la firma ya exista
        return redirect('firma_existente_acuerdos')
    
    if request.method == 'POST':
        form = FirmaTestigoForm1(request.POST, request.FILES)
        if form.is_valid():

            data_url = form.cleaned_data['firmaTestigo1']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]  # Ejemplo: "png"
            data = ContentFile(base64.b64decode(imgstr))
            
            file_name = f"firmaTestigo1_{alegato_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTestigo1.save(file_name, file, save=True)
            return redirect(reverse_lazy('firma_exitosa'))
    else:
        form = FirmaTestigoForm1()

    return render(request, 'firma/firma_testigo1_alegato.html', {'form': form, 'alegato_id': alegato_id})

def firma_testigo2_alojamiento(request, alegato_id):
    alegato = get_object_or_404(Alegatos, pk=alegato_id)
    firma, created = FirmaAlegato.objects.get_or_create(alegato=alegato)

    if firma.firmaTestigo2:
        return redirect('firma_existente_acuerdos')  # Asumiendo que tienes una URL para este caso

    if request.method == 'POST':
        form = FirmaTestigo2Form1(request.POST, request.FILES)
        if form.is_valid():
            # Código para procesar y guardar la firma
            data_url = form.cleaned_data['firmaTestigo2']
            format, imgstr = data_url.split(';base64,') 
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))

            file_name = f"firmaTestigo2_{alegato_id}.{ext}"
            file = InMemoryUploadedFile(data, None, file_name, 'image/' + ext, len(data), None)

            firma.firmaTestigo2.save(file_name, file, save=True)

            # Redireccionar a la página de firma exitosa
            return redirect(reverse_lazy('firma_exitosa'))  # Asegúrate de que esta URL esté definida
    else:
        form = FirmaTestigo2Form1()

    return render(request, 'firma/firma_testigo2_alegato.html', {'form': form, 'alegato_id': alegato_id})

@csrf_exempt
def verificar_firma_autoridad_actuante_alegato(request, alegato_id):
    try:
        firma = FirmaAlegato.objects.get(alegato=alegato_id)
        if firma.firmaAutoridadActuante:
            image_url = request.build_absolute_uri(firma.firmaAutoridadActuante.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma de la Autoridad Actuante encontrada',
                'image_url': image_url
            })
    except FirmaAlegato.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma de la Autoridad Actuante aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_representante_legal_alegato(request, alegato_id):
    try:
        firma = FirmaAlegato.objects.get(alegato=alegato_id)
        if firma.firmaRepresentanteLegal:
            image_url = request.build_absolute_uri(firma.firmaRepresentanteLegal.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Representante Legal encontrada',
                'image_url': image_url
            })
    except FirmaAlegato.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Representante Legal aún no registrada'}, status=404)

@csrf_exempt
def verificar_firma_testigo1_alegato(request, alegato_id):
    try:
        firma = FirmaAlegato.objects.get(alegato=alegato_id)
        if firma.firmaTestigo1:
            image_url = request.build_absolute_uri(firma.firmaTestigo1.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 1 encontrada',
                'image_url': image_url
            })
    except FirmaAlegato.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 1 aún no registrada'}, status=404)
@csrf_exempt
def verificar_firma_testigo2_alegato(request, alegato_id):
    try:
        firma = FirmaAlegato.objects.get(alegato=alegato_id)
        if firma.firmaTestigo2:
            image_url = request.build_absolute_uri(firma.firmaTestigo2.url)
            return JsonResponse({
                'status': 'success',
                'message': 'Firma del Testigo 2 encontrada',
                'image_url': image_url
            })
    except FirmaAlegato.DoesNotExist:
        pass

    return JsonResponse({'status': 'waiting', 'message': 'Firma del Testigo 2 aún no registrada'}, status=404)

def estado_firmas_alegato(request, alegato_id):
    # Obtener la instancia de Comparecencia, o devolver un error 404 si no se encuentra
    alegato = get_object_or_404(Alegatos, pk=alegato_id)

    # Obtener la instancia de FirmaComparecencia asociada a la Comparecencia
    firma = FirmaAlegato.objects.filter(alegato=alegato).first()

    # Si no existe una instancia de FirmaComparecencia, establecer todas las firmas como None
    if not firma:
        estado_firmas = {
            'firmaAutoridadActuante': None,
            'firmaRepresentanteLegal': None,
            'firmaTestigo1': None,
            'firmaTestigo2': None
        }
    else:
        # Crear un diccionario con el estado de cada firma (True si existe, False si no)
        estado_firmas = {
            'firmaAutoridadActuante': firma.firmaAutoridadActuante is not None,
            'firmaRepresentanteLegal': firma.firmaRepresentanteLegal is not None,
            'firmaTestigo1': firma.firmaTestigo1 is not None,
            'firmaTestigo2': firma.firmaTestigo2 is not None
        }

    # Devolver el estado de las firmas en formato JSON
    return JsonResponse(estado_firmas)
# Modifica tu vista verificarFirmas así
def verificar_firmas(request, alegato_id):
    try:
        alegato_firmas = FirmaAlegato.objects.filter(alegato_id=alegato_id).values('firmaAutoridadActuante', 'firmaRepresentanteLegal', 'firmaTestigo1', 'firmaTestigo2')
        
        firmas_existen = all(alegato_firma for alegato_firma in alegato_firmas[0].values())
        
        return JsonResponse({'firmas_existen': firmas_existen})
    except Exception as e:
        return JsonResponse({'error': str(e)})
