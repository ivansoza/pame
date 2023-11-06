# Importaciones de librerías estándar de Python
import os
import time
from io import BytesIO

# Importaciones de librerías externas
import cv2
import face_recognition
import numpy as np
from PIL import Image

# Importaciones de Django
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, DetailView

# Importaciones de formularios, modelos y demás elementos locales
from .forms import CompareFacesForm, UserFaceForm, SearchFaceForm, SearchFaceForm1
from .models import UserFace, UserFace1
from vigilancia.models import Biometrico
from django.contrib.auth.mixins import LoginRequiredMixin




def compare_faces(request):
    result = None
    similarity = None  # Para guardar la similitud (distancia)

    if request.method == "POST":
        form = CompareFacesForm(request.POST, request.FILES)
        if form.is_valid():
            image1 = form.cleaned_data['image1']
            image2 = form.cleaned_data['image2']

            # Convertir las imágenes a arrays
            img1_array = face_recognition.load_image_file(image1)
            img2_array = face_recognition.load_image_file(image2)

            # Obtener los encodings
            encodings1 = face_recognition.face_encodings(img1_array)
            encodings2 = face_recognition.face_encodings(img2_array)

            if encodings1 and encodings2:  # Verificar que se detectaron rostros
                matches = face_recognition.compare_faces([encodings1[0]], encodings2[0])
                result = matches[0]

                # Calcular la distancia (similitud)
                distance = face_recognition.face_distance([encodings1[0]], encodings2[0])
                similarity = f"Similitud: {100 - distance[0]*100:.2f}%"

            else:
                result = "No se detectó rostro en una o ambas imágenes."
    else:
        form = CompareFacesForm()

    return render(request, 'face/compare_faces.html', {'form': form, 'result': result, 'similarity': similarity})



class UserFaceCreateView(LoginRequiredMixin,CreateView):
    model = UserFace
    form_class = UserFaceForm
    template_name = 'face/guardar_fotos.html'
    success_url = reverse_lazy('create_user_face')
    login_url = '/permisoDenegado/'  # Reemplaza con tu URL de inicio de sesión

    
    def form_valid(self, form):
        form.instance.image.save(form.instance.image.name, form.instance.image, save=True)
        image_path = form.instance.image.path

        # Verificar si la imagen se ha guardado correctamente
        if os.path.exists(image_path):
            
            # Cargar la imagen
            image_array = face_recognition.load_image_file(image_path)
            
            # Obtener los encodings de la imagen
            face_encodings = face_recognition.face_encodings(image_array)
            
            if face_encodings:  # Verificar que se detectaron rostros
                encoding = face_encodings[0].tolist()
                
                # Guardar el encoding en el modelo y guardar el objeto en la base de datos
                self.object = form.save(commit=False)
                self.object.face_encoding = encoding
                self.object.save()
                
                return super().form_valid(form)
            # El 'else' se puede omitir si no es necesario manejar el caso de no detección de rostros
            
        # El 'else' se puede omitir si no es necesario manejar el caso de fallo al guardar la imagen

        return self.form_invalid(form)




def search_face(request):
    result = None
    
    if request.method == 'POST':
        form = SearchFaceForm(request.POST, request.FILES)
        
        if form.is_valid():
            start_time = time.time()  # Guarda el tiempo de inicio
            
            uploaded_image = form.cleaned_data['image']
            uploaded_image_array = face_recognition.load_image_file(uploaded_image)
            uploaded_encoding = face_recognition.face_encodings(uploaded_image_array)
            
            if not uploaded_encoding:  # Si no se detectó un rostro
                result = 'No se detectó rostro en la imagen subida.'
            else:
                uploaded_encoding = uploaded_encoding[0]  # Tomar el primer encoding si hay múltiples rostros
                
                for user_face in UserFace.objects.all():
                    saved_encoding = user_face.face_encoding  # El encoding guardado en el modelo
                    
                    if not saved_encoding:
                        continue  # Pasar al siguiente si no hay encoding
                    
                    distance = face_recognition.face_distance([saved_encoding], uploaded_encoding)
                    
                    if distance < 0.6:  # Puedes ajustar el umbral según tus necesidades
                        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                        result = (f'Coincidencia encontrada con {user_face.nombreExtranjero} '
                                  f'(Distancia: {distance[0]}). '
                                  f'Tiempo de búsqueda: {elapsed_time:.2f} segundos.')
                        break  # Salir del bucle si se encuentra una coincidencia
                else:  # Se ejecuta si no se rompió el bucle (no se encontró coincidencia)
                    elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                    result = f'No se encontraron coincidencias. Tiempo de búsqueda: {elapsed_time:.2f} segundos.'
    else:
        form = SearchFaceForm()
    
    return render(request, 'face/search_face.html', {'form': form, 'result': result})

