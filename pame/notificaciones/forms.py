# forms.py
from django import forms
from .models import Defensorias, notificacionesAceptadas,Relacion,Qrfirma, NotificacionConsular, FirmaNotificacionConsular

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



class NotificacionConsularForm(forms.ModelForm):
    class Meta:
        model = NotificacionConsular
        fields = ['delaEstacion', 'nup', 'numeroOficio', 'delConsulado', 'accion', 'delaAutoridad']
        widgets = {
            'delaEstacion': forms.Select(attrs={'placeholder': 'Seleccione Estación'}),
            'nup': forms.Select(attrs={'placeholder': 'Seleccione Número de Proceso'}),
            'numeroOficio': forms.TextInput(attrs={'placeholder': 'Número de Oficio'}),
            'delConsulado': forms.Select(attrs={'placeholder': 'Seleccione Consulado'}),
            'accion': forms.Select(attrs={'placeholder': 'Seleccione Acción'}),
            'delaAutoridad': forms.Select(attrs={'placeholder': 'Seleccione Autoridad Actuante'}),
        }


class FirmaAutoridadActuanteConsuladoForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaNotificacionConsular
        fields = ['firmaAutoridadActuante']




class QrfirmaForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=Qrfirma
        fields = ['firmaAutoridadActuante']