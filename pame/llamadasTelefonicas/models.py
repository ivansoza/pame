from django.db import models
from vigilancia.models import Extranjero

Desea_llamar_choices = [
    ('1', 'No'),
    ('2', 'Si'),
]

class llamadasTelefonicas(models.Model):
    noExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    estacionMigratoria = models.CharField(max_length=50)
    fechaHoraLlamada = models.DateTimeField()
    deseaLlamar = models.CharField(max_length=1, choices=Desea_llamar_choices)
    observaciones =  models.TextField(null=True, blank=True)
    motivo = models.TextField(null=True, blank=True)
    firmaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)
    huellaExtranjero = models.FileField(upload_to='files/', null=True, blank=True)