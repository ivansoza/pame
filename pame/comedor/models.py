from django.db import models
# Create your models here.

# Create your models here.

class TipoDieta(models.Model):
    nombre = models.CharField(max_length=200,verbose_name='Nombre de Dieta')
    caracteristicas = models.TextField(verbose_name='Caracteristicas de la Dieta')
    region = models.CharField(max_length=200,verbose_name='Región de donde proviene')

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Tipos de Dietas"
    
class Dietas(models.Model):
    tipoDieta = models.ForeignKey(TipoDieta, on_delete=models.CASCADE, verbose_name='Tipo de Dieta')
    
    
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Dietas"



class Comedor(models.Model):
    fechaEvento = models.DateField(verbose_name='Fecha Evento')
    horaEvento = models.DateTimeField(verbose_name='Hora Evento')
    comida = models.BooleanField(verbose_name='Comida')
    desayuno = models.BooleanField(verbose_name='Desayuno')
    cena = models.BooleanField(verbose_name='Cena')
    firmaExtranjero = models.BinaryField(verbose_name='Firma del Extranjero')
    huellaExtranjero = models.BinaryField(verbose_name='Huella del Extranjero')
   

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Comedores"
    

class BoxLunch(models.Model):
    fechaEvento = models.DateField(verbose_name='Fecha Evento')
    horaEvento = models.DateTimeField(verbose_name='Fecha Evento')
    firmaResponsable = models.BinaryField(verbose_name='Firma del Responsable')
    huellaResponsable=models.BinaryField(verbose_name='Huella del Responsable')
    

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Box Lunches"
    