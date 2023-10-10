from django.db import models

class Tipos(models.Model):
    tipo = models.CharField(max_length=50, null=False)

    def __str__(self) -> str:
        return self.tipo
    
    class Meta:
        verbose_name_plural = "Tipos"
    
class Estatus(models.Model):
    tipoEstatus = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return self.tipoEstatus
    
    class Meta:
        verbose_name_plural = "Estatus"
    
class Estado(models.Model):
    estado = models.CharField(max_length=50, null=False)

    def __str__(self) -> str:
        return self.estado

class Responsable(models.Model):
    nombre = models.CharField(max_length=50, null=False)
    apellidoPat = models.CharField(max_length=50, null=False)
    apellidoMat = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False)
    telefono = models.CharField(max_length=10, null=False)

    def __str__(self) -> str:
        return self.nombre
    

class Estacion(models.Model):
    identificador = models.CharField(max_length=10, null=False)
    nombre = models.CharField(max_length=50, null=False)
    calle = models.CharField(max_length=50, null=False)
    noext = models.CharField(max_length=5)
    noint = models.CharField(max_length=5, blank=True)
    colonia = models.CharField(max_length=50, null=False)
    cp = models.IntegerField(null=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    municipio =models.CharField(max_length=50)
    email = models.EmailField(max_length=254, null=False)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipos, on_delete=models.CASCADE)
    estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE)
    capacidad = models.IntegerField( null=False)
    servicioMedico = models.BooleanField(verbose_name='¿Cuenta con servicio medico?')
    
    def __str__(self) -> str:
        return self.nombre 
    
    class Meta:
        verbose_name_plural = "Estaciones"

class Salida(models.Model):
    tipoSalida = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.tipoSalida

class Estancia(models.Model):
    tipoEstancia = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.tipoEstancia

class Relacion(models.Model):
    tipoRelacion = models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.tipoRelacion