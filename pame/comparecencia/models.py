from django.db import models
from catalogos.models import Traductores
from vigilancia.models import Extranjero, NoProceso, AutoridadesActuantes
from catalogos.models import RepresentantesLegales

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

GRADOS_ACADEMICOS = [
    ('Doctorado', 'Doctorado'),
    ('Maestría', 'Maestría'),
    ('Licenciatura', 'Licenciatura'),
    ('Bachillerato', 'Bachillerato'),
    ('Diplomado', 'Diplomado'),
    ('Técnico', 'Técnico'),
    ('Secundaria', 'Secundaria'),
    ('Primaria', 'Primaria'),
    ('Sin educación formal', 'Sin educación formal'),
]
class Comparecencia(models.Model):
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE, related_name="comparecencias")
    fechahoraComparecencia = models.DateTimeField(auto_now_add=True)
    estadoCivil = models.CharField(max_length=50, blank=True, null=True, verbose_name="Estado Civil")
    escolaridad = models.CharField(max_length=50, blank=True, null=True, verbose_name="Escolaridad")
    ocupacion = models.CharField(max_length=50, blank=True, null=True, verbose_name="Ocupación")
    nacionalidad = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nacionalidad")
    DomicilioPais = models.CharField(max_length=50, blank=True, null=True, verbose_name="Domicilio en el País")
    lugarOrigen = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lugar de Origen")
    domicilioEnMexico = models.BooleanField(verbose_name="¿Domicilio en Mexico?", blank=True, null=True)
    nombrePadre = models.CharField(max_length=80, blank=True, null=True, verbose_name="Nombre(s) del Padre")
    nacionalidadPadre = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nacionalidad del Padre")
    nombreMadre = models.CharField(max_length=80, blank=True, null=True, verbose_name="Nombre(s) de la Madre")
    nacionalidadMadre = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nacionalidad de la Madre")
    fechaIngresoMexico= models.DateField(verbose_name="Fecha de Ingreso a Mexico")
    lugarIngresoMexico= models.CharField(max_length=50, verbose_name="Lugar de Ingreso a Mexico")
    formaIngresoMexico= models.CharField(max_length=50, verbose_name="Forma de Ingreso a Mexico")
    declaracion = models.TextField(verbose_name="Declaración")
    solicitaRefugio= models.BooleanField(verbose_name="¿Solicita Refugio?",  blank=True, null=True)
    victimaDelito= models.BooleanField(verbose_name="Es Victima de delito?", blank=True, null=True)
    autoridadActuante=models.ForeignKey(AutoridadesActuantes,related_name='Autoridadactuante', on_delete=models.CASCADE, verbose_name='Autoridad', blank=True, null=True)
    representanteLegal = models.ForeignKey(RepresentantesLegales, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Representante Legal')
    traductor=models.ForeignKey(Traductores,related_name='Traductor', on_delete=models.CASCADE, verbose_name='Traductor', blank=True, null=True)
    testigo1=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 1")
    grado_academico_testigo1=models.CharField(verbose_name='Grado Académico del Testigo 1', max_length=50, choices=GRADOS_ACADEMICOS)
    testigo2=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 2")
    grado_academico_testigo2=models.CharField(verbose_name='Grado Académico del Testigo 2', max_length=50, choices=GRADOS_ACADEMICOS)


class FirmaCompareciencia(models.Model):
    compareciencia = models.ForeignKey(Comparecencia, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaRepresentanteLegal = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTraductor= models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaExtranjero= models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo1= models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo2= models.ImageField(upload_to='files/', null=True, blank=True) 

class Refugio(models.Model):
    notificacionComar= models.TextField()
    fechaNotificacion= models.DateField()
    delExtranjero= models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    contstanciaAdmisnion = models.CharField(max_length=100)
    acuerdoSuspension = models.CharField(max_length=100)
        
class VictimaDelito(models.Model):
    notificacionAutoridad = models.TextField()
    fechaNotificacion= models.DateField()
    delExtranjero= models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    documentoMigratorio = models.CharField(max_length=100)
    asunto = models.TextField()
    documentoFGR = models.CharField(max_length=100)

class Consular(models.Model):
    lugar= models.CharField(max_length=50)
    fechaNotificacionConsular= models.DateField()
    horaNotificacionConsular = models.DateTimeField()
    consulado= models.CharField(max_length=50)
    tipoResolucion = models.CharField(max_length=50)
    delExtranjero= models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    numeroOficio = models.CharField(max_length=50)
    asunto = models.TextField() 
    