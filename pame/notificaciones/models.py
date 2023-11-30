from django.db import models
from vigilancia.models import Extranjero,NoProceso  # Asegúrate de importar el modelo Extranjero correctamente
from catalogos.models import Estacion, Estado

class Notificacion(models.Model):
    fechaAceptacion = models.DateField(verbose_name='Fecha de Aceptación', auto_now_add=True)
    no_proceso = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name='Número de Proceso Asociado', related_name='notificaciones_comaparecencia')
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación de Notificación')
    descripcion = models.TextField(verbose_name='Descripción', blank=True, null=True)
    estatus_notificacion = models.CharField(max_length=50, verbose_name='Estatus de Notificación', blank=True, null=True)

    def __str__(self):
        return f"Notificación de {self.no_proceso.extranjero.nombreExtranjero} en {self.estacion.nombre}"
    
OPCIONES_CARGO=[
    ('Director', 'Director'),
    ('Subdirector', 'Subdirector'),
    ('Jefe de Seguridad', 'Jefe de Seguridad'),
    ('Oficial de Inmigración', 'Oficial de Inmigración'),
    ('Oficial de Custodia', 'Oficial de Custodia'),
    ('Oficial de Documentación', 'Oficial de Documentación'),
    ('Oficial de Derechos Humanos', 'Oficial de Derechos Humanos'),
    ('Oficial Médico', 'Oficial Médico'),
    ('Oficial de Procesamiento de Solicitudes', 'Oficial de Procesamiento de Solicitudes'),
    ('Abogado de Inmigración', 'Abogado de Inmigración'),
    ('Traductor', 'Traductor'),
    ('Oficial de Seguridad Nacional', 'Oficial de Seguridad Nacional'),
    ('Oficial de Reubicación', 'Oficial de Reubicación'),
    ('Consejero de Asilo', 'Consejero de Asilo'),
    ('Asistente Social', 'Asistente Social'),
    ('Oficial de Derechos de los Menores', 'Oficial de Derechos de los Menores'),
    ('Otro', 'Otro'),

]
ESTATUS_DEFENSO = [
    ('Activo','Activo'),
    ('Inactivo','Inactivo'),
]
class Defensorias(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="Estado de la Republica")
    nombreTitular = models.CharField(max_length=50, verbose_name="Nombre del titular")
    apellidoPaternoTitular = models.CharField(max_length=50, verbose_name="Apellido paterno del titular")
    apellidoMaternoTitular = models.CharField(max_length=50, verbose_name="Apellido materno del titular")
    cargoTitular = models.CharField(choices=OPCIONES_CARGO, verbose_name='Cargo de la autoridad', max_length=75)
    email1 = models.CharField(max_length=50, verbose_name="Correo 1")
    email2 = models.CharField(max_length=50, verbose_name="Correo 2", blank=True, null=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    telefono2 = models.CharField(max_length=20, verbose_name="Teléfono 2", blank=True,null=True)
    calle = models.CharField(max_length=50, verbose_name="Calle")
    colonia = models.CharField(max_length=50, verbose_name="Colonia")
    municipio = models.CharField(max_length=50, verbose_name="Municipio")
    cp = models.CharField(max_length=10, verbose_name="CP")
    estatus = models.CharField(choices=ESTATUS_DEFENSO,max_length=25, verbose_name='Estatus de la autoridad en la estación', default='Activo')

    def _str_(self):
        return self.estado

    def direccion_completa(self):
        direccion_parts = [
            self.calle,
            self.colonia,
            self.municipio,
            self.estado,  # Asumiendo que 'entidad' representa el estado
            self.cp
        ]
        return ', '.join(filter(None, direccion_parts))
    
    
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