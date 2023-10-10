from django import forms
from .models import Inventario, Pertenencias, Valores, EnseresBasicos, Pertenencia_aparatos, valoresefectivo, valoresjoyas, documentospertenencias

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
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
            'observaciones': forms.TextInput(attrs={'placeholder': 'Observaciones'}),
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'}),
        }
        
class EditPertenenciaForm(forms.ModelForm):
    class Meta:
        model = Pertenencias
        fields = ['equipaje','cantidad','color','observaciones']
        
        
class pertenenciaselectronicasForm(forms.ModelForm):
    class Meta:
        model = Pertenencia_aparatos
        fields = '__all__'
        widgets ={
            'electronicos': forms.TextInput(attrs={'placeholder': 'Electronicos'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
            'marca': forms.TextInput(attrs={'placeholder': 'Marca'}),
            'serie': forms.TextInput(attrs={'placeholder': 'Serie'}),
            'observaciones': forms.TextInput(attrs={'placehoolder': 'Observaciones'}),
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'})
        }
  
class EditarelectronicosForm(forms.ModelForm):
    class Meta:
        model = Pertenencia_aparatos
        fields = '__all__'
        
        
# aqui empiezan los formularios de valores efectivo -----------------<>>>>>
class valoresefectivoForm(forms.ModelForm):
    class Meta:
        model = valoresefectivo
        fields = '__all__'
        widgets ={
            'importe': forms.NumberInput(attrs={'placeholder': 'Importe'}),
            'moneda': forms.TextInput(attrs={'placeholder': 'Moneda'}),
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'})
        }
  
class EditarelectronicosForm(forms.ModelForm):
    class Meta:
        model = valoresefectivo
        fields = ['importe', 'moneda']
        
        
        
# aqui terminan los formularios de valores joyas ---------------->>>>>>
class valorejoyasForm(forms.ModelForm):
    class Meta:
        model = valoresjoyas
        fields = '__all__'
        widgets ={
            'metal': forms.TextInput(attrs={'placeholder': 'Metal'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripcion'}),
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'})
        }
  
class valorejoyasForm(forms.ModelForm):
    class Meta:
        model = valoresjoyas
        fields = ['metal', 'descripcion']
# aqui terminan los formularios de valores joyas ---------------->>>>>>



# aqui empieza los formularios de valores documentospertenencias ---------------->>>>>>
class documentospertenenciasForm(forms.ModelForm):
    class Meta:
        model = documentospertenencias
        fields = '__all__'
        widgets ={
            'tipodocumento': forms.TextInput(attrs={'placeholder': 'Tipodocumento'}),
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripcion'}),
            'delInventario': forms.TextInput(attrs={'style': 'display:none;'})
        }
  
class documentospertenenciasForm(forms.ModelForm):
    class Meta:
        model = documentospertenencias
        fields = ['tipodocumento', 'descripcion']
# aqui terminan los formularios de valores documentos pertenencias ---------------->>>>>>


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
        fields = ['enseres','enseresExtras','nup']
      