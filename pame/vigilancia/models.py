from django.db import models
from catalogos.models import Estacion, Responsable, Salida, Estancia, Relacion
from PIL import Image, ExifTags


class Nacionalidad(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='País')
    Abreviatura = models.CharField(max_length=200,verbose_name='Abreviatura')
    
    class Meta:
        verbose_name_plural = "Países"
    
    def __str__(self):
        return self.nombre
    
# FUNCION PARA ASIGNAR UN NOMBRE DE CARPETA A PARTIR DE LA ESTACION, SU IDENTIFICADOR DE PROCESO Y SU FILE NAME 
def user_directory_pathINM(instance, filename):
    estacion = instance.deLaEstacion.identificador if instance.deLaEstacion else 'sin_estacion'
    identificador_proceso = instance.identificadorProceso if instance.identificadorProceso else 'sin_identificador'
    return f'{estacion}/PUESTAINM/{identificador_proceso}/{filename}'

class PuestaDisposicionINM(models.Model):
    identificadorProceso = models.CharField(verbose_name='Número de Proceso', max_length=50)
    numeroOficio = models.CharField(verbose_name='Número de Oficio', max_length=50)
    fechaOficio = models.DateTimeField(verbose_name='Fecha de Oficio',auto_now_add=True)
    nombreAutoridadSignaUno = models.CharField(verbose_name='Nombre de Autoridad que firma (1)', max_length=100)
    cargoAutoridadSignaUno = models.CharField(verbose_name='Cargo de Autoridad que firma (1)', max_length=100)
    nombreAutoridadSignaDos = models.CharField(verbose_name='Nombre de Autoridad que firma (2)', max_length=100)
    cargoAutoridadSignaDos = models.CharField(verbose_name='Cargo de Autoridad que firma (2)', max_length=100)
    oficioPuesta = models.FileField(upload_to=user_directory_pathINM, verbose_name='Oficio de Puesta', null=True, blank=True)
    oficioComision = models.FileField(upload_to=user_directory_pathINM, verbose_name='Oficio de Comisión', null=True, blank=True)
    puntoRevision = models.CharField(verbose_name='Punto de Revisión', max_length=100)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación de Origen', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Puestas a Disposición INM"
        ordering = ['-fechaOficio']

    def __str__(self):
        return self.identificadorProceso
    
    @property
    def extranjeros(self):
        return self.extranjeros.all()
    
def user_directory_pathAC(instance, filename):
    estacion = instance.deLaEstacion.identificador if instance.deLaEstacion else 'sin_estacion'
    identificador_proceso = instance.identificadorProceso if instance.identificadorProceso else 'sin_identificador'
    return f'{estacion}/PUESTAC/{identificador_proceso}/{filename}'

class PuestaDisposicionAC(models.Model):
    identificadorProceso = models.CharField(verbose_name='Número de Proceso', max_length=50)
    numeroOficio = models.CharField(verbose_name='Número de Oficio', max_length=50)
    fechaOficio = models.DateField(verbose_name='Fecha de Oficio')
    nombreAutoridadSignaUno = models.CharField(verbose_name='Nombre de Autoridad que firma (1)', max_length=100)
    cargoAutoridadSignaUno = models.CharField(verbose_name='Cargo de Autoridad que firma (1)', max_length=100)
    nombreAutoridadSignaDos = models.CharField(verbose_name='Nombre de Autoridad que firma (2)', max_length=100)
    cargoAutoridadSignaDos = models.CharField(verbose_name='Cargo de Autoridad que firma (2)', max_length=100)
    oficioPuesta = models.FileField(upload_to=user_directory_pathAC, verbose_name='Oficio de Puesta', null=True, blank=True)
    oficioComision = models.FileField(upload_to=user_directory_pathAC, verbose_name='Oficio de Comisión', null=True, blank=True)
    puntoRevision = models.CharField(verbose_name='Punto de Revisión', max_length=100)
    dependencia = models.CharField(verbose_name='Dependencia', max_length=100)
    numeroCarpeta = models.IntegerField(verbose_name='Número de Carpeta')
    entidadFederativa = models.CharField(verbose_name='Entidad Federativa', max_length=100)
    municipio =models.CharField(max_length=50)
    certificadoMedico = models.FileField(upload_to=user_directory_pathAC, verbose_name='Certificado Médico', null=True, blank=True)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación de Origen', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Puestas a Disposicion AC"
    
    def __str__(self):
        return str(self.numeroOficio) 
    
class PuestaDisposicionVP(models.Model):
    numeroOficio = models.CharField(max_length=50, verbose_name='Numero de Oficio')
    fechaOficio = models.DateField(verbose_name='Fecha de Oficio')
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name="Estación de origen", null=True, blank=True)
    class Meta:
        verbose_name_plural = "Puestas a Disposición VP"
    def __str__(self):
        return str(self.numeroOficio) 


