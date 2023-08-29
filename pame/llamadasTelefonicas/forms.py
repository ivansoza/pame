from django import forms
from .models import LlamadasTelefonicas

class LlamadasTelefonicasForm(forms.ModelForm):
    class Meta:
        model = LlamadasTelefonicas
        fields = '__all__'
        widgets = {
            # Otros campos y widgets
            'noExtranjero': forms.TextInput(attrs={'readonly': 'readonly'}),
        }