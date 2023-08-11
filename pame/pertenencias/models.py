from django.db import models

# Create your models here.

class Inventario(models.Model):
    unidadMigratoria = models.CharField(max_length=30, verbose_name='Unidad Migratoria')
    fechaEntrega = models.DateField(verbose_name='Fecha Entrega')
    horaEntrega = models.DateTimeField(verbose_name='Hora Entrega')
  

    def __str__(self) -> str:
        return '__all__'

class Pertenencias(models.Model):
    descripcion = models.DateField(max_length=100, verbose_name='Descripcion')
    cantidad = models.FloatField(verbose_name='Cantidad')
    observaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Pertenencias"
class Valores(models.Model):
    descripcion = models.DateField(max_length=100, verbose_name='Descripcion')
    cantidad = models.FloatField(verbose_name='Cantidad')
    Obsevaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Valores"