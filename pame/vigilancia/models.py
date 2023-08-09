from django.db import models
from catalogos.models import Estacion
# Create your models here.

class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='Nacionalidad')
    Abreviatura = models.CharField(max_length=200,verbose_name='Abreviatura')
    
    class Meta:
        verbose_name_plural = "Nacionalidades"

# Create your models here.
class TipoDisposicion(models.Model):
    numero = models.IntegerField()
    descripcion = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = "Tipos de Disposiciones"

class PuestaDisposicion(models.Model):
    numeroOficio = models.CharField(max_length=50)
    fechaOficio = models.DateField()
    nombreAutoridadSigna = models.CharField(max_length=100)
    cargoAutoridadSigna = models.CharField(max_length=100)
    oficioPuesta = models.BinaryField()
    oficioComision = models.BinaryField()
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    deLadisposicion = models.ForeignKey(TipoDisposicion, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Puestas Disposición"
   
OPCION_GENERO_CHOICES=[
    [0,'HOMBRE'],
    [1,'MUJER'],
]
class Extranjero(models.Model):
    fechaRegistro = models.DateField()
    horaRegistro = models.DateTimeField(blank=True)
    numeroExtranjero = models.IntegerField(blank=True, null=True)
    estacionMigratoria = models.CharField(max_length=50,blank=True)
    nombreExtranjero = models.CharField(max_length= 50, blank=True)
    apellidoPaternoExtranjero = models.CharField(max_length=50, blank=True)
    apellidoMaternoExtranjero = models.CharField(max_length=50, blank=True)
    firmaExtranjero = models.BinaryField(blank=True)
    huellaExtranjero = models.BinaryField(blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    genero = models.IntegerField(choices=OPCION_GENERO_CHOICES)
    fechaNacimiento = models.DateField()
    documentoIdentidad = models.BinaryField(blank=True)
    fotografiaExtranjero = models.BinaryField(blank=True)
    viajaSolo = models.BooleanField()
    tipoEstancia = models.CharField(max_length=50, blank=True)
    deLaPuesta = models.ForeignKey(PuestaDisposicion, on_delete= models.CASCADE,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Extranjeros"

    
class ComplementoINM(models.Model):
    puntoRevision = models.CharField(max_length=100)
    deLaPuesta = models.ForeignKey(PuestaDisposicion, on_delete= models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Complemento INM"
    
 
     
class ComplementonAC(models.Model):
    dependencia = models.CharField(max_length=100)
    numeroCarpeta = models.CharField(max_length=30)
    entidadFederativa = models.CharField(max_length=100)
    certificadoMedico = models.BinaryField()
    deLaPuesta = models.ForeignKey(PuestaDisposicion, on_delete= models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Complemento AC"

OPCION_RELACION_CHOICES=[
    [0,'ESPOSO(A)'],
    [1,'HIJO(A)'],
    [2,'MADRE'],
    [3,'PADRE'],
    [4,'OTRO'],
]
class Acompanante(models.Model):
    delExtranjero = models.IntegerField()
    delAcompanante = models.ForeignKey(Extranjero, on_delete=models.CASCADE, blank=True, null=True)
    relacion = models.IntegerField(choices=OPCION_RELACION_CHOICES)

    class Meta:
        verbose_name_plural = "Acompañantes"