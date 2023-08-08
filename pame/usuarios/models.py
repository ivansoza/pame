from django.db import models
from django.contrib.auth.models import (AbstractUser)
from catalogos.models import Estacion
class Usuario(AbstractUser):
    estancia = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Usuarios"
    