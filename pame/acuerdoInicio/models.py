from django.db import models
from vigilancia.models import Extranjero

# Create your models here.
class TestigoUno (models.Model):
    nombreTestigoUno = models.CharField(max_length=50, verbose_name='Nombre del primer testigo')
    apellidoPaternoTestigoUno = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    apellidoMaternoTestigoUno = models.CharField(max_length=50, verbose_name='Apellido Materno')
    firmaTestigoUno = models.BinaryField(verbose_name='Firma')
    huellaTestigoUno = models.BinaryField(verbose_name='Huella')
    delExtanjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '__all__'

class TestigoDos (models.Model):
    nombreTestigoDos = models.CharField(max_length=50, verbose_name='Nombre del Segundo testigo')
    apellidoPaternoTestigoDos = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    apellidoMaternoTestigoDos = models.CharField(max_length=50, verbose_name='Apellido Materno')
    firmaTestigoDos = models.BinaryField(verbose_name='Firma')
    huellaTestigoDos = models.BinaryField(verbose_name='Huella')
    delExtanjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '__all__'
    
class Traductor (models.Model):
    nombreTraductor = models.CharField(max_length=50, verbose_name='Nombre(s)')
    apellidoPaternoTraductor = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    apellidoMaternoTraductor = models.CharField(max_length=50, verbose_name='Apellido Materno')
    delExtanjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return '__all__'