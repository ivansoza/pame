from django.db import models
from catalogos.models import Estacion
from vigilancia.models import Proceso, Extranjero
from django import forms

# Create your models here.

OPCION_STATUS_CHOICES=[
    [0,'SOLICITUD'],
    [1,'ACEPTADO'],
    [2,'RECHAZADO'],
]

TRASLADO_STATUS_CHOICES = (
    (0, 'No iniciado'),  # No ha iniciado el traslado aún
    (1, 'Inicio del Traslado'),
    (2, 'En Traslado'),
    (3, 'Llegada'),
)

TIPO_TRASLADO_CHOICES = (
    (0, 'Por Resolución'),
    (1, 'Por Alojamiento'),
)

class Traslado(models.Model):
    numeroUnicoProceso = models.CharField(verbose_name="Numero Único de Proceso" ,max_length=50)
    estacion_origen = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='solicitudes_origen1', verbose_name='Estación de Origen')
    estacion_destino = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='solicitudes_destino1', verbose_name='Estación de Destino')
    fechaSolicitud = models.DateTimeField(auto_now_add=True)
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)  # Permitir null y blank ya que puede no haber sido aceptada aún
    fecha_traslado = models.DateTimeField(null=True, blank=True)  # Similar al anterior
    fecha_arrivo = models.DateTimeField(null=True, blank=True)  # S
    fecha_rechazo = models.DateTimeField(null=True, blank=True)  
    fecha_inicio = models.DateTimeField(null=True, blank=True)  
    fecha_llegada= models.DateTimeField(null=True, blank=True)  

    nombreAutoridadEnvia = models.CharField(verbose_name="Nombre de la Autoridad que Envia" ,max_length=100)
    nombreAutoridadRecibe = models.CharField(max_length=100, null=True, blank=True)
    responsableEnvia = models.CharField(max_length=100, null=True, blank=True)
    responsableRecibe = models.CharField(max_length=100, null=True, blank=True)
    enTraslado = models.BooleanField(default=False)
    status = models.IntegerField(choices=OPCION_STATUS_CHOICES, default=0)  # Proporcionar un valor predeterminado
    motivo_rechazo = models.TextField(null=True, blank=True)
    status_traslado = models.IntegerField(choices=TRASLADO_STATUS_CHOICES, default=0)
    numero_camiones = models.PositiveIntegerField(verbose_name="Número de Extranjeros")
    tipo_de_traslado = models.IntegerField(choices=TIPO_TRASLADO_CHOICES)  # Proporcionar un valor predeterminado

    def __str__(self):
        return f'Solicitud de {self.estacion_origen} a {self.estacion_destino}'
    

OPCION_STATUS_TRASLADO_CHOICES=[
    [0,'SOLICITUD'],
    [1,'ACEPTADO'],
    [2,'RECHAZADO'],
]
class ExtranjeroTraslado(models.Model):
    statusTraslado = models.IntegerField(choices=OPCION_STATUS_TRASLADO_CHOICES, default=0, verbose_name='Status del Exranjero')
    delTraslado = models.ForeignKey(Traslado, on_delete=models.CASCADE, null=True, blank=True)
    delExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, null=True, blank=True)
    motivo_rechazo = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.delExtranjero.nombreExtranjero} - Status: {self.get_statusTraslado_display()}'


class Alojamiento(models.Model):
    numeroOficio = models.CharField(max_length=50)
    fechaOficio = models.DateTimeField()
    estacionOrigen = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True, blank=True)
    estacionDestino = models.CharField(max_length=50)
    estatus = models.CharField(max_length=50)
    acuerdoTraslado = models.FileField(upload_to='files/', null=True, blank=True)
    

class SolicitudTraslado(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, verbose_name='Extranjero')
    estacion_origen = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='solicitudes_origen', verbose_name='Estación de Origen')
    estacion_destino = models.ForeignKey(Estacion, on_delete=models.CASCADE, related_name='solicitudes_destino', verbose_name='Estación de Destino')
    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')], default='pendiente')
    
    # Agrega campos adicionales aquí
    motivo = models.TextField(verbose_name='Motivo del traslado', blank=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Solicitud')
    fecha_aceptacion = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Aceptación')
    
    class Meta:
        verbose_name_plural = "Solicitudes de Traslado"

    def __str__(self):
        return f'Solicitud de {self.extranjero} a {self.estacion_destino}'
    

#pruebaaa
