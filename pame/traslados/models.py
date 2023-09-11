from django.db import models
from catalogos.models import Estacion
from vigilancia.models import Proceso, Extranjero


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
    

class SolicitudTraslado(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, verbose_name='Extranjero')
    estacion_origen = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='solicitudes_origen', verbose_name='Estación de Origen')
    estacion_destino = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='solicitudes_destino', verbose_name='Estación de Destino')
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente')
    
    # Agrega campos adicionales aquí
    motivo = models.TextField(verbose_name='Motivo del traslado', blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Solicitud')
    fecha_aceptacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Aceptación')
    
    class Meta:
        verbose_name_plural = "Solicitudes de Traslado"

    def __str__(self):
        return f'Solicitud de {self.extranjero} a {self.estacion_destino}'