OPCION_GENERO_CHOICES=[
    [0,'HOMBRE'],
    [1,'MUJER'],
    [2, 'NO BINARIO']
]
OPCION_ESTATUS_CHOICES=[
    ('Activo','activo'),
    ('Inactivo','inactivo'),
]
class Extranjero(models.Model):
    fechaRegistro = models.DateField(verbose_name='Fecha de Registro', auto_now_add=True)
    horaRegistro = models.DateTimeField(verbose_name='Hora de Registro', auto_now_add=True)
    numeroExtranjero = models.CharField(verbose_name='Número de Extranjero', max_length=25, null=True, blank=True)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación de Origen', null=True, blank=True)
    nombreExtranjero = models.CharField(verbose_name='Nombre de Extranjero', max_length=50, blank=True)
    apellidoPaternoExtranjero = models.CharField(verbose_name='Apellido Paterno de Extranjero', max_length=50, blank=True)
    apellidoMaternoExtranjero = models.CharField(verbose_name='Apellido Materno', max_length=50, blank=True, null=True, default=" ")
    nacionalidad = models.ForeignKey(Nacionalidad, on_delete=models.CASCADE, verbose_name='País')
    genero = models.IntegerField(verbose_name='Género', choices=OPCION_GENERO_CHOICES)
    fechaNacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
    documentoIdentidad = models.FileField(upload_to='files/', verbose_name='Documento de Identidad', null=True, blank=True)
    tipoEstancia = models.ForeignKey(Estancia, on_delete=models.CASCADE, verbose_name='Modalidad de Ingreso')
    estatus = models.CharField(verbose_name='Estatus', max_length=25, choices=OPCION_ESTATUS_CHOICES, default='Activo')
    viajaSolo = models.BooleanField(verbose_name='Viaja Solo', default=True)
    deLaPuestaIMN = models.ForeignKey(PuestaDisposicionINM, on_delete=models.CASCADE, blank=True, null=True, related_name='extranjeros', verbose_name='Puesta IMN')
    deLaPuestaAC = models.ForeignKey(PuestaDisposicionAC, on_delete=models.CASCADE, blank=True, null=True, related_name='extranjeros', verbose_name='Puesta AC')
    deLaPuestaVP = models.ForeignKey(PuestaDisposicionVP, on_delete=models.CASCADE, blank=True, null=True, related_name='extranjeros', verbose_name='Puesta VP')
    def save(self, *args, **kwargs):
    # Si el númeroExtranjero no está establecido, asigna un valor único basado en el ID del registro.
     if not self.numeroExtranjero:
        base_value = str(self.id)
        self.numeroExtranjero = base_value

     super(Extranjero, self).save(*args, **kwargs)

   
    class Meta:
        verbose_name_plural = "Extranjeros" 
    def __str__(self):
         return self.nombreExtranjero
    
    def delete(self, *args, **kwargs):
        # Incrementar la capacidad de la estación al eliminar
        if self.deLaEstacion:
            self.deLaEstacion.capacidad += 1
            self.deLaEstacion.save()
        super().delete(*args, **kwargs)

    @property
    def tiene_fotografia(self):
        try:
            return bool(self.biometrico.fotografiaExtranjero)
        except Biometrico.DoesNotExist:
            return False

estatura_choices = (
        ('1.70', '1.70 m o más'),
        ('1.65', '1.65 m - 1.69 m'),
        ('1.60', '1.60 m - 1.64 m'),
        ('1.55', '1.55 m - 1.59 m'),
        ('1.50', '1.50 m - 1.54 m'),
        ('1.45', '1.45 m - 1.49 m'),
)

cejas_choices = (
    ('Pobladas', 'Pobladas'),
    ('Delgadas', 'Delgadas'),
    ('Normales', 'Normales'),
    # Agrega más opciones según sea necesario
)

nariz_choices = (
    ('Aguileña', 'Aguileña'),
    ('Chata', 'Chata'),
    ('Normal', 'Normal'),
    # Agrega más opciones según sea necesario
)

labios_choices = (
    ('Gruesos', 'Gruesos'),
    ('Delgados', 'Delgados'),
    ('Normales', 'Normales'),
    # Agrega más opciones según sea necesario
)

tipoCabello_choices = (
    ('Largo', 'Largo'),
    ('Corto', 'Corto'),
    ('Rizado', 'Rizado'),
    # Agrega más opciones según sea necesario
)

bigote_choices = (
    ('Presente', 'Presente'),
    ('Ausente', 'Ausente'),
    ('No Aplica', 'No Aplica'),
    # Agrega más opciones según sea necesario
)

complexion_choices = (
    ('Delgada', 'Delgada'),
    ('Normal', 'Normal'),
    ('Robusta', 'Robusta'),
    # Agrega más opciones según sea necesario
)

