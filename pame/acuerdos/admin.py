from django.contrib import admin
from .models import TipoAcuerdo, Acuerdo, PDFGenerado

admin.site.register(TipoAcuerdo)

admin.site.register(Acuerdo)

admin.site.register(PDFGenerado)