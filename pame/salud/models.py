from django.db import models


# Create your models here.

class ExpedienteMedico(models.Model):
    fecha_consulta = models.DateField()
    sintomas = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField()


    class Meta:
        verbose_name_plural = "Expedientes Medicos"