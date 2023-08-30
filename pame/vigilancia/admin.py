from django.contrib import admin

from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionINM, PuestaDisposicionAC, Biometrico


class ExtranjeroAdmin(admin.ModelAdmin):
    list_display = ["fechaRegistro"]

admin.site.register(Extranjero, ExtranjeroAdmin)

admin.site.register(PuestaDisposicionINM)

admin.site.register(PuestaDisposicionAC)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad)

admin.site.register(Biometrico)
