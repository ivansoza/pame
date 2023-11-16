from django.db import models
from vigilancia.models import Extranjero, NoProceso
from catalogos.models import Estacion
from multiselectfield import MultiSelectField

class Inventario(models.Model):
    foloInventario = models.CharField(max_length=30, verbose_name='Folio de Inventario')
    unidadMigratoria = models.CharField(max_length=30, verbose_name='Unidad Migratoria')
    fechaEntrega = models.DateField(verbose_name='Fecha Entrega', auto_now_add=True)
    horaEntrega = models.DateTimeField(verbose_name='Hora Entrega', auto_now_add=True)
    validacion = models.FileField(upload_to='files/',  null=True,blank=True,verbose_name='Documento de Validación')
    noExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)

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
        
        
MONEDAS_CHOICES = (
    ('USD', 'Dólar estadounidense'),
    ('EUR', 'Euro'),
    ('GBP', 'Libra esterlina británica'),
    ('JPY', 'Yen japonés'),
    ('CAD', 'Dólar canadiense'),
    ('AUD', 'Dólar australiano'),
    ('CHF', 'Franco suizo'),
    ('NZD', 'Dólar neozelandés'),
    ('SEK', 'Corona sueca'),
    ('NOK', 'Corona noruega'),
    ('SGD', 'Dólar singapurense'),
    ('CNY', 'Yuan chino'),
    ('INR', 'Rupia india'),
    ('MXN', 'Peso mexicano'),
    ('HKD', 'Dólar hongkonés'),
    ('RUB', 'Rublo ruso'),
    ('TRY', 'Lira turca'),
    ('BRL', 'Real brasileño'),
    ('ZAR', 'Rand sudafricano'),
    ('ARS', 'Peso argentino'),
)


class valoresefectivo(models.Model): #modales para el efectivo ------------>>>
    importe = models.FloatField(max_length=100, verbose_name='Importe')
    moneda = models.CharField(max_length=100, verbose_name='Moneda', choices=MONEDAS_CHOICES)
    delInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero de Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "valoresefectivo"


METALES_CHOICES = (
    ('Oro', 'Oro'),
    ('Plata', 'Plata'),
    ('Platino', 'Platino'),
    ('Paladio', 'Paladio'),
    ('Titanio', 'Titanio'),
    ('Acero inoxidable', 'Acero inoxidable'),
    ('Latón', 'Latón'),
    ('Bronce', 'Bronce'),
    ('Cobre', 'Cobre'),
    ('Aluminio', 'Aluminio'),
    ('Aleación de níquel', 'Aleación de níquel'),
    ('Plata de ley', 'Plata de ley'),
    ('Aleación de oro', 'Aleación de oro'),
    ('Oro blanco', 'Oro blanco'),
    ('Oro rosa', 'Oro rosa'),
    ('Oro amarillo', 'Oro amarillo'),
    ('Oro verde', 'Oro verde'),
    ('Oro negro', 'Oro negro'),
)

class valoresjoyas(models.Model): # valores de joyas y otros -------->>>>>>>
    metal = models.CharField(max_length=100, verbose_name='Metal', choices=METALES_CHOICES)
    descripcion = models.CharField(max_length=300, verbose_name='Descripcion')
    delInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Numero del Inventario')
    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "valoresjoyas"
    
class documentospertenencias(models.Model):  # Documentos del extranjero
    tipodocumento = models.CharField(max_length=200, verbose_name='Tipo de documento')
    descripcion = models.CharField(max_length=300, verbose_name='Descripción')
    delInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Número del inventario')

    def __str__(self) -> str:
        return '__all__'
    
    class Meta:
        verbose_name_plural = "documentospertenencias"
    
# aqui terminan los modales ---------->>>>>
class Valores(models.Model):
    descripcion = models.CharField(max_length=100, verbose_name='Descripción')
    cantidad = models.FloatField(verbose_name='Cantidad')
    Obsevaciones = models.CharField(max_length=100, verbose_name='Obervaciones')
    delInventario =models.ForeignKey(Inventario, on_delete=models.CASCADE, verbose_name='Número de Inventario')
    
    def __str__(self) -> str:
        return self.descripcion
    
    class Meta:
        verbose_name_plural = "Valores"

ENSERES = (
    ("Papel Higiénico","Papel Higiénico"),  # Añadido acento en "Higiénico"
    ("Kit Personal","Kit Personal"),
    ("Pañal Desechable","Pañal Desechable"),  # Añadido acento en "Pañal"
    ("Toalla Sanitaria","Toalla Sanitaria"),
    ("Colchoneta","Colchoneta"),
    ("Manta Térmica","Manta Térmica"),  # Añadido acento en "Térmica"
    ("Otros","Otros"),
)
class EnseresBasicos(models.Model):
    unidadMigratoria = models.ForeignKey(Estacion, on_delete=models.CASCADE, verbose_name='Estación Migratoria')
    fechaEntrega = models.DateField(verbose_name='Fecha Entrega', auto_now_add=True)
    horaEntrega = models.DateTimeField(verbose_name='Hora Entrega', auto_now_add=True)
    enseres = MultiSelectField(choices=ENSERES, max_length=200)
    enseresExtras = models.CharField(max_length=200, verbose_name='Enseres extras', blank=True, null= True, default='')
    noExtranjero = models.ForeignKey(Extranjero, on_delete=models.CASCADE)
    nup = models.ForeignKey(NoProceso, on_delete=models.CASCADE)
