from django import forms
from .models import Acuerdo


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