from django.db import models

# Create your models here.

class Nacionalidad(models.Model):
    nombre = models.CharField('Nacionalidad')
    Abreviatura = models.CharField(verbose_name='Abreviatura')

class Genero(models.Model):
    genero = models.CharField(verbose_name='Genero')

class Extranjero(models.Model):
    fechaRegistro = models.DateField(verbose_name='Fecha de Registro')
    horaRegistro = models.DateTimeField(verbose_name='Hora de Registro')
    numeroE = models.IntegerField(verbose_name='Numero')
    nombreE = models.CharField(max_length= 50, verbose_name='Nombre')
    apellidoPaternoE = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    apellidoMaternoE = models.CharField(max_length=50, verbose_name='Apellido Materno')
    firmaE = models.BinaryField(verbose_name='Firma')
    huellaE = models.BinaryField(verbose_name='Huella')
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE, verbose_name='Nacionalidad')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, verbose_name='Genero')
    fechaNacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    documentoIdentidad = models.BinaryField(verbose_name='Documento Identidad')
    fotografiaExtranjero = models.BinaryField(verbose_name='fotografia')
    viajaSolo = models.BooleanField(verbose_name='¿Viaja solo?')

    def __str__(self) -> str:
        return '__all__'
    
class OficioPuestaDisposicionINM(models.Model):
    numeroOficio = models.IntegerField(verbose_name='Numero Oficial')
    fechaOficio = models.DateField(verbose_name='Fecha de Oficio')
    nombreAutoridadSigna = models.CharField(max_length=100, verbose_name='Nombre de la Autoridad Asignada')
    cargoAutoridadSigna = models.CharField(max_length=100, verbose_name='Cargo de la Autoridad Asignada')
    puntoRevision = models.CharField(max_length=100, verbose_name='Punto de Revisión')
    oficioPuesta = models.BinaryField(verbose_name='Oficio Puesta')
    oficioComision = models.BinaryField(verbose_name='Ofisio Comisión')
    delExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, verbose_name='Numero del Extranjero')

    def __str__(self) -> str:
        return '__all__'
    
     
class OficioPuestaDisposicionAC(models.Model):
    numeroOficio = models.IntegerField(verbose_name='Numero Oficio')
    fechaOficio = models.DateField(verbose_name='Fecha Oficio')
    dependencia = models.CharField(max_length=100, verbose_name='Dependencia')
    numeroCarpeta = models.CharField(max_length=30, verbose_name='Numero de Carpeta')
    nombreAutoridadSigna = models.CharField(max_length=100, verbose_name='Nombre de la Autoridad Asignada' )
    cargoAutoridadSigna = models.CharField(max_length=100, verbose_name='Cargo de la Autoridad Asignada')
    entidadFederativa = models.CharField(max_length=100, verbose_name='Entidad Federativa')
    oficioPuesta =models.BinaryField(verbose_name='Oficio Puesta')
    certificadoMedico = models.BinaryField(verbose_name='Certificado Medico')
    delExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, verbose_name='Numero del Extranjero')

    def __str__(self) -> str:
        return '__all__'

class Acompanante(models.Model):
    delExtranjero = models.IntegerField(verbose_name='Numero del Acompañante')
    delAcompanante = models.ForeignKey(Extranjero, on_delete=models.CASCADE, verbose_name='Numero del Extranjero')
    relacion = models.CharField(max_length=30,verbose_name='Relación')

    def __str__(self) -> str:
        return '__all__'
    