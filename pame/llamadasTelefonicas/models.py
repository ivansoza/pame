from django.db import models
from vigilancia.models import Extranjero

Desea_llamar_choices = [
    ['No','no'],
    ['Si','si'],
]

class LlamadasTelefonicas(models.Model):
    noExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    estacionMigratoria = models.CharField(max_length=50)
    fechaHoraLlamada = models.DateTimeField(auto_now_add=True)
    deseaLlamar = models.CharField(max_length=2,choices=Desea_llamar_choices, default='Si')
    observaciones =  models.TextField(null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)
    firmaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    huellaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)

class Notificacion(models.Model):
    fechaHoraNotificacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora de la notificación')
    deseaLlamar = models.BooleanField(verbose_name='¿Desea Llamar?')
    motivoNoLlamada =  models.TextField(verbose_name='Motivo')
    firmaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    huellaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    delExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)

   
    