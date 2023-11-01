from django.db import models
from vigilancia.models import Extranjero, NoProceso

# Create your models here.

class ExpedienteMedico(models.Model):
    fecha_consulta = models.DateField()
    sintomas = models.TextField()
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    observaciones = models.TextField()


    class Meta:
        verbose_name_plural = "Expedientes Medicos"

class Patologicos(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    hepatitis = models.BooleanField()
    tuberculosis= models.BooleanField() 
    paludismo= models.BooleanField() 
    dengue= models.BooleanField() 
    colera= models.BooleanField() 
    diabetes= models.BooleanField() 
    hipertension= models.BooleanField() 
    cardiopatias= models.BooleanField() 
    vih= models.BooleanField() 
    otrosAntecedentes= models.TextField() 
    antecedentesQuirurgicos= models.TextField() 
    padecimientosCronicos= models.TextField() 
    alergias= models.TextField() 

    class Meta:
        verbose_name_plural = 'Datos Patologicos'

class ExploracionFisica(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    temperatura = models.DecimalField(decimal_places=2, max_digits=10)
    frecuenciaRespiratoria: models.IntegerField()
    presionArterialSistolica: models.IntegerField() 
    presionArterialDiatolica: models.IntegerField() 
    peso: models.DecimalField(decimal_places=2) 
    estatura: models.DecimalField(decimal_places=2) 
    oxigenacionSaturacion: models.DecimalField(decimal_places=2) 
    oxigenacionFrecuencia: models.DecimalField(decimal_places=2) 
    indiceMasaCorporal: models.DecimalField(decimal_places=2)

    class Meta:
        verbose_name_plural = 'Exploración Fisica'

class PadecimientoActual(models.Model):
    extranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
    diarrea= models.BooleanField() 
    infeccionesRespiratoria= models.BooleanField() 
    fiebre= models.BooleanField() 
    hemorragias= models.BooleanField() 
    bebidasAlcoholicas= models.BooleanField() 
    toxicomanias= models.BooleanField() 
    nauseaVomito= models.BooleanField() 
    tos= models.BooleanField() 
    dolores= models.BooleanField() 
    lesionesenPiel= models.BooleanField() 
    mareosVertigo= models.BooleanField() 
    tabaquismo= models.BooleanField() 
    tipoDieta = models.CharField(max_length=100) 
    sintomasCovid = models.TextField() 
    embarazo= models.BooleanField() 
    tiempoEmbarazo = models.DecimalField(decimal_places=2, max_digits=10) 
    conclusionDiagnostica = models.TextField() 
    observaciones = models.TextField() 

    class Meta:
        verbose_name_plural = 'Padecimientos Actuales'