from django import forms
from .models import Inventario, Pertenencias, Valores

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'
        widgets = {
            'noExtranjero': forms.TextInput(attrs={'readonly': 'readonly'}),
      }

class PertenenciaForm(forms.ModelForm):
    class Meta:
        model = Pertenencias
        fields = '__all__'
        


class ValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = '__all__'