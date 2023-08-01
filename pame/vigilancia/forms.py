from django import forms
from .models import OficioPuestaDisposicionINM

class OficioPuestaDisposicionINMform(forms.ModelForm):
    class Meta:
        model = OficioPuestaDisposicionINM
        fields = ['numeroOficio', 'fechaOficio', 'nombreAutoridadSigna', 'cargoAutoridadSigna',
                  'puntoRevision', 'oficioPuesta', 'oficioComision', 'delExtranjero']
        labels = {
            'numeroOficio':'Numero de Oficio',
            'fechaOficio':'Fecha',
            'nombreAutoridadSigna':"Nombre de Autoridad Asignada",
            'cargoAutoridadSigna':'Cargo de autoridad Asignada',
            'puntoRevision':'Punto de Revision',
            'oficioPuesta':'Oficio Puesta a Disposicion',
            'oficioComision':'Oficio Comision',
            'delExtranjero':'Numero del Extranjero',
        }
        widgets = {
            'numeroOficio': forms.TextInput(
                attrs={
                    'placeholder':'Numero de Oficio'
                }
            ),
            'nombreAutoridadSigna': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el nombre de la Autoridad Asignada'
                }
            ),
            'cargoAutoridadSigna': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Cargo de la Autoridad'
                }
            ),
            'puntoRevision': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Punto de Revision'
                }
            ),
            'oficioPuesta': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Numero De oficio'
                }
            ),
            'oficioComision': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Numero de Comision'
                }
            )
        }

    def clean_numeroOficio(self):
        data = self.cleaned_data['numeroOficio']
        if not data.isdigit():
            raise forms.ValidationError('Solo debe contener numeros')
        return data
    
    def clean_oficioPuesta(self):
        data = self.cleaned_data['oficioPuesta']
        if not data.isdigit():
            raise forms.ValidationError('Solo debe contener numeros')
        return data
    
    def clean_oficioComision(self):
        data = self.cleaned_data['oficioComision']
        if not data.isdigit():
            raise forms.ValidationError('Solo debe contener numeros')
        return data