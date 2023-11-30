# forms.py
from django import forms
from .models import Defensorias, notificacionesAceptadas,Relacion

class DefensorForm(forms.ModelForm):
    class Meta:
        model = Defensorias
        fields = '__all__'


class NotificacionesAceptadasForm(forms.ModelForm):
    class Meta:
        model = notificacionesAceptadas
        fields = '__all__'


class modalnotificicacionForm(forms.ModelForm):
    class Meta:
        model = Relacion
        fields = ['extranjero','nup','defensoria']
    