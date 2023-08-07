from django.db import models

from vigilancia.models import Extranjero
# Create your models here.

class ExpedienteMedico(models.Model):
    numeroE = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    fecha_consulta = models.DateField()
    sintomas = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField()