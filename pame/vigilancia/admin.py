from django.contrib import admin

from .models import Extranjero, Acompanante, Nacionalidad, TipoDisposicion, PuestaDisposicion, ComplementoINM, ComplementonAC

# Register your models here.

admin.site.register(Extranjero)

admin.site.register(TipoDisposicion)

admin.site.register(PuestaDisposicion)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad)

admin.site.register(ComplementonAC)

admin.site.register(ComplementoINM)
