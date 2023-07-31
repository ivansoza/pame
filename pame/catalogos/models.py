from django.db import models


# Create your models here.
class Tipos(models.Model):
    tipo = models.CharField(max_length=50, null=False)

    def __str__(self) -> str:
        return self.tipo
    
class Estatus(models.Model):
    tipoEstatus = models.CharField(max_length=20, null=False)

    def __str__(self) -> str:
        return self.tipoEstatus
    
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
    noint = models.CharField(max_length=5, default='sn')
    colonia = models.CharField(max_length=50, null=False)
    cp = models.IntegerField(null=False)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, null=False)
    responsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipos, on_delete=models.CASCADE)
    estatus = models.ForeignKey(Estatus, on_delete=models.CASCADE)
    capacidad = models.IntegerField( null=False)
    
    def __str__(self) -> str:
        return self.identificador, self.nombre, self.estado,self.responsable, self.tipo, self.estatus, self.capacidad 
    
class User(models.Model):
    identificador = models.CharField(max_length=10, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellidoPat = models.CharField(max_length=50, null=False)
    apellidoMat = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=254, null=False)
    telefono = models.CharField(max_length=10, null=False)
    contasena = models.CharField(max_length=12, null=False)

    def __str__(self) -> str:
        return self.identificador, self.nombre
    
# genero=[

#     ("H","Hombre"),
#     ("M","Mujer"),
#     ("NB","No Binario"),
# ]
  

# edoCivil=[

#     ("H","Hombre"),
#     ("M","Mujer"),
#     ("NB","No Binario"),
# ]

class Extranjeros(models.Model):
    identificador = models.CharField(max_length=10, null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellidoPat = models.CharField(max_length=50, null=False)
    apellidoMat = models.CharField(max_length=50, null=False)
    edad = models.IntegerField(null=False)
    nacionalidad = models.CharField(max_length=50, null=False)
    fecha_nac = models.DateField(verbose_name="Fecha de Nacimiento")
    fecha_ing = models.DateField(verbose_name="Fecha de Ingreso")

    def __str__(self) -> str:
        return self.identificador, self.nombre, self.nacionalidad   