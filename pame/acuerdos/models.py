from django.db import models
from catalogos.models import Estacion, Responsable
from vigilancia.models import Extranjero, NoProceso
from django.core.exceptions import ValidationError
import os
from usuarios.models import Usuario
# class TestigoUno (models.Model):
#     nombreTestigoUno = models.CharField(max_length=50, verbose_name='Nombre del primer testigo')
#     apellidoPaternoTestigoUno = models.CharField(max_length=50, verbose_name='Apellido Paterno')
#     apellidoMaternoTestigoUno = models.CharField(max_length=50, verbose_name='Apellido Materno')
#     firmaTestigoUno = models.ImageField(upload_to='files/') #Ubicacion de archivos/imagenes(verbose_name='Firma')
#     huellaTestigoUno = models.ImageField(upload_to='files/') #Ubicacion de archivos/imagenes(verbose_name='Huella')
    

#     def __str__(self) -> str:
#         return '__all__'
    
#     class Meta:
#         verbose_name_plural = "Testigos Uno"

# class TestigoDos (models.Model):
#     nombreTestigoDos = models.CharField(max_length=50, verbose_name='Nombre del Segundo testigo')
#     apellidoPaternoTestigoDos = models.CharField(max_length=50, verbose_name='Apellido Paterno')
#     apellidoMaternoTestigoDos = models.CharField(max_length=50, verbose_name='Apellido Materno')
#     firmaTestigoDos = models.ImageField(upload_to='files/') #Ubicacion de archivos/imagenes(verbose_name='Firma')
#     huellaTestigoDos = models.ImageField(upload_to='files/') #Ubicacion de archivos/imagenes(verbose_name='Huella')
   

#     def __str__(self) -> str:
#         return '__all__'
    
#     class Meta:
#         verbose_name_plural = "Testigos Dos"

# class Traductor (models.Model):
#     nombreTraductor = models.CharField(max_length=50, verbose_name='Nombre(s)')
#     apellidoPaternoTraductor = models.CharField(max_length=50, verbose_name='Apellido Paterno')
#     apellidoMaternoTraductor = models.CharField(max_length=50, verbose_name='Apellido Materno')
  

#     def __str__(self) -> str:
#         return '__all__'
    
#     class Meta:
#         verbose_name_plural = "Traductores"

class TipoAcuerdo(models.Model):
    tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.tipo

class Acuerdo(models.Model):
    delAcuerdo = models.ForeignKey(TipoAcuerdo, on_delete=models.CASCADE, verbose_name="Tipo de Acuerdo")
    fechaAcuerdo = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Acuerdo")
    numeroExpediente = models.CharField(max_length=50, verbose_name="Número de Expediente")
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Estación")
    delResponsable = models.ForeignKey(Responsable, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Responsable")
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name="NUP (No. Proceso)")
    nombreTestigoUno = models.CharField(max_length=50, verbose_name="Nombre:")
    apellidoPaternoTestigoUno = models.CharField(max_length=50, verbose_name="Apellido Paterno:")
    apellidoMaternoTestigoUno = models.CharField(max_length=50, verbose_name="Apellido Materno:")
    nombreTestigoDos = models.CharField(max_length=50, verbose_name="Nombre:")
    apellidoPaternoTestigoDos = models.CharField(max_length=50, verbose_name="Apellido Paterno:")
    apellidoMaternoTestigoDos = models.CharField(max_length=50, verbose_name="Apellido Materno:")
    nombreTraductor = models.CharField(max_length=50, verbose_name="Nombre del Traductor")
    apellidoPaternoTraductor = models.CharField(max_length=50, verbose_name="Apellido Paterno del Traductor")
    apellidoMaternoTraductor = models.CharField(max_length=50, verbose_name="Apellido Materno del Traductor")
    razonContinuidad_Continuacion = models.TextField(null=True, blank=True, verbose_name="Razón de Continuidad/Continuación")
    fechaSuspensión_Continuacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Suspensión/Continuación")
    autoridadEmisora_Acumulacion = models.TextField(null=True, blank=True, verbose_name="Autoridad Emisora/Acumulación")
    numeroExpedienteAnterior_Acumulacion = models.CharField(max_length=50, null=True, blank=True, verbose_name="Número de Expediente Anterior/Acumulación")
    antecedentes_conclusion = models.TextField(null=True, blank=True, verbose_name="Antecedentes/Conclusión")
    delegatorio_inicio = models.TextField(null=True, blank=True, verbose_name="Delegatorio/Inicio")
    descripcion_recepcion = models.TextField(null=True, blank=True, verbose_name="Descripción/Recepción")
    fundamento_separacion = models.TextField(null=True, blank=True, verbose_name="Fundamento/Separación")
    razon_suspension = models.TextField(null=True, blank=True, verbose_name="Razón/Suspensión")
    declaracionExtanjero_comparecencia = models.TextField(null=True, blank=True, verbose_name="Declaración de Extranjero/Comparecencia")
    estacionDestino_traslado = models.CharField(max_length=50, null=True, blank=True, verbose_name="Estación de Destino/Traslado")
    motivo_traslado = models.TextField(null=True, blank=True, verbose_name="Motivo/Traslado")


