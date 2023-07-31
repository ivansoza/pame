from django.contrib import admin

from .models import Extranjero, OficioPuestaDisposicionINM, OficioPuestaDisposicionAC, Acompanante

# Register your models here.

admin.site.register(Extranjero)

admin.site.register(OficioPuestaDisposicionINM)

admin.site.register(OficioPuestaDisposicionAC)

admin.site.register(Acompanante)