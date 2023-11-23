# forms.py
from django import forms
from .models import Defensorias, notificacionesAceptadas,Relacion

class DefensorForm(forms.ModelForm):
    class Meta:
        model = Defensorias
        fields = ['entidad', 'nombreTitular', 'apellidoPaternoTitular', 'apellidoMaternoTitular', 'cargoTitular', 'email1', 'email2', 'telefono', 'calle', 'colonia', 'municipio', 'cp']


class NotificacionesAceptadasForm(forms.ModelForm):
    class Meta:
        model = notificacionesAceptadas
        fields = '__all__'


class modalnotificicacionForm(forms.ModelForm):
    class Meta:
        model = Relacion
        fields = ['extranjero','nup','defensoria','firma','autoridad_actuante']
        widgets = {
            'firma': forms.ClearableFileInput(attrs={'multiple': True}),
        }