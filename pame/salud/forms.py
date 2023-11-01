from django import forms
from .models import Patologicos, ExploracionFisica, PadecimientoActual, ExpedienteMedico

class patlogicosForms(forms.ModelForm):
    class Meta:
        model = Patologicos
        fields = '__all__'


class exploracionFisicaForms(forms.ModelForm):
    class Meta:
        model = ExploracionFisica
        fields = '__all__'

class padecimientoActualForms(forms.ModelForm):
    class Meta:
        model = PadecimientoActual
        fields = '__all__'