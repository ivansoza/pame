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
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
            'observaciones': forms.TextInput(attrs={'placeholder': 'Observaciones'}),
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'}),
        }
        
class EditPertenenciaForm(forms.ModelForm):
    class Meta:
        model = Pertenencias
        fields = ['descripcion','cantidad','observaciones']
  
        


class ValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = '__all__'
        widgets = {
            'delInventario': forms.TextInput(attrs={'style': 'visibility:hidden;'}),
      }


class EditarValoresForm(forms.ModelForm):
    class Meta:
        model = Valores
        fields = ['descripcion','cantidad','Obsevaciones']
      


class EnseresForm(forms.ModelForm):
    class Meta:
        model = EnseresBasicos
        fields = ['enseres','enseresExtras']
      