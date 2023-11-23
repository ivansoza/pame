from django.db import models
from vigilancia.models import Extranjero,NoProceso  # Asegúrate de importar el modelo Extranjero correctamente
from vigilancia.models import Estancia
from catalogos.models import AutoridadesActuantes, Consulado, Estacion

ACCION= (
    ('Deportacion', 'DEPORTACION'),
    ('Retorno_Asistido', 'RETORNO ASISTIDO'),
)
class Notificacion(models.Model):

    ESTATUS_PENDIENTE = 'pendiente'
    ESTATUS_ACEPTADO = 'aceptado'
    ESTATUS_RECHAZADO = 'rechazado'
    ESTATUS_EN_PROCESO = 'en_proceso'

    # Define una lista de opciones que se usarán en el campo 'choices'
    ESTATUS_CHOICES = [
        (ESTATUS_PENDIENTE, 'Pendiente'),
        (ESTATUS_ACEPTADO, 'Aceptado'),
        (ESTATUS_RECHAZADO, 'Rechazado'),
        (ESTATUS_EN_PROCESO, 'En proceso'),
    ]
    fecha_aceptacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Aceptación')
    numero_proceso = models.ForeignKey(NoProceso,on_delete=models.CASCADE,verbose_name='Número de Proceso Asociado',related_name='notificaciones')
    estacion = models.ForeignKey(Estacion,on_delete=models.CASCADE,verbose_name='Estación de Notificación')
    descripcion = models.TextField(verbose_name='Descripción',blank=True,null=True)
    estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES,verbose_name='Estatus de la Notificación',blank=True,null=True,default=ESTATUS_PENDIENTE)

    def __str__(self):
        return f"Notificación del proceso {self.numero_proceso} en {self.estacion.nombre}"

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    
ACCION= (
    ('Deportacion', 'DEPORTACION'),
    ('Retorno_Asistido', 'RETORNO ASISTIDO'),
)
class NotificcionConsular(models.Model):
    delaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name="Estación")
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name="Numero de Proceso")
    fechaNotificacion= models.DateField(auto_now_add=True)
    horaNotificacion = models.DateTimeField(auto_now_add=True)
    numeroOficio = models.CharField(max_length=50, verbose_name="Numero de Oficio")
    delConsulado = models.ForeignKey(Consulado, on_delete=models.CASCADE, verbose_name="Consulado")
    accion = models.CharField(max_length=50, choices= ACCION, verbose_name="Acción")
    delaAutoridad = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name="Autoridad Actuante")

class FirmaAcuerdo(models.Model):
    notificacionConsular = models.ForeignKey(NotificcionConsular, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True, verbose_name="Firma de la Autoridad Actuante") #Ubicacion de archivos/imagenes()

    
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