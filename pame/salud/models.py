from django.db import models
from vigilancia.models import Extranjero, NoProceso
from catalogos.models import Estacion
# Create your models here.
class PerfilMedico(models.Model):
    nombreMedico = models.CharField(max_length=50)
    apellidoPaternoMedico = models.CharField(max_length=50)
    apellidoMaternoMedico = models.CharField(max_length=50)
    cedula = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural= "Perfiles Medicos"

class Consulta(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaConsulta = models.DateField()
    horaConsulta = models.DateTimeField()
# Exploracion física
    temperatura = models.DecimalField(max_digits=10, decimal_places=2)
    frecuenciaRespiratoria = models.IntegerField()
    presionArterialSistolica = models.IntegerField()
    presionArterialDiastolica =models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    estatura = models.DecimalField(max_digits=10, decimal_places=2)
    oxigenacionSaturacion = models.DecimalField(max_digits=10, decimal_places=2)
    oxigenacionFrecuencia = models.DecimalField(max_digits=10, decimal_places=2)
    indiceMasaCorporal = models.DecimalField(max_digits=10, decimal_places=2)
#Padecimientos actuales
    diarrea = models.BooleanField()
    infeccionesRespiratorias =models.BooleanField()
    fiebre=models.BooleanField()
    hemorragias = models.BooleanField()
    nauseasVomito= models.BooleanField()
    tos = models.BooleanField()
    dolores=models.BooleanField()
    lesionesPiel = models.BooleanField()
    mareosVertigo=models.BooleanField()
    tabaquismo=models.BooleanField()
    bebidasAlcoholicas = models.BooleanField()
    toxicomanias = models.TextField()
    tipoDieta = models.CharField(max_length=50)
    sintomasCovid=models.TextField()
    embarazo = models.BooleanField()
    tiempoEmbarazo=models.DecimalField(max_digits=10, decimal_places=2)
    conclusionDiagnostica= models.TextField()
    observaciones =models.TextField()
    tratamiento = models.TextField()
    class Meta:
        verbose_name_plural = "Consulta"

class ConsultaExterna(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaConsulta = models.DateField()
    horaConsulta = models.CharField(max_length=50)
    diagnostico = models.TextField()
    unidadMedica = models.TextField()
    documentoAtencionExterna = models.FileField(verbose_name="Consulta externa",upload_to='files/', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Consultas Externas"

class RecetaMedica(models.Model):
    diagnostico = models.TextField()
    delaConsulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, null = True, blank= True)
    delaConsultaExterna = models.ForeignKey(ConsultaExterna, on_delete=models.CASCADE, null = True, blank= True)
    class Meta:
        verbose_name_plural = "Recetas Medicas"
 
class DetalleTratamiento(models.Model):
    dosis = models.IntegerField()
    unidad = models.CharField(max_length=50)
    nombreMedicamento = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    delaReceta = models.ForeignKey(RecetaMedica, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Detalle Tratamientos"

OPCION_TIPO_CHOICES= [
    [0,'INGRESO'],
    [1,'EGRESO'],
]

class CertificadoMedico(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, related_name='certificados_medicos')
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaCertificado = models.DateField()
    horaCertificado = models.CharField(max_length=50)
    tipoCertificado = models.CharField(verbose_name='Tipo Certificado', max_length=25, choices=OPCION_TIPO_CHOICES, default='INGRESO')
# Exploracion física
    temperatura = models.DecimalField(max_digits=10, decimal_places=2)
    frecuenciaRespiratoria = models.IntegerField(verbose_name='Frecuencia Respiratoria')
    presionArterialSistolica = models.IntegerField()
    presionArterialDiastolica =models.IntegerField()
    peso = models.DecimalField(max_digits=10, decimal_places=2)
    estatura = models.DecimalField(max_digits=10, decimal_places=2)
    oxigenacionSaturacion = models.DecimalField(max_digits=10, decimal_places=2)
    oxigenacionFrecuencia = models.DecimalField(max_digits=10, decimal_places=2)
    indiceMasaCorporal = models.DecimalField(max_digits=10, decimal_places=2)
# Antecedentes
    hepatitis = models.BooleanField()
    tubercolisis = models.BooleanField()
    paludismo = models.BooleanField()
    dengue = models.BooleanField()
    colera = models.BooleanField()
    hipertension = models.BooleanField()
    cardiopatias = models.BooleanField()
    vih = models.BooleanField()
    otrosAntecedentes = models.TextField()
    antecedentesQuirurgicos = models.TextField()
    padecimientosCronicos= models.TextField()
    alergias = models.TextField()
#   Padecimientos actuales
    diarrea = models.BooleanField()
    infeccionesRespiratorias =models.BooleanField()
    fiebre=models.BooleanField()
    hemorragias = models.BooleanField()
    nauseasVomito= models.BooleanField()
    tos = models.BooleanField()
    dolores=models.BooleanField()
    lesionesPiel = models.BooleanField()
    mareosVertigo=models.BooleanField()
    tabaquismo=models.BooleanField()
    bebidasAlcoholicas = models.BooleanField()
    toxicomanias = models.TextField()
    tipoDieta = models.CharField(max_length=50)
    sintomasCovid=models.TextField()
    embarazo = models.BooleanField()
    tiempoEmbarazo=models.DecimalField(max_digits=10, decimal_places=2)
    conclusionDiagnostica= models.TextField()
    observaciones =models.TextField()
    tratamiento = models.TextField()

    class Meta:
        verbose_name_plural = "Certificados Medicos"

class CertificadoExterno(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaCertificado = models.DateField()
    horaCertificado = models.CharField(max_length=50)
    diagnostico = models.TextField()
    unidadMedica = models.TextField()
    documentoAtencionExterna = models.FileField(verbose_name="Certificado Externo:",upload_to='files/', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Certificados Externos"