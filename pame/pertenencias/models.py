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
COLORES_CHOICES = [
        ('Rojo', 'Rojo'),
        ('Azul', 'Azul'),
        ('Verde', 'Verde'),
        ('Amarillo', 'Amarillo'),
        ('Naranja', 'Naranja'),
        ('Morado', 'Morado'),
        ('Rosa', 'Rosa'),
        ('Blanco', 'Blanco'),
        ('Negro', 'Negro'),
        ('Gris', 'Gris'),
    ]
class Pertenencias(models.Model):
    equipaje = models.CharField(max_length=100, verbose_name='Equipaje')
    cantidad = models.FloatField(verbose_name='Cantidad')
    color = models.CharField(max_length=50, verbose_name='Color', choices=COLORES_CHOICES)
    observaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "Pertenencias"
        
# aqui empiezan los modales ------->>>>>>>>>>
class Pertenencia_aparatos(models.Model):# pentenencias electronicas ----------------->>>>>>
    electronicos = models.CharField(max_length=100, verbose_name='Electronicos')
    cantidad = models.FloatField(verbose_name='Cantidad')
    marca = models.CharField(max_length=100, verbose_name='Marca')
    serie = models.CharField(max_length=100, verbose_name='Serie')
    observaciones = models.CharField(max_length=100, verbose_name='Observaciones')
    delInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "pertenenecia_aparatos"
        

class valoresefectivo(models.Model): #modales para el efectivo ------------>>>
    importe = models.FloatField(max_length=100, verbose_name='Importe')
    moneda = models.CharField(max_length=100, verbose_name='Moneda')
    delInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "valoresefectivo"
        
class valoresjoyas(models.Model): # valores de joyas y otros -------->>>>>>>
    metal = models.CharField(max_length=100, verbose_name='Metal')
    descripcion = models.CharField(max_length=300, verbose_name='Descripcion')
    delInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero del Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "valoresjoyas"
    
class documentospertenencias(models.Model): #docuemntos del extranjero ------------------->>>>>>>>>
    tipodocumento = models.CharField(max_length=200, verbose_name='Tipodocumento')
    descripcion = models.CharField(max_length=300, verbose_name='Descripcion')
    delInventario = models.ForeignKey(Inventario,on_delete=models.CASCADE, verbose_name='Numero del Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "documentospertenencias"
    
# aqui terminan los modales ---------->>>>>

        
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
