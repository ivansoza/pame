
from django import forms 
from .models import Traslado
class TrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['numeroUnicoProceso', 'estacion_destino', 'nombreAutoridadEnvia']
        widgets={ 
            'numeroUnicoProceso':forms.TextInput(attrs={'readonly':'readonly'}),
        }



class EstatusTrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['status']
       