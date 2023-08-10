from django.contrib import admin

from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionINM, PuestaDisposicionAC

admin.site.register(Extranjero)

admin.site.register(PuestaDisposicionINM)

admin.site.register(PuestaDisposicionAC)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad)

