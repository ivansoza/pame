from django.contrib import admin

# Register your models here.

from .models import PerfilMedico, Consulta, ConsultaExterna, RecetaMedica, DetalleTratamiento, CertificadoMedico, CertificadoExterno

admin.site.register(PerfilMedico)
admin.site.register(Consulta)
admin.site.register(ConsultaExterna)
admin.site.register(RecetaMedica)
admin.site.register(DetalleTratamiento)
admin.site.register(CertificadoMedico)
admin.site.register(CertificadoExterno)