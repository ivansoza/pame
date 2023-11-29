from django.contrib import admin

# Register your models here.

from .models import PerfilMedico, Consulta, ConsultaExterna, RecetaMedica, DetalleTratamiento, CertificadoMedico, CertificadoExterno, ReferenciaMedica, DocumentosReferencia, FirmaMedico, \
    constanciaNoLesiones

admin.site.register(PerfilMedico)
admin.site.register(Consulta)
admin.site.register(ConsultaExterna)
admin.site.register(RecetaMedica)
admin.site.register(DetalleTratamiento)
admin.site.register(CertificadoMedico)
admin.site.register(CertificadoExterno)
admin.site.register(ReferenciaMedica)
admin.site.register(DocumentosReferencia)
admin.site.register(FirmaMedico)
admin.site.register(constanciaNoLesiones)

