from django.db import models
from vigilancia.models import NoProceso, Estacion
# Create your models here.


class NotificacionDerechos(models.Model):
    fechaAceptacion = models.DateTimeField(verbose_name='Fecha de Aceptación', auto_now_add=True)
    no_proceso = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name='Número de Proceso Asociado', related_name='notificaciones_juridico')
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación de Notificación')
    
    # Campos adicionales que podrías necesitar en el futuro...
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    estatus_notificacion = models.CharField(max_length=50, verbose_name='Estatus de Notificación', blank=True, null=True)

    def __str__(self):
        return f"Notificación de {self.no_proceso.extranjero.nombreExtranjero} en {self.estacion.nombre}"