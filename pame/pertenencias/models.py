from django.db import models
from vigilancia.models import Extranjero
from catalogos.models import Estacion
from multiselectfield import MultiSelectField

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
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')
    cantidad = models.FloatField(verbose_name='Cantidad')
    Obsevaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')
    
    def __str__(self) -> str:
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Valores"

ENSERES = (
    ("Papel Higienico","Papel Higienico"),
    ("Kit Personal","Kit Personal"),
    ("Pañal Desechable","Pañal Desechable"),
    ("Toalla Sanitaria","Toalla Sanitaria"),
    ("Colchoneta","Colchoneta"),
    ("Manta Termica","Manta Termica"),
    ("Otros","Otros"),
)
class EnseresBasicos(models.Model):
    unidadMigratoria = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación Migratoria')
    fechaEntrega = models.DateField(verbose_name='Fecha Entrega', auto_now_add=True)
    horaEntrega = models.DateTimeField(verbose_name='Hora Entrega', auto_now_add=True)
    enseres = MultiSelectField(choices=ENSERES, max_length=200)
    enseresExtras = models.CharField(max_length=200, verbose_name='Enseres extras', blank=True, null= True, default='')
    noExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
