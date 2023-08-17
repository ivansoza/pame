# from django import forms

# from .models import Puesta1, Puesta2

# class Puesta1Form(forms.ModelForm):
#     class Meta:
#         model = Puesta1
#         fields = ['numero_oficio', 'nombre_responsable', 'entidad']

# class Puesta2Form(forms.ModelForm):
#     class Meta:
#         model = Puesta2
#         fields = ['numero_oficio', 'nombre_responsable', 'entidad', 'pais']

from django import forms
from .models import PuestaGeneral, Complemento1, Complemento2

class PuestaGeneralForm(forms.ModelForm):
    class Meta:
        model = PuestaGeneral
        fields = '__all__'

class Complemento1Form(forms.ModelForm):
    class Meta:
        model = Complemento1
        fields = ['estado']

class Complemento2Form(forms.ModelForm):
    class Meta:
        model = Complemento2
        fields = ['municipio']