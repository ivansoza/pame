from django.db import models


class Defensorias(models.Model):
    entidad = models.CharField(max_length=50, verbose_name="Estado de la entidad")
    nombreTitular = models.CharField(max_length=50, verbose_name="Nombre del titular")
    apellidoPaternoTitular = models.CharField(max_length=50, verbose_name="Apellido paterno del titular")
    apellidoMaternoTitular = models.CharField(max_length=50, verbose_name="Apellido materno del titular")
    cargoTitular = models.CharField(max_length=50, verbose_name="Cargo del titular")
    email1 = models.CharField(max_length=50,verbose_name="Correo 1")
    email2 = models.CharField(max_length=50, verbose_name="Correo 2")
    telefono = models.CharField(max_length=20,verbose_name="Telefono")
    calle = models.CharField(max_length=50,verbose_name="Calle")
    colonia = models.CharField(max_length=50,verbose_name="Colonia")
    municipio = models.CharField(max_length=50,verbose_name="Municipio")
    cp = models.CharField(max_length=10,verbose_name="CP")

    def _str_(self):
        return self.__all__
