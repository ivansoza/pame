from django.db import models
from vigilancia.models import Extranjero,NoProceso  # Asegúrate de importar el modelo Extranjero correctamente
from catalogos.models import AutoridadesActuantes, Consulado, Estacion,AutoridadesActuantes
from catalogos.models import AutoridadesActuantes, Consulado, Estacion, Comar, Fiscalia
from comparecencia.models import Comparecencia
from catalogos.models import AutoridadesActuantes, Consulado, Estacion,AutoridadesActuantes, Estado
import os
from acuerdos.models import Repositorio
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


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
class NotificacionConsular(models.Model):
    delaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name="Estación")
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name="Numero de Proceso")
    fechaNotificacion= models.DateField(auto_now_add=True)
    horaNotificacion = models.DateTimeField(auto_now_add=True)
    numeroOficio = models.CharField(max_length=50, verbose_name="Numero de Oficio")
    delConsulado = models.ForeignKey(Consulado, on_delete=models.CASCADE, verbose_name="Consulado")
    accion = models.CharField(max_length=50, choices= ACCION, verbose_name="Acción")
    delaAutoridad = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name="Autoridad Actuante")

class FirmaNotificacionConsular(models.Model):
    notificacionConsular = models.ForeignKey(NotificacionConsular, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True, verbose_name="Firma de la Autoridad Actuante") #Ubicacion de archivos/imagenes()

class NotificacionCOMAR(models.Model):
    delaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    deComar = models.ForeignKey(Comar, on_delete=models.CASCADE)
    fechaNotificacion= models.DateField(auto_now_add=True)
    horaNotificacion = models.DateTimeField(auto_now_add=True)
    numeroOficio = models.CharField(max_length=50)
    nup= models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name="Numero de Proceso")
    notificacionComar= models.TextField()
    delaComparecencia = models.ForeignKey(Comparecencia, on_delete=models.CASCADE)
    delaAutoridad = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name="Autoridad Actuante")
    contstanciaAdmision_Rechazo = models.FileField(verbose_name="Constancia de Admisión/Rechazo:",upload_to='files/', null=True, blank=True)
    acuerdoSuspension = models.FileField(verbose_name="Acuerdo Suspensión:",upload_to='files/', null=True, blank=True)
class FirmaNotificacionComar(models.Model):
    notificacionComar = models.ForeignKey(NotificacionCOMAR, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True, verbose_name="Firma de la Autoridad Actuante") #Ubicacion de archivos/imagenes()

CONDICION = (
    ('Victima', 'VICTIMA'),
    ('Testigo', 'TESTIGO'),
)
class NotificacionFiscalia(models.Model):
    delaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    nup= models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name="Numero de Proceso")
    fechaNotificacion= models.DateField(auto_now_add=True)
    horaNotificacion = models.DateTimeField(auto_now_add=True)
    numeroOficio = models.CharField(max_length=50)
    delaFiscalia = models.ForeignKey(Fiscalia, on_delete=models.CASCADE)
    delaComparecencia = models.ForeignKey(Comparecencia, on_delete=models.CASCADE)
    condicion = models.CharField(max_length=50, choices= CONDICION)
    delaAutoridad = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name="Autoridad Actuante")

    documentoFGR = models.FileField(verbose_name="Documento FGR:",upload_to='files/', null=True, blank=True)
    
class FirmaNotificacionFiscalia(models.Model):
    notificacionFiscalia = models.ForeignKey(NotificacionFiscalia, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True, verbose_name="Firma de la Autoridad Actuante") #Ubicacion de archivos/imagenes()

    
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
 
    def __str__(self):
        # Asumiendo que 'estado' tiene un campo 'nombre' que representa el nombre del estado
        nombre_estado = self.estado.estado if self.estado else ''
        nombre_titular = f'{self.nombreTitular} {self.apellidoPaternoTitular} {self.apellidoMaternoTitular}'.strip()
        return f'{nombre_estado} - {nombre_titular}'


    def direccion_completa(self):
        direccion_parts = [
            self.calle,
            self.colonia,
            self.municipio,
            self.estado.estado,  # Asumiendo que 'entidad' representa el estado
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
    autoridad_actuante = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, related_name='autoridad_actuante')
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    defensoria = models.ForeignKey(Defensorias, on_delete=models.CASCADE)
    fechaHora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return f"{self.extranjero}"
     
