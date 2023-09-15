from django import forms
from .models import Inventario, Pertenencias, Valores, EnseresBasicos

class InventarioForm(forms.ModelForm):
    # unidadMigratoria = forms.CharField(
    #      label= "Estación Migratoria" 
    #     ) 
    class Meta:
        model = Inventario
        fields = ['foloInventario', 'validacion']

    #     widgets = {
    #         'noExtranjero': forms.TextInput(attrs={'readonly': 'readonly'}),
    #   }

class PertenenciaForm(forms.ModelForm):
    class Meta:
        model = Pertenencias
        fields = '__all__'
        widgets = {
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'}),
      }
        
        


class ValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = '__all__'
        widgets = {
            'delInventario': forms.TextInput(attrs={'style': 'visibility:hidden;'}),
      }

class EnseresForm(forms.ModelForm):
    class Meta:
        model = EnseresBasicos
        fields = '__all__'
        widgets = {
            'unidadMigratoria': forms.TextInput(attrs={'readonly': 'readonly'}),
      }
