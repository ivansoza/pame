from django.db import models
from catalogos.models import Estacion

class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='Nacionalidad')
    Abreviatura = models.CharField(max_length=200,verbose_name='Abreviatura')
    
    class Meta:
        verbose_name_plural = "Nacionalidades"

<<<<<<< HEAD
class PuestaDisposicionINM(models.Model):
    numeroOficio = models.CharField(max_length=50)
    fechaOficio = models.DateField()
    nombreAutoridadSigna = models.CharField(max_length=100)
    cargoAutoridadSigna = models.CharField(max_length=100)
    oficioPuesta = models.FileField(upload_to='files',  null=True, blank=True)
    oficioComision = models.FileField(upload_to='files',  null=True, blank=True)
    puntoRevision = models.CharField(max_length=100)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
=======
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
>>>>>>> origin/jose

    class Meta:
        verbose_name_plural = "Puestas a Disposición INM"

<<<<<<< HEAD
class PuestaDisposicionAC(models.Model):   
    numeroOficio = models.IntegerField()
    fechaOficio = models.DateField()
    nombreAutoridadSigna = models.CharField(max_length=100)
    cargoAutoridadSigna = models.CharField(max_length=100)
    oficioPuesta = models.FileField(upload_to='files',  null=True)
    oficioComision = models.FileField(upload_to='files',  null=True)
    puntoRevision = models.CharField(max_length=100)
    dependencia = models.CharField(max_length=100)
    numeroCarpeta = models.IntegerField()
    entidadFederativa = models.CharField(max_length=100)
    certificadoMedico = models.FileField(upload_to='files')
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
    firmaExtranjero = models.FileField(upload_to='files', null=True)
    huellaExtranjero = models.FileField(upload_to='files',  null=True)
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE)
    genero = models.IntegerField(choices=OPCION_GENERO_CHOICES)
    fechaNacimiento = models.DateField()
    documentoIdentidad = models.FileField(upload_to='files',  null=True)
    fotografiaExtranjero = models.FileField(upload_to='files',  null=True)
    viajaSolo = models.BooleanField()
    tipoEstancia = models.CharField(max_length=50, blank=True)
    deLaPuestaIMN = models.ForeignKey(PuestaDisposicionINM, on_delete= models.CASCADE,blank=True, null=True)
    deLaPuestaAC = models.ForeignKey(PuestaDisposicionAC, on_delete= models.CASCADE,blank=True, null=True)
    class Meta:
        verbose_name_plural = "Extranjeros" 
=======
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
>>>>>>> origin/jose

        return self.nombreE
    
OPCION_RELACION_CHOICES=[
    [0,'ESPOSO(A)'],
    [1,'HIJO(A)'],
    [2,'MADRE'],
    [3,'PADRE'],
    [4,'OTRO'],
]
class Acompanante(models.Model):
<<<<<<< HEAD
    delExtranjero = models.IntegerField()
    delAcompanante = models.ForeignKey(Extranjero, on_delete=models.CASCADE, blank=True, null=True)
    relacion = models.IntegerField(choices=OPCION_RELACION_CHOICES)

    class Meta:
        verbose_name_plural = "Acompañantes"
=======
    delAcompañante = models.IntegerField(verbose_name='Numero del Acompañante', blank=True, null=True)
    nombreE = models.CharField(max_length= 50, verbose_name='Nombre', blank=True)
    apellidoPaternoE = models.CharField(max_length=50, verbose_name='Apellido Paterno', blank=True)
    apellidoMaternoE = models.CharField(max_length=50, verbose_name='Apellido Materno', blank=True)
    relacion = models.IntegerField(choices=OPCION_RELACION_CHOICES, verbose_name='Relación')
    delExtanjeroAC = models.ForeignKey(ExtranjeroAC, on_delete=models.CASCADE, null=True, blank=True)
    delExtanjeroINM = models.ForeignKey(ExtranjeroINM, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.nombreE
    
>>>>>>> origin/jose
