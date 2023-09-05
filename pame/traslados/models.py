from django.db import models
from catalogos.models import Estacion
from vigilancia.models import Proceso

# Create your models here.

class Traslado(models.Model):
    numeroOficio = models.CharField(max_length=50, verbose_name='Numero de Oficio')
    fechaOficio = models.DateTimeField(verbose_name='Fecha de Oficio')
    estacionOrigen = models.CharField(max_length=50, verbose_name='Estación Origen')
    estacionDestino = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Estación Destino')
    estatus = models.CharField(max_length=50, verbose_name='Estatus')
    numeroUnicoProceso = models.ForeignKey(Proceso,on_delete=models.CASCADE, verbose_name='Numero Unico Proceso')

    def __str__(self):
        return self.numeroOficio