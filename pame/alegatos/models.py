from django.db import models
from vigilancia.models import Extranjero, NoProceso
from catalogos.models import Estacion, AutoridadesActuantes, RepresentantesLegales
# Create your models here.
class Alegatos(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    lugarEmision = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Lugar Emisión')
    fechaHora = models.DateTimeField(auto_now_add=True)
    autoridadActuante = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name='Autoridad actuante')
    repreLegal = models.ForeignKey(RepresentantesLegales, on_delete=models.CASCADE, verbose_name='Representante Legal')
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
    def __str__(self):
        return f'{self.descripcion} {self.documento}'
    class Meta:
        verbose_name_plural = " Documentos Alegatos"

class presentapruebas(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    presenta = models.BooleanField()

class FirmaAlegato(models.Model):
    alegato = models.ForeignKey(Alegatos, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaRepresentanteLegal = models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo1= models.ImageField(upload_to='files/', null=True, blank=True) 
    firmaTestigo2= models.ImageField(upload_to='files/', null=True, blank=True) 