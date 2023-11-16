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
    def __str__(self):
        return (self.entidad)
    
    
class notificacionesAceptadas(models.Model):
    defensoria = models.ForeignKey(Defensorias, on_delete=models.CASCADE, related_name='archivos_pdf')
    archivo = models.FileField(upload_to='files/', verbose_name='Archivo PDF', blank=True, null=True)
    
    def __str__(self):
        return str(self.archivo)

