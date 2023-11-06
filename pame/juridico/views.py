from django.shortcuts import render
from django.views.generic import CreateView, ListView, TemplateView
from vigilancia.models import Extranjero, PuestaDisposicionINM, Biometrico, PuestaDisposicionAC, PuestaDisposicionVP, NoProceso
from django.shortcuts import redirect
from .models import NotificacionDerechos
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import face_recognition
from io import BytesIO
import numpy as np
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages
from acuerdos.models import NotificacionesGlobales
from acuerdos.models import Documentos
from acuerdos.views import guardar_derechoObligaciones_pdf
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def homeJuridicoGeneral(request):
    return render (request, "home/homeJuridicoGeneral.html")


def homeJuridico(request):
    return render (request, "/home/homeJuridico.html")

def homeJuridicoResponsable(request):
    return render (request, "home/homeJuridicoResponsable.html")

class notificacionDO(LoginRequiredMixin,TemplateView):
    template_name ='home/notificacion_d_o.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def post(self, request, *args, **kwargs):
        try:
            extranjero_id = self.kwargs['extranjero_id']
            extranjero = Extranjero.objects.get(pk=extranjero_id)
            estacion = extranjero.deLaEstacion

            # Usando el método para obtener el último NoProceso
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()

            # Solo crea la Notificacion si hay un NoProceso asociado
            if ultimo_nup:
                NotificacionDerechos.objects.create(no_proceso=ultimo_nup, estacion=estacion)
            
            guardar_derechoObligaciones_pdf(extranjero_id, request.user)
            messages.success(request, 'Notificación y PDF creados exitosamente.')
            return redirect('listarExtranjeros', puesta_id=self.kwargs.get('puesta_id'))

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('notificacionDO', extranjero_id=extranjero_id)
        


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
        try:
            documento = Documentos.objects.get(nup=ultimo_nup)
            context['oficio_derechos_obligaciones'] = documento.oficio_derechos_obligaciones
        except Documentos.DoesNotExist:
            context['oficio_derechos_obligaciones'] = None

        extranjero_id = self.kwargs['extranjero_id']
     # Obtener la instancia del Extranjero correspondiente
        extrannjero = Extranjero.objects.get(pk=extranjero_id)
        if extranjero.apellidoMaternoExtranjero:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero + " " + extranjero.apellidoMaternoExtranjero
        else:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero
    
        estacion = extrannjero.deLaEstacion.responsable
        responsable = estacion.nombre+" "+estacion.apellidoPat+" "+estacion.apellidoMat
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionINM.objects.get(id=puesta_id)
        context['extranjero']= extrannjero
        context['nombreCompleto']= nombre_completo
        context['responsable']=responsable
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadINM'  # Cambia esto según la página activa
        return context
    
class notificacionDOAC(LoginRequiredMixin,TemplateView):
    template_name ='notificacionDOAC.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def post(self, request, *args, **kwargs):
        try:
            extranjero_id = self.kwargs['extranjero_id']
            extranjero = Extranjero.objects.get(pk=extranjero_id)
            estacion = extranjero.deLaEstacion

            # Usando el método para obtener el último NoProceso
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()

            # Solo crea la Notificacion si hay un NoProceso asociado
            if ultimo_nup:
                NotificacionDerechos.objects.create(no_proceso=ultimo_nup, estacion=estacion)
            guardar_derechoObligaciones_pdf(extranjero_id, request.user)
            messages.success(request, 'Notificación y PDF creados exitosamente.')
            return redirect('listarExtranjeroAC', puesta_id=self.kwargs.get('puesta_id'))

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('notificacionDOAC', extranjero_id=extranjero_id)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
        try:
            documento = Documentos.objects.get(nup=ultimo_nup)
            context['oficio_derechos_obligaciones'] = documento.oficio_derechos_obligaciones
        except Documentos.DoesNotExist:
            context['oficio_derechos_obligaciones'] = None

        extranjero_id = self.kwargs['extranjero_id']
     # Obtener la instancia del Extranjero correspondiente
        extrannjero = Extranjero.objects.get(pk=extranjero_id)
        if extranjero.apellidoMaternoExtranjero:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero + " " + extranjero.apellidoMaternoExtranjero
        else:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero
    
        estacion = extrannjero.deLaEstacion.responsable
        responsable = estacion.nombre+" "+estacion.apellidoPat+" "+estacion.apellidoMat
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionAC.objects.get(id=puesta_id)
        context['extranjero']= extrannjero
        context['nombreCompleto']= nombre_completo
        context['responsable']=responsable
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadAC'  # Cambia esto según la página activa
        return context
    