class FirmaAcuerdo(models.Model):
    acuerdo = models.ForeignKey(Acuerdo, on_delete=models.CASCADE)
    firmaTestigoUno = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    firmaTestigoDos = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    firmaTraductor = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    firmaResponsable = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()


class PDFGenerado(models.Model):
    documento = models.CharField(max_length=255)
    # Ruta donde se van a guardar los pdf generados por primera vez
    ruta = models.FileField(upload_to='files/') 

    def __str__(self):
        return self.documento
    

def upload_to(instance, filename):
    # Esta función determina dónde se almacenará el archivo
    base_filename = instance.tipo_notificacion  # Usamos el tipo de notificación como el nombre base del archivo
    return f'acuerdos/acuerdos_generales/{base_filename}.pdf'
def validate_pdf(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] devuelve el path+filename; [1] devuelve la extensión del archivo
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Solo se aceptan archivos PDF.')
class NotificacionesGlobales(models.Model):
    NOTIFICACION_DERECHOS = 'notificacion_derechos_obligaciones'
    
    TIPO_NOTIFICACION_CHOICES = [
        (NOTIFICACION_DERECHOS, 'Notificación de Derechos y Obligaciones'),
    ]

    tipo_notificacion = models.CharField(max_length=50, choices=TIPO_NOTIFICACION_CHOICES, unique=True)
    archivo = models.FileField(upload_to=upload_to, validators=[validate_pdf])
    fecha_hora = models.DateTimeField(auto_now_add=True)

def upload(instance, filename):
    # Toma el nup de la instancia de NoProceso relacionada
    nup_folder = instance.nup.nup
    # Crea la estructura de directorio final
    path = os.path.join('extranjeros', nup_folder, filename)
    return path

class Documentos(models.Model):
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE, verbose_name='Número de Proceso Asociado')
    acuerdo_inicio = models.FileField(upload_to=upload)
    oficio_llamada = models.FileField(upload_to=upload)
    oficio_derechos_obligaciones = models.FileField(upload_to=upload)


class ClasificaDoc(models.Model):
    clasificacion = models.CharField(max_length=50)
    
    def __str__(self):
        return self.clasificacion
class TiposDoc (models.Model):
    descripcion = models.CharField(max_length=50)
    delaClasificacion = models.ForeignKey(ClasificaDoc, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
class Repositorio (models.Model):
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    fechaGeneracion = models.DateTimeField(auto_now_add=True)
    delTipo = models.ForeignKey(TiposDoc, on_delete=models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    delResponsable = models.CharField(max_length=255)  # CharField para guardar el nombre completo del usuario
    archivo = models.FileField(verbose_name="Documento:",upload_to=upload, null=True, blank=True)

    def delete(self, *args, **kwargs):
            # Si el modelo tiene un archivo asociado, elimínalo
            if self.archivo:
                self.archivo.delete(save=False)
            super(Repositorio, self).delete(*args, **kwargs)
    def __str__(self):
        return str(self.nup)

