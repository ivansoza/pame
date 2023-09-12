
from django import forms 
from .models import Traslado
class TrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['numeroUnicoProceso', 'estacion_origen', 'estacion_destino', 'nombreAutoridadEnvia']