from django.contrib import admin

from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionINM, PuestaDisposicionAC, Biometrico, PuestaDisposicionVP, Proceso, descripcion


class ExtranjeroAdmin(admin.ModelAdmin):
    list_display = ["fechaRegistro", "horaRegistro","numeroExtranjero","nombreExtranjero","apellidoPaternoExtranjero"]

admin.site.register(Extranjero, ExtranjeroAdmin)

admin.site.register(PuestaDisposicionINM)

admin.site.register(PuestaDisposicionAC)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad)

admin.site.register(Biometrico)

admin.site.register(PuestaDisposicionVP)

admin.site.register(Proceso)

admin.site.register(descripcion)