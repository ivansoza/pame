
from django.db import models

class PuestaGeneral(models.Model):
    numero_oficio = models.CharField(max_length=20)
    nombre_responsable = models.CharField(max_length=100)
    entidad = models.CharField(max_length=100)

class Complemento1(models.Model):
    puesta_general = models.OneToOneField(PuestaGeneral, on_delete=models.CASCADE)
    estado = models.CharField(max_length=100)

class Complemento2(models.Model):
    puesta_general = models.OneToOneField(PuestaGeneral, on_delete=models.CASCADE)
    municipio = models.CharField(max_length=100)
