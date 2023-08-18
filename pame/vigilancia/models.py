from django.db import models
from catalogos.models import Estacion

class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='Nacionalidad')
    Abreviatura = models.CharField(max_length=200,verbose_name='Abreviatura')
    
    class Meta:
        verbose_name_plural = "Nacionalidades"
    
    def __str__(self):
        return self.nombre

class PuestaDisposicionINM(models.Model):
    numeroOficio = models.CharField(max_length=50)
    fechaOficio = models.DateField()
    nombreAutoridadSignaUno = models.CharField(max_length=100)
    cargoAutoridadSignaUno = models.CharField(max_length=100)
    nombreAutoridadSignaDos = models.CharField(max_length=100)
    cargoAutoridadSignaDos = models.CharField(max_length=100)
    oficioPuesta = models.FileField(upload_to='files/',  null=True, blank=True)
    oficioComision = models.FileField(upload_to='files/',  null=True, blank=True)
    puntoRevision = models.CharField(max_length=100)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Puestas a Disposición INM"

    def __str__(self):
        return self.numeroOficio
    
    @property
    def extranjeros(self):
        return self.extranjeros.all()
    

class PuestaDisposicionAC(models.Model):   
    numeroOficio = models.CharField(max_length=50)
    fechaOficio = models.DateField()
    nombreAutoridadSignaUno = models.CharField(max_length=100)
    cargoAutoridadSignaUno = models.CharField(max_length=100)
    nombreAutoridadSignaDos = models.CharField(max_length=100)
    cargoAutoridadSignaDos = models.CharField(max_length=100)
    oficioPuesta = models.FileField(upload_to='files/',  null=True, blank=True)
    oficioComision = models.FileField(upload_to='files/',  null=True, blank=True)
    puntoRevision = models.CharField(max_length=100)
    dependencia = models.CharField(max_length=100)
    numeroCarpeta = models.IntegerField()
    entidadFederativa = models.CharField(max_length=100)
    certificadoMedico = models.FileField(upload_to='files/',  null=True, blank=True)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name="Estación de origen", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Puestas a Disposicion AC"
    
    def __str__(self):
        return str(self.numeroOficio) 
    
    

OPCION_GENERO_CHOICES=[
    [0,'HOMBRE'],
    [1,'MUJER'],
]

class Extranjero(models.Model):
    fechaRegistro = models.DateField(auto_now_add=True)
    horaRegistro = models.DateTimeField(auto_now_add=True)
    numeroExtranjero = models.CharField(max_length=25, unique=True)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estacion de Origen', null=True, blank=True)
    nombreExtranjero = models.CharField(max_length= 50, blank=True)
    apellidoPaternoExtranjero = models.CharField(max_length=50, blank=True)
    apellidoMaternoExtranjero = models.CharField(max_length=50, blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE, verbose_name="Nacionalidad")
   
    genero = models.IntegerField(choices=OPCION_GENERO_CHOICES)
    fechaNacimiento = models.DateField()
    documentoIdentidad = models.FileField(upload_to='files/',  null=True,blank=True)
    
    viajaSolo = models.BooleanField(default=True)
    tipoEstancia = models.CharField(max_length=50, blank=True)
    deLaPuestaIMN = models.ForeignKey(PuestaDisposicionINM, on_delete= models.CASCADE,blank=True, null=True, related_name='extranjeros',verbose_name='Puesta')
    deLaPuestaAC = models.ForeignKey(PuestaDisposicionAC, on_delete= models.CASCADE,blank=True, null=True, related_name='extranjeros', verbose_name='Puesta')

    class Meta:
        verbose_name_plural = "Extranjeros" 
    def __str__(self):
         return self.nombreExtranjero
    
OPCION_RELACION_CHOICES=[
    [0,'ESPOSO(A)'],
    [1,'HIJO(A)'],
    [2,'MADRE'],
    [3,'PADRE'],
    [4,'OTRO'],
]
class Acompanante(models.Model):
    delExtranjero = models.CharField(max_length=200)
    delAcompanante = models.ForeignKey(Extranjero, on_delete=models.CASCADE, blank=True, null=True)
    relacion = models.IntegerField(choices=OPCION_RELACION_CHOICES)

    class Meta:
        verbose_name_plural = "Acompañantes"

class Biometrico(models.Model):
    Extranjero = models.OneToOneField(
        Extranjero, on_delete=models.CASCADE,
        primary_key=True,
    )
    fotografiaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    fechaHoraFotografia = models.DateTimeField(auto_now_add=True)
    huellaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    fechaHoraHuella = models.DateTimeField(auto_now_add=True)
    firmaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    fechaHoraFirma = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Biometricos'