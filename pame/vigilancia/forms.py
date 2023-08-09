from django import forms

from .models import Extranjero, Acompanante, Nacionalidad, TipoDisposicion, PuestaDisposicion, ComplementoINM, ComplementonAC

class TipoDisposicionForm(forms.ModelForm):
    model = TipoDisposicion
    fields = '__all__'

class ComplementoINMForm(forms.ModelForm):
    model = ComplementoINM
    fields ='__all__'

class ComplementoACForm(forms.ModelForm):
    model = ComplementonAC
    fields ='__all__'
    