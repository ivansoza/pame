from django.db import models
from vigilancia.models import Extranjero
# Create your models here.

class Inventario(models.Model):
    foloInventario = models.CharField(max_length=30, verbose_name='Folio de Inventario')
    unidadMigratoria = models.CharField(max_length=30, verbose_name='Unidad Migratoria')
    fechaEntrega = models.DateField(verbose_name='Fecha Entrega', auto_now_add=True)
    horaEntrega = models.DateTimeField(verbose_name='Hora Entrega', auto_now_add=True)
    validacion = models.FileField(upload_to='files/',  null=True,blank=True,verbose_name='Documento de Validación')
    noExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.foloInventario

class Pertenencias(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='Descripcion')
    cantidad = models.FloatField(verbose_name='Cantidad')
    observaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Pertenencias"
class Valores(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='Descripcion')
    cantidad = models.FloatField(verbose_name='Cantidad')
    Obsevaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Valores"