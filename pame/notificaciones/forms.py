# forms.py
from django import forms
from .models import Defensorias, notificacionesAceptadas

class DefensorForm(forms.ModelForm):
    class Meta:
        model = Defensorias
        fields = ['entidad', 'nombreTitular', 'apellidoPaternoTitular', 'apellidoMaternoTitular', 'cargoTitular', 'email1', 'email2', 'telefono', 'calle', 'colonia', 'municipio', 'cp']


class NotificacionesAceptadasForm(forms.ModelForm):
    class Meta:
        model = notificacionesAceptadas
        fields = '__all__'
