from django.contrib import admin

# Register your models here.

from .models import ExpedienteMedico, Patologicos


admin.site.register(ExpedienteMedico)
admin.site.register(Patologicos)