class notificacionDOVP(LoginRequiredMixin,TemplateView):
    template_name ='notificacionDOVP.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def post(self, request, *args, **kwargs):
        try:
            extranjero_id = self.kwargs['extranjero_id']
            extranjero = Extranjero.objects.get(pk=extranjero_id)
            estacion = extranjero.deLaEstacion
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
            if ultimo_nup:
                NotificacionDerechos.objects.create(no_proceso=ultimo_nup, estacion=estacion)
                
            guardar_derechoObligaciones_pdf(extranjero_id, request.user)
            messages.success(request, 'Notificación y PDF creados exitosamente.')
            return redirect('listarExtranjerosVP', puesta_id=self.kwargs.get('puesta_id'))

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('notificacionDOVP', extranjero_id=extranjero_id, puesta_id=self.kwargs.get('puesta_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
        try:
            documento = Documentos.objects.get(nup=ultimo_nup)
            context['oficio_derechos_obligaciones'] = documento.oficio_derechos_obligaciones
        except Documentos.DoesNotExist:
            context['oficio_derechos_obligaciones'] = None

        extranjero_id = self.kwargs['extranjero_id']
     # Obtener la instancia del Extranjero correspondiente
        extrannjero = Extranjero.objects.get(pk=extranjero_id)
         
        if extranjero.apellidoMaternoExtranjero:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero + " " + extranjero.apellidoMaternoExtranjero
        else:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero
    
        estacion = extrannjero.deLaEstacion.responsable
        responsable = estacion.nombre+" "+estacion.apellidoPat+" "+estacion.apellidoMat
        puesta_id = self.kwargs.get('puesta_id')
        context['puesta']=PuestaDisposicionVP.objects.get(id=puesta_id)
        context['extranjero']= extrannjero
        context['nombreCompleto']= nombre_completo
        context['responsable']=responsable
        context['navbar'] = 'seguridad'  # Cambia esto según la página activa
        context['seccion'] = 'seguridadVP'  # Cambia esto según la página activa
        return context

class notificacionDOGeneral(LoginRequiredMixin,TemplateView):
    template_name ='notificacionGeneralDO.html'
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    def post(self, request, *args, **kwargs):
        try:
            extranjero_id = self.kwargs['extranjero_id']
            extranjero = Extranjero.objects.get(pk=extranjero_id)
            estacion = extranjero.deLaEstacion

            # Usando el método para obtener el último NoProceso
            ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()

            # Solo crea la Notificacion si hay un NoProceso asociado
            if ultimo_nup:
                NotificacionDerechos.objects.create(no_proceso=ultimo_nup, estacion=estacion)
                
            guardar_derechoObligaciones_pdf(extranjero_id, request.user)
            messages.success(request, 'Notificación y PDF creados exitosamente.')
            estatus = extranjero.estatus
            if estatus == "Trasladado":
              return redirect('listTrasladados')
            else:
              return redirect('listarExtranjerosEstacion')

        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return redirect('notificacionGeneralDO', extranjero_id=extranjero_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extranjero_id = self.kwargs['extranjero_id']
        extranjero = Extranjero.objects.get(pk=extranjero_id)
        ultimo_nup = extranjero.noproceso_set.order_by('-consecutivo').first()
        try:
            documento = Documentos.objects.get(nup=ultimo_nup)
            context['oficio_derechos_obligaciones'] = documento.oficio_derechos_obligaciones
        except Documentos.DoesNotExist:
            context['oficio_derechos_obligaciones'] = None

        extranjero_id = self.kwargs['extranjero_id']
     # Obtener la instancia del Extranjero correspondiente
        extrannjero = Extranjero.objects.get(pk=extranjero_id)
        if extranjero.apellidoMaternoExtranjero:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero + " " + extranjero.apellidoMaternoExtranjero
        else:
            nombre_completo = extranjero.nombreExtranjero +" "+ extranjero.apellidoPaternoExtranjero
    
        estacion = extrannjero.deLaEstacion.responsable
        responsable = estacion.nombre+" "+estacion.apellidoPat+" "+estacion.apellidoMat
        estatus = extranjero.estatus
        if estatus == "Trasladado":
         context['seccion'] = 'trasladados'
        else:
         context['seccion'] = 'verextranjero'
        context['extranjero']= extrannjero
        context['nombreCompleto']= nombre_completo
        context['responsable']=responsable
        context['navbar'] = 'extranjeros'  # Cambia esto según la página activa
        return context
    
@csrf_exempt
def manejar_imagen(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        extranjero_id_str = request.POST.get('extranjero_id')
       

        if extranjero_id_str is None or not extranjero_id_str.isdigit():
            return JsonResponse({'error': 'Invalid llamada_id'}, status=400)

        extranjero_id = int(extranjero_id_str)

        try:
            biometrico = Biometrico.objects.get(Extranjero=extranjero_id)
            face_encoding_almacenado = biometrico.face_encoding

            # Conversion de la imagen subida
            imagen_bytes_io = BytesIO(imagen.read())
            imagen_pil = Image.open(imagen_bytes_io)

            if imagen_pil.mode != 'RGB':
                imagen_pil = imagen_pil.convert('RGB')

            imagen_array = np.array(imagen_pil)

            if not isinstance(imagen_array, np.ndarray):
                return JsonResponse({'error': 'Failed to load image'}, status=400)

            # Obteniendo los encodings de la imagen subida
            encodings_subido = face_recognition.face_encodings(imagen_array)

            if not encodings_subido:
                return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)

            uploaded_encoding = encodings_subido[0]
            tolerance = 0.5  # Puedes ajustar este valor

            distance = face_recognition.face_distance([face_encoding_almacenado], uploaded_encoding)
            distance_value = float(distance[0])
            
            if distance_value < tolerance:
                similarity_str = f"Similitud: {(1 - distance_value) * 100:.2f}%"
                return JsonResponse({'match': True, 'similarity': similarity_str, 'distance': distance_value})
            else:
                return JsonResponse({'match': False, 'similarity': None, 'distance': distance_value})

        except Biometrico.DoesNotExist:
            return JsonResponse({'error': 'Biometrico does not exist for given extranjero_id'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def compare_faces(request):
    if request.method == "POST":
        imagen = request.FILES.get('image')
        extranjero_id_str = request.POST.get('extranjero_id')

        # Verifica si el extranjero_id es None o si no es un número válido
        if extranjero_id_str is None or not extranjero_id_str.isdigit():
            return JsonResponse({'error': 'Invalid extranjero_id'}, status=400)

        extranjero_id = int(extranjero_id_str)  # Convertir a entero
     
        try:
            # Obtener el objeto Biometrico asociado con el Extranjero_id
      # Debería ser un número entero válido
            biometrico = Biometrico.objects.get(Extranjero=extranjero_id)
            # ...

            # Cargar face_encoding almacenado
            face_encoding_almacenado = biometrico.face_encoding

            # Convertir imagen subida a formato que face_recognition puede entender
            imagen = face_recognition.load_image_file(InMemoryUploadedFile(imagen))

            # Obtener los encodings de la imagen subida
            encodings_subido = face_recognition.face_encodings(imagen)
            
            if not encodings_subido:  # Verificar que se detectaron rostros en la imagen subida
                return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)
            
            # Comparar face_encoding_subido con face_encoding_almacenado
            matches = face_recognition.compare_faces([face_encoding_almacenado], encodings_subido[0])
            
            # También puedes calcular la distancia si lo necesitas
            distance = face_recognition.face_distance([face_encoding_almacenado], encodings_subido[0])
            similarity = f"Similitud: {100 - distance[0]*100:.2f}%"
            
            return JsonResponse({'match': matches[0], 'similarity': similarity})
        
        except Biometrico.DoesNotExist:
            return JsonResponse({'error': 'Biometrico does not exist for given extranjero_id'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)