from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField

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
    identificador = models.CharField(max_length=25, null=False)
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

GRADOS_ACADEMICOS = [
    ('Doctorado', 'Doctorado'),
    ('Maestría', 'Maestría'),
    ('Licenciatura', 'Licenciatura'),
    ('Bachillerato', 'Bachillerato'),
    ('Diplomado', 'Diplomado'),
    ('Técnico', 'Técnico'),
    ('Secundaria', 'Secundaria'),
    ('Primaria', 'Primaria'),
    ('Sin educación formal', 'Sin educación formal'),
]
ESTADO_OPCIONES =[
    ('Vigente','Vigente'),
    ('NoVigente','No Vigente'),
    ('Libre','Libre'),
    ('Asignado','Asignado'),
]
class Autoridades(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre de autoridad')
    apellidoPaterno = models.CharField(max_length=100, verbose_name='Apellido paterno')
    apellidoMaterno = models.CharField(max_length=100, verbose_name='Apellido materno')
    telefono = models.CharField(max_length=12, verbose_name='Numero telefonico')
    email = models.EmailField(max_length=100, verbose_name='Correo electronico')
    grado_academico = models.CharField(verbose_name='Grado academico', max_length=50, choices=GRADOS_ACADEMICOS)
    estado = models.CharField(verbose_name='Estado actual de la autoridad', max_length=25,choices=ESTADO_OPCIONES, default='Vigente')
    def __str__(self):
     full_name = self.nombre
     if self.apellidoPaterno:
        full_name += f' {self.apellidoPaterno}'
     if self.apellidoMaterno:
        full_name += f' {self.apellidoMaterno}'
     return full_name 
ESTATUS_AUTORIDAD = [
    ('Activo','Activo'),
    ('Inactivo','Inactivo'),
]
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
class AutoridadesActuantes(models.Model):
    autoridad = models.ForeignKey(Autoridades, on_delete=models.CASCADE, verbose_name='Autoridad')
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación')
    estatus = models.CharField(choices=ESTATUS_AUTORIDAD,max_length=25, verbose_name='Estatus de la autoridad en la estación', default='Activo')
    cargo = models.CharField(choices=OPCIONES_CARGO, verbose_name='Cargo de la autoridad', max_length=50)
    fechaInicio = models.DateField(verbose_name='Fecha de inicio de actividades', auto_now_add=True)
    fechaFin = models.DateField(verbose_name='Fceha fin de actividades', blank=True, null=True)
    def __str__(self):
        return '%s' % self.autoridad
@receiver(post_save, sender=AutoridadesActuantes)
def cambiar_estado_autoridad(sender, instance, **kwargs):
    autoridad = instance.autoridad
    autoridad.estado = 'Libre'
    autoridad.save()
class FirmaAutoridad(models.Model):
    autoridad = models.OneToOneField(Autoridades, on_delete=models.CASCADE)
    firma_imagen = models.ImageField(upload_to='firmas/', blank=True, null=True)
    fechaHoraFirmaCreate = models.DateTimeField(auto_now_add=True)
    fechaHoraFirmaUpdate = models.DateTimeField(auto_now_add=True)
IDIOMAS_CHOICES = [
    ('Inglés', 'Inglés'),
    ('Francés', 'Francés'),
    ('Alemán', 'Alemán'),
    ('Italiano', 'Italiano'),
    ('Portugués', 'Portugués'),
    ('Chino Mandarín', 'Chino Mandarín'),
    ('Japonés', 'Japonés'),
    ('Ruso', 'Ruso'),
    ('Árabe', 'Árabe'),
    ('Hindi', 'Hindi'),
    ('Coreano', 'Coreano'),
    ('Vietnamita', 'Vietnamita'),
    ('Tailandés', 'Tailandés'),
    ('Otro', 'Otro'),

    # Agrega más opciones según sea necesario
]
ESTATUS_TRADUCTORES=[
    ('Activo', 'Activo'),
    ('Inactivo', 'Inactivo'),
]
class Traductores(models.Model):
    # Campos de información personal
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    apellido_paterno = models.CharField(max_length=100, verbose_name='Apellido paterno')
    apellido_materno = models.CharField(max_length=100, verbose_name='Apellido materno')
    telefono = models.CharField(max_length=12, verbose_name='Número telefónico')
    email = models.EmailField(max_length=100, verbose_name='Correo electrónico')
    estatus = models.CharField(choices=ESTATUS_TRADUCTORES, verbose_name='Estatus del traductor', max_length=25, default='Activo')
    # Campos de información profesional
    idiomas = MultiSelectField(choices=IDIOMAS_CHOICES, max_choices=5, max_length=100)
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación migratoria')

    def __str__(self):
        return f'{self.nombre} {self.apellido_paterno}'