class Qrfirma(models.Model):
    autoridad = models.ForeignKey(Relacion, on_delete=models.CASCADE)
    firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True) 


class ExtranjeroDefensoria(models.Model):
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    autoridadActuante = models.ForeignKey(AutoridadesActuantes, on_delete=models.CASCADE, verbose_name='Autoridad Actuante')
    numeroExpediente = models.CharField(max_length=50, verbose_name='Numero de expediente')
    defensoria = models.ForeignKey(Defensorias, on_delete=models.CASCADE)
    oficio = models.CharField(max_length=100, verbose_name='Numero de oficio')
    fechaHora = models.DateTimeField(auto_now_add=True)

class firmasDefenso(models.Model):
     defensoria = models.ForeignKey(ExtranjeroDefensoria, on_delete=models.CASCADE)
     firmaAutoridadActuante = models.ImageField(upload_to='files/', null=True, blank=True) 

def upload(instance, filename):
    # Toma el nup de la instancia de NoProceso relacionada
    nup_folder = instance.nup.nup
    # Crea la estructura de directorio final
    path = os.path.join('extranjeros', nup_folder, filename)
    return path
class DocumentoRespuestaDefensoria(models.Model):
    extranjero_defensoria = models.ForeignKey(ExtranjeroDefensoria, on_delete=models.CASCADE, related_name='documentos_respuesta')
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    archivo = models.FileField(verbose_name="Documento:",upload_to=upload, null=True, blank=True)
    descripcion = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento para {self.extranjero_defensoria.nup}"
    def delete(self, *args, **kwargs):
            # Si el modelo tiene un archivo asociado, elimínalo
            if self.archivo:
                self.archivo.delete(save=False)
            super(Repositorio, self).delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        # Si el archivo es una imagen, conviértelo a PDF
        if 'image' in self.archivo.file.content_type:
            # Abre la imagen usando Pillow
            img = Image.open(self.archivo)
            # Convierte la imagen a PDF
            buffer = BytesIO()
            img.save(buffer, format='PDF')
            # Guarda el PDF en lugar de la imagen
            file_name = os.path.splitext(self.archivo.name)[0] + '.pdf'
            self.archivo.save(file_name, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)


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
# class nombramientoRepresentante(models.Model):
#     delaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name="Estación")
#     nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
#     defensoria = models.ForeignKey(ExtranjeroDefensoria, on_delete=models.CASCADE)
    
#     autoridadActuante=models.ForeignKey(AutoridadesActuantes,related_name='Autoridadactuante', on_delete=models.CASCADE, verbose_name='Autoridad', blank=True, null=True)
#     representanteLegal = models.ForeignKey(RepresentantesLegales, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Representante Legal')
#     representanteLegalExterno = models.ForeignKey(null=True, blank=True, verbose_name='Representante Legal Externo')
#     cedulaLegalExterno = models.CharField(max_length=50, verbose_name='Número de Cédula')
#     traductor=models.ForeignKey(Traductores,related_name='Traductor', on_delete=models.CASCADE, verbose_name='Traductor', blank=True, null=True)
#     testigo1=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 1")
#     grado_academico_testigo1=models.CharField(verbose_name='Grado Académico del Testigo 1', max_length=50, choices=GRADOS_ACADEMICOS)
#     testigo2=models.CharField(max_length=50, verbose_name="Nombre Completo del Testigo 2")
#     grado_academico_testigo2=models.CharField(verbose_name='Grado Académico del Testigo 2', max_length=50, choices=GRADOS_ACADEMICOS)

   