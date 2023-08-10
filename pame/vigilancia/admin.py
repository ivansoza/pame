from django.contrib import admin

<<<<<<< HEAD
from .models import Extranjero, Acompanante, Nacionalidad, TipoDisposicion, PuestaDisposicion, ComplementoINM, ComplementonAC
=======
from .models import  OficioPuestaDisposicionINM, OficioPuestaDisposicionAC, Acompanante, Nacionalidad, Genero, ExtranjeroAC, ExtranjeroINM
>>>>>>> origin/jose

# Register your models here.

admin.site.register(ExtranjeroAC)

admin.site.register(ExtranjeroINM)

admin.site.register(TipoDisposicion)

admin.site.register(PuestaDisposicion)

admin.site.register(Acompanante)

admin.site.register(Nacionalidad)

admin.site.register(ComplementonAC)

admin.site.register(ComplementoINM)
