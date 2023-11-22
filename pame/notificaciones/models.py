from django.db import models
from vigilancia.models import Extranjero,NoProceso  # Asegúrate de importar el modelo Extranjero correctamente
from vigilancia.models import Estancia
from catalogos.models import Estacion

class Notificacion(models.Model):
    fechaAceptacion = models.DateField(verbose_name='Fecha de Aceptación', auto_now_add=True)
    no_proceso = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name='Número de Proceso Asociado', related_name='notificaciones_comaparecencia')
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación de Notificación')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    estatus_notificacion = models.CharField(max_length=50, verbose_name='Estatus de Notificación', blank=True, null=True)

    def __str__(self):
        return f"Notificación de {self.no_proceso.extranjero.nombreExtranjero} en {self.estacion.nombre}"
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

class Relacion(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    defensoria = models.ForeignKey(Defensorias, on_delete=models.CASCADE)
    fechaHora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f"{self.extranjero}"