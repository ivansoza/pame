from django import forms
from .models import comidasAsignadas

class validacioncomedor(forms.ModelForm):
    class Meta:
        model = comidasAsignadas
        fields = '__all__'