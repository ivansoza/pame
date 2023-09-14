from django import forms
from .models import LlamadasTelefonicas, Notificacion

class LlamadasTelefonicasForm(forms.ModelForm):
    class Meta:
        model = LlamadasTelefonicas
        fields = '__all__'
        widgets = {
            # Otros campos y widgets
            'noExtranjero': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class notifificacionLlamada(forms.ModelForm):
    class Meta:
        model = Notificacion
        fields = '__all__'
        widgets = {
            'deseaLlamar': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }