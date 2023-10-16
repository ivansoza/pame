
from django import forms 
from .models import Traslado, ExtranjeroTraslado
from django.core.exceptions import ValidationError

class TrasladoForm(forms.ModelForm):
    
    class Meta:
        model = Traslado
        fields = ['numeroUnicoProceso', 'estacion_destino', 'nombreAutoridadEnvia', 'numero_camiones']
        widgets = { 
            'numeroUnicoProceso': forms.TextInput(attrs={'readonly':'readonly'}),
            'numero_camiones': forms.NumberInput(attrs={'min': '1'}),
        }

    def clean_numero_camiones(self):
        numero_camiones = self.cleaned_data.get('numero_camiones')
        
        if numero_camiones <= 0:
            raise ValidationError('El número de camiones debe ser mayor que 0.')
        
        return numero_camiones

class EstatusTrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['status', 'nombreAutoridadRecibe', 'motivo_rechazo']


class EstatusTrasladoFormExtranjero(forms.ModelForm):
    class Meta:
        model = ExtranjeroTraslado
        fields = ['statusTraslado']
    