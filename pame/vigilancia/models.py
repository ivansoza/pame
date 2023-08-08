from django.db import models
from catalogos.models import Estacion
# Create your models here.

class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='Nacionalidad')
    Abreviatura = models.CharField(max_length=200,verbose_name='Abreviatura')
   
    def __str__(self) -> str:
        return '__all__'

class Genero(models.Model):
    genero = models.CharField(max_length=100,verbose_name='Genero')
    
    def __str__(self) -> str:
        return '__all__'

class OficioPuestaDisposicionINM(models.Model):
    numeroOficio = models.IntegerField(verbose_name='Numero Oficial')
    fechaOficio = models.DateField(verbose_name='Fecha de Oficio')
    puntoRevision = models.CharField(max_length=100, verbose_name='Punto de Revisión')
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estacion Migratoria', blank=True, null=True)
    nombreAutoridadSigna = models.CharField(max_length=100, verbose_name='Nombre de la Autoridad Asignada')
    cargoAutoridadSigna = models.CharField(max_length=100, verbose_name='Cargo de la Autoridad Asignada')
    oficioPuesta = models.FileField(verbose_name='Oficio Puesta')
    oficioComision = models.FileField(verbose_name='Oficio Comisión')
    def __str__(self):
        return self.numeroOficio
    

class ExtranjeroINM(models.Model):
    numeroOficio = models.ForeignKey(OficioPuestaDisposicionINM, on_delete=models.CASCADE)
    fechaRegistro = models.DateField(verbose_name='Fecha de Registro')
    horaRegistro = models.DateTimeField(verbose_name='Hora de Registro')
    numeroE = models.IntegerField(verbose_name='Numero')
    nombreE = models.CharField(max_length= 50, verbose_name='Nombre')
    apellidoPaternoE = models.CharField(max_length=50, verbose_name='Apellido Paterno', blank=True)
    apellidoMaternoE = models.CharField(max_length=50, verbose_name='Apellido Materno', blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE, verbose_name='Nacionalidad')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, verbose_name='Genero')
    documentoIdentidad = models.FileField(verbose_name='Documento Identidad')
    fechaNacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    viajaSolo = models.BooleanField(verbose_name='¿Viaja solo?')

    def __str__(self) -> str:

        return self.nombreE


class OficioPuestaDisposicionAC(models.Model):
    numeroOficio = models.IntegerField(verbose_name='Numero Oficio')
    fechaOficio = models.DateField(verbose_name='Fecha Oficio')
    numeroCarpeta = models.CharField(max_length=30, verbose_name='Numero de Carpeta')
    estacion = models.ForeignKey(Estacion, verbose_name="Estacion Migratoria", on_delete=models.CASCADE, blank=True, null=True)
    dependencia = models.CharField(max_length=100, verbose_name='Dependencia')
    nombreAutoridadSigna = models.CharField(max_length=100, verbose_name='Nombre de la Autoridad Asignada' )
    cargoAutoridadSigna = models.CharField(max_length=100, verbose_name='Cargo de la Autoridad Asignada')
    entidadFederativa = models.CharField(max_length=100, verbose_name='Entidad Federativa')
    municipio = models.CharField(max_length=50, verbose_name='Municipio ', blank=True)
    localidad = models.CharField(max_length=50, verbose_name='Localidad ', blank=True)
    certificadoMedico = models.FileField(verbose_name='Certificado Medico', blank=True)
    oficioPuesta =models.FileField(verbose_name='Oficio Puesta',blank=True)
    oficioComision = models.FileField(verbose_name='Oficio Comisión', blank=True)
    
    
    
class ExtranjeroAC(models.Model):
    numeroOficio = models.ForeignKey(OficioPuestaDisposicionAC, on_delete=models.CASCADE)
    fechaRegistro = models.DateField(verbose_name='Fecha de Registro')
    horaRegistro = models.DateTimeField(verbose_name='Hora de Registro')
    numeroE = models.IntegerField(verbose_name='Numero')
    nombreE = models.CharField(max_length= 50, verbose_name='Nombre')
    apellidoPaternoE = models.CharField(max_length=50, verbose_name='Apellido Paterno', blank=True)
    apellidoMaternoE = models.CharField(max_length=50, verbose_name='Apellido Materno', blank=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE, verbose_name='Nacionalidad')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, verbose_name='Genero')
    documentoIdentidad = models.FileField(verbose_name='Documento Identidad')
    fechaNacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    viajaSolo = models.BooleanField(verbose_name='¿Viaja solo?')

    def __str__(self) -> str:

        return self.nombreE
    
OPCION_RELACION_CHOICES=[
    [0,'ESPOSO(A)'],
    [1,'HIJO(A)'],
    [2,'MADRE'],
    [3,'PADRE'],
    [4,'OTRO'],
]

class Acompanante(models.Model):
    delAcompañante = models.IntegerField(verbose_name='Numero del Acompañante', blank=True, null=True)
    nombreE = models.CharField(max_length= 50, verbose_name='Nombre', blank=True)
    apellidoPaternoE = models.CharField(max_length=50, verbose_name='Apellido Paterno', blank=True)
    apellidoMaternoE = models.CharField(max_length=50, verbose_name='Apellido Materno', blank=True)
    relacion = models.IntegerField(choices=OPCION_RELACION_CHOICES, verbose_name='Relación')
    delExtanjeroAC = models.ForeignKey(ExtranjeroAC, on_delete=models.CASCADE, null=True, blank=True)
    delExtanjeroINM = models.ForeignKey(ExtranjeroINM, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.nombreE
    