frente_choices = (
    ('Amplia', 'Amplia'),
    ('Estrecha', 'Estrecha'),
    ('Normal', 'Normal'),
    # Agrega más opciones según sea necesario
)

colorOjos_choices = (
    ('Azul', 'Azul'),
    ('Verde', 'Verde'),
    ('Café', 'Café'),
    # Agrega más opciones según sea necesario
)

boca_choices = (
    ('Grande', 'Grande'),
    ('Pequeña', 'Pequeña'),
    ('Normal', 'Normal'),
    # Agrega más opciones según sea necesario
)

segnasParticulares_choices = (
    ('Tatuaje en el brazo', 'Tatuaje en el brazo'),
    ('Cicatriz en la mejilla', 'Cicatriz en la mejilla'),
    ('Sin señas particulares', 'Sin señas particulares'),
    # Agrega más opciones según sea necesario
)
class descripcion(models.Model):
    delExtranjero = models.OneToOneField(
        Extranjero, on_delete=models.CASCADE,
        primary_key=True,
    )
    estatura = models.CharField(max_length=20, choices=estatura_choices)
    cejas = models.CharField(max_length=50, choices=cejas_choices)
    nariz = models.CharField(max_length=50, choices=nariz_choices)
    labios = models.CharField(max_length=50, choices=labios_choices)
    tipoCabello = models.CharField(max_length=50, choices=tipoCabello_choices, verbose_name='Tipo de cabello')
    bigote = models.CharField(max_length=50, blank=True, null=True, choices=bigote_choices)
    complexion = models.CharField(max_length=50, choices=complexion_choices)
    frente = models.CharField(max_length=50, choices=frente_choices)
    colorOjos=models.CharField(max_length=50, verbose_name='Color de Ojos', choices=colorOjos_choices)
    boca = models.CharField(max_length=50, choices=boca_choices)
    segnasParticulares = models.CharField(max_length=50, verbose_name='Señas Particulares', choices=segnasParticulares_choices)
    observaciones = models.CharField(max_length=50)  

STATUS_PROCESO_CHOICES= (
    ('Activo', 'Activo'),
    ('Suspendido', 'Suspendido'),
    ('Cerrado', 'Cerrado'),
    # Agrega más opciones según sea necesario
)
class NoProceso(models.Model):
    agno = models.DateField(auto_now_add=True)
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    consecutivo = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_PROCESO_CHOICES)
    comparecencia = models.BooleanField(verbose_name='¿Tuvo comparecencia?')
    nup = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
       return self.nup

    @property
    def only_year(self):
        return self.agno.strftime('%Y')

class Proceso(models.Model):
    estacionInicio = models.CharField(max_length=60)
    estacionFin = models.CharField(max_length=60, blank=True, null=True)
    fechaInicio = models.DateTimeField(auto_now_add=True)
    fechaFin = models.DateTimeField(blank=True, null=True)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    
    
        
class Acompanante(models.Model):
    delExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, blank=True, null=True, related_name='acompanantes_delExtranjero')
    delAcompanante = models.ForeignKey(Extranjero, on_delete=models.CASCADE, blank=True, null=True, related_name='acompanantes_delAcompanante')
    relacion = models.ForeignKey(Relacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.delExtranjero} - {self.delAcompanante}"

    class Meta:
        verbose_name_plural = "Acompañantes"
class Biometrico(models.Model):
    Extranjero = models.OneToOneField(
        Extranjero, on_delete=models.CASCADE,
        primary_key=True,
    )
    fotografiaExtranjero = models.ImageField(verbose_name="Fotografía del Extranjero:", upload_to='rostros/')
    fechaHoraFotoCreate = models.DateTimeField(auto_now_add=True)
    fechaHoraFotoUpdate = models.DateTimeField(auto_now_add=True)
    face_encoding = models.JSONField(blank=True, null=True)  #

    huellaExtranjero = models.FileField(verbose_name="Huella del Extranjero:",upload_to='files/', null=True, blank=True)
    fechaHoraHuellaCreate = models.DateTimeField(auto_now_add=True)
    fechaHoraHuellaUpdate = models.DateTimeField(auto_now_add=True)
    firmaExtranjero = models.FileField(verbose_name="Firma del Extranjero:",upload_to='files/', null=True, blank=True)
    fechaHoraFirmaCreate = models.DateTimeField(auto_now_add=True)
    fechaHoraFirmaUpdate = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = 'Biometricos'

    def __str__(self):
        return str(self.Extranjero.nombreExtranjero) 
    
class UserFace(models.Model):
    nombreExtranjero = models.CharField(verbose_name='Nombre de Extranjero', max_length=50, blank=True)
    image = models.ImageField(upload_to='user_faces/')
    face_encoding = models.JSONField(blank=True, null=True)  #

    def __str__(self):
        return self.nombreExtranjero


