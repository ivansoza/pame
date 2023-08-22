from django import forms
from .models import Inventario, Pertenencias

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'

class PertenenciaForm(forms.ModelForm):
    class Meta:
        model = Pertenencias
        fields = '__all__'