def search_face1(request):
    result = None
    matched_image_url = None  # Inicializar con None
    
    if request.method == 'POST':
        form = SearchFaceForm(request.POST, request.FILES)
        
        if form.is_valid():
            start_time = time.time()  # Guarda el tiempo de inicio
            
            uploaded_image = form.cleaned_data['image']
            uploaded_image_array = face_recognition.load_image_file(uploaded_image)
            uploaded_encoding = face_recognition.face_encodings(uploaded_image_array)
            
            if not uploaded_encoding:  # Si no se detectó un rostro
                result = 'No se detectó rostro en la imagen subida.'
            else:
                uploaded_encoding = uploaded_encoding[0]  # Tomar el primer encoding si hay múltiples rostros
                
                for user_face1 in UserFace1.objects.all():
                    saved_encoding = user_face1.face_encoding  # El encoding guardado en el modelo
                
                    if not saved_encoding:
                        continue  # Pasar al siguiente si no hay encoding
                    
                    distance = face_recognition.face_distance([saved_encoding], uploaded_encoding)
                    
                    if distance < 0.4:  # Ajustar el umbral según tus necesidades
                        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                        result = (f'Coincidencia encontrada con {user_face1.extranjero} '
                                  f'(Distancia: {distance[0]}). '
                                  f'Tiempo de búsqueda: {elapsed_time:.2f} segundos.')
                        biometrico = Biometrico.objects.get(Extranjero=user_face1.extranjero)
                        matched_image_url = biometrico.fotografiaExtranjero.url if biometrico.fotografiaExtranjero else None
                        break  # Salir del bucle si se encuentra una coincidencia
                else:  # Se ejecuta si no se rompió el bucle (no se encontró coincidencia)
                    elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                    result = f'No se encontraron coincidencias. Tiempo de búsqueda: {elapsed_time:.2f} segundos.'
    else:
        form = SearchFaceForm1()
    
    return render(request, 'face/search_face1.html', {'form': form, 'result': result, 'matched_image_url': matched_image_url})



@csrf_exempt
def manejar_imagen(request):
    """
    Maneja las peticiones de imágenes para el reconocimiento facial. 
    """

    if request.method != "POST":
        # Retorna error si el método de la petición no es POST.
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Obtener la imagen y el ID extranjero de la petición.
    imagen = request.FILES.get('image')
    extranjero_id_str = request.POST.get('extranjero_id')

    # Validar el ID extranjero.
    if extranjero_id_str is None or not extranjero_id_str.isdigit():
        return JsonResponse({'error': 'Invalid extranjero_id'}, status=400)

    extranjero_id = int(extranjero_id_str)

    try:
        # Obtener el objeto biométrico asociado al ID extranjero.
        biometrico = Biometrico.objects.get(Extranjero=extranjero_id)
        face_encoding_almacenado = biometrico.face_encoding

        # Convertir la imagen subida a un formato adecuado.
        imagen_bytes_io = BytesIO(imagen.read())
        imagen_pil = Image.open(imagen_bytes_io)
        if imagen_pil.mode != 'RGB':
            imagen_pil = imagen_pil.convert('RGB')

        imagen_array = np.array(imagen_pil)
        if not isinstance(imagen_array, np.ndarray):
            return JsonResponse({'error': 'Failed to load image'}, status=400)

        # Obtener los encodings de la imagen subida.
        encodings_subido = face_recognition.face_encodings(imagen_array)
        if not encodings_subido:
            return JsonResponse({'error': 'No face detected in uploaded image'}, status=400)

        # Comparar los encodings obtenidos con los almacenados.
        uploaded_encoding = encodings_subido[0]
        tolerance = 0.5  # Puedes ajustar este valor según necesidad.
        distance = face_recognition.face_distance([face_encoding_almacenado], uploaded_encoding)
        distance_value = float(distance[0])

        # Retornar el resultado de la comparación.
        if distance_value < tolerance:
            similarity_str = f"Similitud: {(1 - distance_value) * 100:.2f}%"
            return JsonResponse({'match': True, 'similarity': similarity_str, 'distance': distance_value})
        else:
            return JsonResponse({'match': False, 'similarity': None, 'distance': distance_value})

    except Biometrico.DoesNotExist:
        return JsonResponse({'error': 'Biometrico does not exist for given extranjero_id'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def search_face2(request):
    result = None
    matched_image_url = None  # Inicializar con None
    
    if request.method == 'POST':
        form = SearchFaceForm1(request.POST, request.FILES)
        
        if form.is_valid():
            start_time = time.time()  # Guarda el tiempo de inicio
            
            uploaded_image = form.cleaned_data['image']
            uploaded_image_array = face_recognition.load_image_file(uploaded_image)
            uploaded_encoding = face_recognition.face_encodings(uploaded_image_array)
            
            if not uploaded_encoding:  # Si no se detectó un rostro
                result = 'No se detectó rostro en la imagen subida.'
            else:
                uploaded_encoding = uploaded_encoding[0]  # Tomar el primer encoding si hay múltiples rostros
                
                for user_face1 in UserFace1.objects.all():
                    saved_encoding = user_face1.face_encoding  # El encoding guardado en el modelo
                
                    if not saved_encoding:
                        continue  # Pasar al siguiente si no hay encoding
                    
                    distance = face_recognition.face_distance([saved_encoding], uploaded_encoding)
                    
                    if distance < 0.4:  # Ajustar el umbral según tus necesidades
                        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                        result = (f'Coincidencia encontrada con {user_face1.extranjero} '
                                  f'(Distancia: {distance[0]}). '
                                  f'Tiempo de búsqueda: {elapsed_time:.2f} segundos.')
                        biometrico = Biometrico.objects.get(Extranjero=user_face1.extranjero)
                        matched_image_url = biometrico.fotografiaExtranjero.url if biometrico.fotografiaExtranjero else None
                        break  # Salir del bucle si se encuentra una coincidencia
                else:  # Se ejecuta si no se rompió el bucle (no se encontró coincidencia)
                    elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
                    result = f'No se encontraron coincidencias. Tiempo de búsqueda: {elapsed_time:.2f} segundos.'
    else:
        form = SearchFaceForm1()
    
    return render(request, 'face/search_face1.html', {'form': form, 'result': result, 'matched_image_url': matched_image_url})  

    