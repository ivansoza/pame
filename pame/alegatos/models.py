from django.db import models
from vigilancia.models import Extranjero, NoProceso
from catalogos.models import Estacion, AutoridadesActuantes, RepresentantesLegales
# Create your models here.
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
class Alegatos(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    lugarEmision = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Lugar Emisión')
    fechaHora = models.DateTimeField(auto_now_add=True)
    autoridadActuante = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name='Autoridad actuante')
    repreLegal = models.ForeignKey(RepresentantesLegales, on_delete=models.CASCADE, verbose_name='Representante Legal')
    testigo1=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 1")
    grado_academico_testigo1=models.CharField(verbose_name='Grado Académico del Testigo 1', max_length=50, choices=GRADOS_ACADEMICOS)
    testigo2=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 2")
    grado_academico_testigo2=models.CharField(verbose_name='Grado Académico del Testigo 2', max_length=50, choices=GRADOS_ACADEMICOS)
    def __str__(self):
        return f'{self.extranjero} {self.autoridadActuante}'
    class Meta:
        verbose_name_plural = "Alegatos"

class DocumentosAlegatos(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    delAlegato = models.ForeignKey(Alegatos, on_delete=models.CASCADE)
    fechaHora = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(verbose_name='Descripción del documento')
    documento = models.FileField(upload_to='files/', verbose_name='Documento', null=True, blank=True)
    eleccion = models.BooleanField()
    def __str__(self):
        return f'{self.descripcion} {self.documento}'
    class Meta:
        verbose_name_plural = " Documentos Alegatos"

class presentapruebas(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    fechaHora = models.DateTimeField(auto_now_add=True)
    presenta = models.BooleanField()
    def __str__(self):
        return f'{self.extranjero.nombreExtranjero} {self.nup}'


class FirmaAlegato(models.Model):
    alegato = models.ForeignKey(Alegatos, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaRepresentanteLegal = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo1= models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo2= models.ImageField(upload_to='files/', null=True, blank=True) 

class NoFirma(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    lugarEmision = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Lugar Emisión')
    fechaHora = models.DateTimeField(auto_now_add=True)
    autoridadActuante = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name='Autoridad actuante')
    repreLegal = models.ForeignKey(RepresentantesLegales, on_delete=models.CASCADE, verbose_name='Representante Legal')
    testigo1=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 1")
    grado_academico_testigo1=models.CharField(verbose_name='Grado Académico del Testigo 1', max_length=50, choices=GRADOS_ACADEMICOS)
    testigo2=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 2")
    grado_academico_testigo2=models.CharField(verbose_name='Grado Académico del Testigo 2', max_length=50, choices=GRADOS_ACADEMICOS)
    descripcion = models.TextField(verbose_name='Breve descripción del contenido a notificar')


class FirmasConstanciaNoFirma(models.Model):
    constancia = models.ForeignKey(NoFirma, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaRepresentanteLegal = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo1= models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo2= models.ImageField(upload_to='files/', null=True, blank=True) 

