
from django import forms 
from .models import Traslado, ExtranjeroTraslado
from django.core.exceptions import ValidationError

class TrasladoForm(forms.ModelForm):
    
    class Meta:
        model = Traslado
        fields = ['numeroUnicoProceso', 'estacion_destino', 'nombreAutoridadEnvia', 'numero_camiones','tipo_de_traslado']
        widgets = { 
            'numeroUnicoProceso': forms.TextInput(attrs={'readonly':'readonly'}),
            'numero_camiones': forms.NumberInput(attrs={'min': '1', 'placeholder': 'Ingresa número de extranjeros'}),
            'tipo_de_traslado': forms.Select(attrs={'class':'form-control'}), # Añadir widget personalizado si lo deseas

        }

    def clean_numero_camiones(self):
        numero_camiones = self.cleaned_data.get('numero_camiones')
        
        if numero_camiones <= 0:
            raise ValidationError('El número de extranjeros debe ser mayor que 0.')
        
        return numero_camiones

# Formulario para poder cambiar de estacion 

class CambioEstacionForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['estacion_destino']
   

# Formulario para elegir que opcion hacer 
class DecisionForm(forms.Form):
    OPCIONES = (
        ('cambiar', 'Cambiar de Estación'),
        ('finalizar', 'Finalizar Proceso')
    )
    decision = forms.ChoiceField(choices=OPCIONES, widget=forms.RadioSelect)

class EstatusTrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['status', 'nombreAutoridadRecibe', 'motivo_rechazo']

class EstatusTrasladoFormOrigen(forms.ModelForm):
    status_traslado = forms.ChoiceField(
        choices=[(0, 'No iniciado'),(1, 'Iniciar Proceso'), (2, 'En Traslado')],
        widget=forms.Select()
    )

    class Meta:
        model = Traslado
        fields = ['status_traslado']

class EstatusTrasladoFormOrigenDestino(forms.ModelForm):
    status_traslado = forms.ChoiceField(
        choices=[(1, 'Iniciar Proceso'), (2, 'En Traslado')],
        widget=forms.Select()
    )

    class Meta:
        model = Traslado
        fields = ['status_traslado']


class EstatusTrasladoFormExtranjero(forms.ModelForm):
    class Meta:
        model = ExtranjeroTraslado
        fields = ['statusTraslado']


    