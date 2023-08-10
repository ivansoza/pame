from django.db import models
from catalogos.models import Estacion

class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='Nacionalidad')
    Abreviatura = models.CharField(max_length=200,verbose_name='Abreviatura')
    
    class Meta:
        verbose_name_plural = "Nacionalidades"

class PuestaDisposicionINM(models.Model):
    numeroOficio = models.CharField(max_length=50)
    fechaOficio = models.DateField()
    nombreAutoridadSigna = models.CharField(max_length=100)
    cargoAutoridadSigna = models.CharField(max_length=100)
    oficioPuesta = models.FieldFile(upload_to='files')
    oficioComision = models.FieldFile(upload_to='files')
    puntoRevision = models.CharField(max_length=100)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Puestas a Disposición INM"

class PuestaDisposicionAC(models.Model):   
    numeroOficio = models.IntegerField()
    fechaOficio = models.DateField()
    nombreAutoridadSigna = models.CharField(max_length=100)
    cargoAutoridadSigna = models.CharField(max_length=100)
    oficioPuesta = models.FieldFile(upload_to='files')
    oficioComision = models.FieldFile(upload_to='files')
    puntoRevision = models.CharField(max_length=100)
    dependencia = models.CharField(max_length=100)
    numeroCarpeta = models.IntegerField()
    entidadFederativa = models.CharField(max_length=100)
    certificadoMedico = models.FieldFile(upload_to='files')
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Puestas a Disposicion AC"

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
    firmaExtranjero = models.FieldFile(upload_to='files')
    huellaExtranjero = models.FieldFile(upload_to='files')
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    genero = models.IntegerField(choices=OPCION_GENERO_CHOICES)
    fechaNacimiento = models.DateField()
    documentoIdentidad = models.FieldFile(upload_to='files')
    fotografiaExtranjero = models.FieldFile(upload_to='files')
    viajaSolo = models.BooleanField()
    tipoEstancia = models.CharField(max_length=50, blank=True)
    deLaPuesta = models.ForeignKey(PuestaDisposicionINM, on_delete= models.CASCADE,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Extranjeros" 

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