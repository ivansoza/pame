from django.contrib import admin

# from .models import Puesta1, Puesta2

# admin.site.register(Puesta1)
# admin.site.register(Puesta2)

from .models import PuestaGeneral, Complemento1, Complemento2


admin.site.register(PuestaGeneral)
admin.site.register(Complemento1)
admin.site.register(Complemento2)


