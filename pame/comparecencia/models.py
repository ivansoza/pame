from django.db import models
from vigilancia.models import Extranjero

# Create your models here.
OPCION_ESTADOCIVIL_CHOICES=[
    [0,'Casado(a)'],
    [1,'Soltero(a)'],
    [2,'Viudo(a)'],
    [3,'Divorciado(a)'],
    [4, 'Separado(a)'],
]

OPCIONES_ESCOLARIDAD_CHOICES=[
    [0,'Presscolar'],
    [1, 'Primaria'],
    [2, 'Secundaria'],
    [3, 'Preparatoria'],
    [4, 'Universidad'],
]

class Comparecencia(models.Model):
    fechaComparecencia = models.DateField(verbose_name='Fecha Comparecencia')
    horaComparecencia = models.DateTimeField(verbose_name='Hora Comparecencia')
    estadoCivil = models.IntegerField(choices=OPCION_ESTADOCIVIL_CHOICES, verbose_name='Estado Civil')
    escolaridad = models.IntegerField(choices=OPCIONES_ESCOLARIDAD_CHOICES, verbose_name='Escolaridad')
    ocupacion = models.CharField(max_length=50, verbose_name='Ocupación')
    lugarOrigen =models.CharField(max_length=50, verbose_name='Lugar de Origen')
    calleDomicilioPais = models.CharField(max_length=50, verbose_name='Calle')
    numeroDomicilioPais = models.IntegerField(verbose_name='Numero')
    localidadPais = models.CharField(max_length=50, verbose_name='Localidad')
    domicilioEnMexico = models.BooleanField(verbose_name='Domicilio en México')
    nombrePadre = models.CharField(max_length=50, verbose_name='Nombre del Padre')
    apellidoPaternoPadre = models.CharField(max_length=50, verbose_name='Apellido Paterno del Padre')
    apellidoMaternoPadre = models.CharField(max_length=50, verbose_name='Apellido Materno del Padre')
    nombreMadre = models.CharField(max_length=50, verbose_name='Nombre de la Madre')
    apellidoPaternoMadre = models.CharField(max_length=50, verbose_name='Apellido Paterno de la Madre')
    apellidoMaternoMadre = models.CharField(max_length=50, verbose_name='Apellido Materno de la Madre')
    
    def __str__(self) -> str:
        return '__all__'