from django.contrib import admin
from .models import Inventario, Pertenencias, Valores
# Register your models here.

admin.site.register(Inventario)

admin.site.register(Pertenencias)

admin.site.register(Valores)