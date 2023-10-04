from django.db import models
from vigilancia.models import Extranjero


# Create your models here.


class UserFace(models.Model):
    nombreExtranjero = models.CharField(verbose_name='Nombre de Extranjero', max_length=50, blank=True)
    image = models.ImageField(upload_to='user_faces/')
    face_encoding = models.JSONField(blank=True, null=True)  #

    def __str__(self):
        return self.nombreExtranjero

class UserFace1(models.Model):
    extranjero = models.OneToOneField(
        Extranjero, on_delete=models.CASCADE,
        primary_key=True,
    )
    image = models.ImageField(upload_to='user_faces/', blank=True, null=True)
    face_encoding = models.JSONField(blank=True, null=True)  #

    def __str__(self):
        return str(self.extranjero.nombreExtranjero) 
