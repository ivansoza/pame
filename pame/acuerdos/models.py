from django.db import models
from catalogos.models import Estacion, Responsable
from vigilancia.models import Extranjero

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
    delAcuerdo = models.ForeignKey(TipoAcuerdo, on_delete=models.CASCADE)
    fechaAcuerdo = models.DateField()
    numeroExpediente = models.CharField(max_length=50)
    horaAcuerdo = models.TimeField()
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE, null=True, blank=True)
    delResponsable = models.ForeignKey(Responsable, on_delete=models.CASCADE)
    delExtanjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nombreTestigoUno = models.CharField(max_length=50)
    apellidoPaternoTestigoUno = models.CharField(max_length=50)
    apellidoMaternoTestigoUno = models.CharField(max_length=50)
    firmaTestigoUno = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    huellaTestigoUno = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    nombreTestigoDos = models.CharField(max_length=50)
    apellidoPaternoTestigoDos = models.CharField(max_length=50)
    apellidoMaternoTestigoDos = models.CharField(max_length=50)
    firmaTestigoDos = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    huellaTestigoDos = models.ImageField(upload_to='files/', null=True, blank=True) #Ubicacion de archivos/imagenes()
    delExtanjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nombreTraductor = models.CharField(max_length=50)
    apellidoPaternoTraductor = models.CharField(max_length=50)
    apellidoMaternoTraductor = models.CharField(max_length=50)
    razonContinuidad_Continuacion = models.TextField(null=True, blank = True)
    fechaSuspensión_Continuacion = models.DateField(null=True, blank=True)
    autoridadEmisora_Acumulacion = models.TextField(null=True, blank = True)
    numeroExpedienteAnterior_Acumulacion =models.CharField(max_length=50, null=True, blank =True)
    antecedentes_conclusion = models.TextField(null=True, blank = True)
    delegatorio_inicio = models.TextField(null=True, blank = True)
    descripcion_recepcion = models.TextField(null=True, blank = True)
    fundamento_separacion = models.TextField(null=True, blank = True)
    razon_suspension = models.TextField(null=True, blank = True)
    declaracionExtanjero_comparecencia = models.TextField(null=True, blank = True)
    estacionDestino_traslado = models.CharField(max_length=50, null=True, blank = True)
    motivo_traslado = models.TextField(null=True, blank = True)
    documentoAcuerdo= models.FileField(upload_to='files/', null=True, blank=True)

class PDFGenerado(models.Model):
    documento = models.CharField(max_length=255)
    # Ruta donde se van a guardar los pdf generados por primera vez
    ruta = models.FileField(upload_to='files/') 

    def __str__(self):
        return self.documento