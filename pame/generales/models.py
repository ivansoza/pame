from django.db import models

# Create your models here.F
from django.db.models.signals import pre_save
from django.dispatch import receiver
import os


class ImagenCarrousel(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='carrousel/')
    descripcion = models.TextField()

    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name_plural = "Imágenes de Carrousel "
    

@receiver(pre_save, sender=ImagenCarrousel)
def eliminar_imagen_anterior(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = ImagenCarrousel.objects.get(id=instance.id)
            if old_instance.imagen != instance.imagen:
                # Eliminar la imagen anterior del sistema de archivos y del modelo
                eliminar_imagen(old_instance.imagen.path)
                old_instance.imagen.delete(save=False)
        except ImagenCarrousel.DoesNotExist:
            pass

def eliminar_imagen(ruta_imagen):
    # Verificar si la ruta de la imagen existe y eliminarla del sistema de archivos
    if os.path.isfile(ruta_imagen):
        os.remove(ruta_imagen)