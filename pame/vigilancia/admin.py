from django.contrib import admin

from .models import  OficioPuestaDisposicionINM, OficioPuestaDisposicionAC, Acompanante, Nacionalidad, Genero, ExtranjeroAC, ExtranjeroINM

# Register your models here.

admin.site.register(ExtranjeroAC)

admin.site.register(ExtranjeroINM)

admin.site.register(OficioPuestaDisposicionINM)

admin.site.register(OficioPuestaDisposicionAC)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad)

admin.site.register(Genero)