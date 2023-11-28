from django.db import models
from vigilancia.models import Extranjero, NoProceso
from catalogos.models import Estacion
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class PerfilMedico(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombreMedico = models.CharField(max_length=50)
    apellidosMedico = models.CharField(max_length=100)
    cedula = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural= "Perfiles Medicos"

TIPO_DIETAS=[
    ('GENERAL','GENERAL'),
    ('RELIGIOSA','RELIGIOSA'),
    ('VEGETARIANA','VEGETARIANA'),
    ('CLÍNICA','CLÍNICA'),
]
REFERENCIA_BOOL = [
    (True, 'Sí'),
    (False, 'No'),
]
class Consulta(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaHoraConsulta = models.DateTimeField(auto_now_add=True)
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
    tipoDieta = models.CharField(max_length=50, verbose_name='Tipo de Dietas', choices=TIPO_DIETAS)
    sintomasCovid=models.TextField()
    embarazo = models.BooleanField()
    tiempoEmbarazo=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tiempo Embarazo', null=True, blank=True)
    conclusionDiagnostica= models.TextField()
    observaciones =models.TextField()
    tratamiento = models.TextField()
    referencia = models.BooleanField(
        verbose_name='¿El extranjero requiere referencia Medica?',
        choices=REFERENCIA_BOOL,
        default=False,  # o True según tu preferencia predeterminada
    )
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


OPCION_TIPO_CHOICES=[
    ('INGRESO','INGRESO'),
    ('EGRESO','EGRESO'),
]
OPCIONES_BOOL = [
    (True, 'Sí'),
    (False, 'No'),
]
class CertificadoMedico(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, related_name='certificados_medicos')
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaHoraCertificado = models.DateTimeField(auto_now_add=True)
    tipoCertificado = models.CharField(verbose_name='Tipo Certificado', max_length=25, choices=OPCION_TIPO_CHOICES, default='INGRESO')
# Exploracion física
    temperatura = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Temperatura')
    frecuenciaRespiratoria = models.IntegerField(verbose_name='Frecuencia Respiratoria')
    presionArterialSistolica = models.IntegerField(verbose_name='Presión Arterial Sistólica')
    presionArterialDiastolica =models.IntegerField(verbose_name='Presión Arterial Diastólica')
    peso = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Peso')
    estatura = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Estatura')
    oxigenacionSaturacion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Oxigenación Saturación')
    oxigenacionFrecuencia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Oxigenación Frecuencia')
    indiceMasaCorporal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Indice Masa Corporal')
# Antecedentes
    hepatitis = models.BooleanField(verbose_name='Hepatitis')
    tubercolisis = models.BooleanField(verbose_name='Tuberculosis')
    paludismo = models.BooleanField(verbose_name='Paludismo')
    dengue = models.BooleanField(verbose_name='Dengue')
    colera = models.BooleanField(verbose_name='Cólera')
    hipertension = models.BooleanField(verbose_name='Hipertensión')
    cardiopatias = models.BooleanField(verbose_name='Cardiopatias')
    vih = models.BooleanField(verbose_name='VIH')
    otrosAntecedentes = models.TextField(verbose_name='Otros Antecedentes')
    antecedentesQuirurgicos = models.TextField(verbose_name='Antecedentes Quirúrgicos')
    padecimientosCronicos= models.TextField(verbose_name='Padecimiento Crónicos')
    alergias = models.TextField(verbose_name='Alergias')
#   Padecimientos actuales
    diarrea = models.BooleanField(verbose_name='Diarrea')
    infeccionesRespiratorias =models.BooleanField(verbose_name='Infecciones Respiratorias')
    fiebre=models.BooleanField(verbose_name='Fiebre')
    hemorragias = models.BooleanField(verbose_name='Hemorragias')
    nauseasVomito= models.BooleanField(verbose_name='Nauseas o Vomito')
    tos = models.BooleanField(verbose_name='Tos')
    dolores=models.BooleanField(verbose_name='Dolores')
    lesionesPiel = models.BooleanField(verbose_name='Lesiones en Piel')
    mareosVertigo=models.BooleanField(verbose_name='Mareos o Vertigo')
    tabaquismo=models.BooleanField(verbose_name='Tabaquismo')
    bebidasAlcoholicas = models.BooleanField(verbose_name='Bebidas Alcohólicas')
    toxicomanias = models.TextField(verbose_name='Toxicómanias')
    tipoDieta = models.CharField(max_length=50, verbose_name='Tipo de Dietas', choices=TIPO_DIETAS)
    sintomasCovid=models.TextField(verbose_name='Síntomas COVID')
    embarazo = models.BooleanField(verbose_name='Embarazo')
    tiempoEmbarazo=models.CharField(max_length=100, verbose_name='Tiempo Embarazo', null=True, blank=True)
    conclusionDiagnostica= models.TextField(verbose_name='Concision Diagnostica')
    observaciones =models.TextField(verbose_name='Observaciones')
    tratamiento = models.BooleanField(
        verbose_name='Tratamiento',
        choices=OPCIONES_BOOL,
        default=False,  # o True según tu preferencia predeterminada
    )
    class Meta:
        verbose_name_plural = "Certificados Medicos"

class CertificadoMedicoEgreso(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE, related_name='certificados_medicos_egreso')
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaHoraCertificado = models.DateTimeField(auto_now_add=True)
    tipoCertificado = models.CharField(verbose_name='Tipo Certificado', max_length=25, choices=OPCION_TIPO_CHOICES, default='INGRESO')
# Exploracion física
    temperatura = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Temperatura')
    frecuenciaRespiratoria = models.IntegerField(verbose_name='Frecuencia Respiratoria')
    presionArterialSistolica = models.IntegerField(verbose_name='Presión Arterial Sistólica')
    presionArterialDiastolica =models.IntegerField(verbose_name='Presión Arterial Diastólica')
    peso = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Peso')
    estatura = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Estatura')
    oxigenacionSaturacion = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Oxigenación Saturación')
    oxigenacionFrecuencia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Oxigenación Frecuencia')
    indiceMasaCorporal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Indice Masa Corporal')
# Antecedentes
    hepatitis = models.BooleanField(verbose_name='Hepatitis')
    tubercolisis = models.BooleanField(verbose_name='Tuberculosis')
    paludismo = models.BooleanField(verbose_name='Paludismo')
    dengue = models.BooleanField(verbose_name='Dengue')
    colera = models.BooleanField(verbose_name='Cólera')
    hipertension = models.BooleanField(verbose_name='Hipertensión')
    cardiopatias = models.BooleanField(verbose_name='Cardiopatias')
    vih = models.BooleanField(verbose_name='VIH')
    otrosAntecedentes = models.TextField(verbose_name='Otros Antecedentes')
    antecedentesQuirurgicos = models.TextField(verbose_name='Antecedentes Quirúrgicos')
    padecimientosCronicos= models.TextField(verbose_name='Padecimiento Crónicos')
    alergias = models.TextField(verbose_name='Alergias')
#   Padecimientos actuales
    diarrea = models.BooleanField(verbose_name='Diarrea')
    infeccionesRespiratorias =models.BooleanField(verbose_name='Infecciones Respiratorias')
    fiebre=models.BooleanField(verbose_name='Fiebre')
    hemorragias = models.BooleanField(verbose_name='Hemorragias')
    nauseasVomito= models.BooleanField(verbose_name='Nauseas o Vomito')
    tos = models.BooleanField(verbose_name='Tos')
    dolores=models.BooleanField(verbose_name='Dolores')
    lesionesPiel = models.BooleanField(verbose_name='Lesiones en Piel')
    mareosVertigo=models.BooleanField(verbose_name='Mareos o Vertigo')
    tabaquismo=models.BooleanField(verbose_name='Tabaquismo')
    bebidasAlcoholicas = models.BooleanField(verbose_name='Bebidas Alcohólicas')
    toxicomanias = models.TextField(verbose_name='Toxicómanias')
    tipoDieta = models.CharField(max_length=50, verbose_name='Tipo de Dietas', choices=TIPO_DIETAS)
    sintomasCovid=models.TextField(verbose_name='Síntomas COVID')
    embarazo = models.BooleanField(verbose_name='Embarazo')
    tiempoEmbarazo=models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Tiempo Embarazo', null=True, blank=True)
    conclusionDiagnostica= models.TextField(verbose_name='Concision Diagnostica')
    observaciones =models.TextField(verbose_name='Observaciones')
    tratamiento = models.TextField(verbose_name='Tratamiento')

    class Meta:
        verbose_name_plural = "Certificados Medicos Egreso"

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
LESIONES_BOOL = [
    (True, 'Sí'),
    (False, 'No'),
]
class constanciaNoLesiones(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    fechaHoraCertificado = models.DateTimeField(auto_now_add=True)
    presentaLesion = models.BooleanField(
        verbose_name='¿Presenta Lesiones?',
        choices=LESIONES_BOOL,
        default=False,  # o True según tu preferencia predeterminada
    )
    descripcion = models.TextField(verbose_name='Descripciones de las lesiones')
    class Meta:
        verbose_name_plural = "Constancias de no lesiones"

class ReferenciaMedica(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete= models.CASCADE)
    delaEstacion = models.ForeignKey(Estacion, on_delete= models.CASCADE)
    delMedico = models.ForeignKey(PerfilMedico, on_delete=models.CASCADE)
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE)
    fechaHoraReferencia = models.DateTimeField(auto_now_add=True)
    especialista = models.CharField(max_length=100,verbose_name='Especialidad medica')
    justificacion = models.TextField(max_length=100,verbose_name='Justificación de la referencia medica')
    class Meta:
        verbose_name_plural = "Referencias Medicas"

class DocumentosReferencia(models.Model):
    descripcion = models.TextField( verbose_name='Descripciones de documentos')
    documento = models.FileField(upload_to='files/', verbose_name='Documentos', null=True, blank=True)
    fechaHora = models.DateTimeField(auto_now_add=True)
    deReferencia = models.ForeignKey(ReferenciaMedica, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "Documentos"

class FirmaMedico(models.Model):
    medico = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firma_imagen = models.ImageField(upload_to='firmas/', blank=True, null=True)
    fechaHoraFirmaCreate = models.DateTimeField(auto_now_add=True)
    fechaHoraFirmaUpdate = models.DateTimeField(auto_now_add=True)

class DocumentosExternos(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    deLaEstacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)
    justificacion = models.CharField(max_length=100, verbose_name='Justificación')
    descripcion = models.TextField( verbose_name='Descripción del archivo')
    documento = models.FileField(upload_to='files/', verbose_name='Documentos', null=True, blank=True)
    fechaHora = models.DateTimeField(auto_now_add=True)
