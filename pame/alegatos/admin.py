from django.contrib import admin
from .models import Alegatos, DocumentosAlegatos, FirmaAlegato, NoFirma, FirmasConstanciaNoFirma, presentapruebas
# Register your models here.
admin.site.register(Alegatos)
admin.site.register(DocumentosAlegatos)
admin.site.register(FirmaAlegato)
admin.site.register(NoFirma)
admin.site.register(FirmasConstanciaNoFirma)
admin.site.register(presentapruebas)