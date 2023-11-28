from django.contrib import admin

from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionINM, PuestaDisposicionAC, Biometrico, PuestaDisposicionVP, Proceso, UserFace, NoProceso, descripcion, Firma, AsignacionRepresentante

class ExtranjeroAdmin(admin.ModelAdmin):
    list_display = ["fechaRegistro", "horaRegistro","numeroExtranjero","nombreExtranjero","apellidoPaternoExtranjero"]

class NacionalidadAdmin(admin.ModelAdmin):
    list_display = ['identificador', 'nombre', 'Abreviatura']

admin.site.register(Extranjero, ExtranjeroAdmin)

admin.site.register(PuestaDisposicionINM)

admin.site.register(PuestaDisposicionAC)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad, NacionalidadAdmin)

admin.site.register(Biometrico)

admin.site.register(PuestaDisposicionVP)

admin.site.register(Proceso)

admin.site.register(UserFace)

admin.site.register(descripcion)

admin.site.register(NoProceso)

admin.site.register(Firma)
admin.site.register(AsignacionRepresentante)

