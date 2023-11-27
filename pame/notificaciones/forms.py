# forms.py
from django import forms
from .models import Defensorias, notificacionesAceptadas,Relacion,Qrfirma

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
        fields = ['extranjero','nup','defensoria','autoridad_actuante']


class QrfirmaForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=Qrfirma
        fields = ['firmaAutoridadActuante']