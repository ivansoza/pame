from django import forms
from .models import Acuerdo, FirmaAcuerdo

class AcuerdoInicioForm(forms.ModelForm):
    class Meta:
        model = Acuerdo
        fields = [
            'nombreTestigoUno',
            'apellidoPaternoTestigoUno',
            'apellidoMaternoTestigoUno',
            'nombreTestigoDos',
            'apellidoPaternoTestigoDos',
            'apellidoMaternoTestigoDos',
        ]
        widgets = {
            'nombreTestigoUno': forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan'}),
            'apellidoPaternoTestigoUno': forms.TextInput(attrs={'placeholder': 'Ejemplo: Pérez'}),
            'apellidoMaternoTestigoUno': forms.TextInput(attrs={'placeholder': 'Ejemplo: Rodriguez'}),
            'nombreTestigoDos': forms.TextInput(attrs={'placeholder': 'Ejemplo: Ana'}),
            'apellidoPaternoTestigoDos': forms.TextInput(attrs={'placeholder': 'Ejemplo: López'}),
            'apellidoMaternoTestigoDos': forms.TextInput(attrs={'placeholder': 'Ejemplo: Morales'}),
        }

class FirmaTestigoUnoForm(forms.ModelForm):
    class Meta:
        model = FirmaAcuerdo
        fields = ["firmaTestigoUno"]

class FirmaTestigoDosForm(forms.ModelForm):
    class Meta:
        model = FirmaAcuerdo
        fields = ["firmaTestigoDos"]