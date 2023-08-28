from django import forms
from .models import LlamadasTelefonicas

class LlamadasTelefonicasForm(forms.ModelForm):
    class Meta:
        model = LlamadasTelefonicas
        fields = '__all__'