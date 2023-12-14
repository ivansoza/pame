# forms.py
from django import forms
from .models import Defensorias, notificacionesAceptadas,Relacion,Qrfirma, NotificacionConsular, FirmaNotificacionConsular
from .models import Defensorias, notificacionesAceptadas,Relacion, NotificacionConsular, FirmaNotificacionConsular, ExtranjeroDefensoria, firmasDefenso
from .models import Defensorias, notificacionesAceptadas,Relacion, NotificacionConsular, FirmaNotificacionConsular, NotificacionCOMAR, NotificacionFiscalia, FirmaNotificacionComar, FirmaNotificacionFiscalia,DocumentoRespuestaDefensoria,nombramientoRepresentante
from django.forms.widgets import HiddenInput

class DefensorForm(forms.ModelForm):
    class Meta:
        model = Defensorias
        fields = '__all__'
        widgets = {
            'nombreTitular': forms.TextInput(attrs={'placeholder': 'Ejemplo: Adrian '}),
            'apellidoPaternoTitular': forms.TextInput(attrs={'placeholder': 'Ejemplo:  Huerta '}),
            'apellidoMaternoTitular': forms.TextInput(attrs={'placeholder': 'Ejemplo: Garcia '}),
            'email1': forms.TextInput(attrs={'placeholder': 'Ejemplo: ejemplo@outlook.com.mx'}),
            'email2': forms.TextInput(attrs={'placeholder': 'Ejemplo: ejemplo@outlook.com.mx'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5518954598'}),
            'telefono2': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5518954598'}),
            'calle': forms.TextInput(attrs={'placeholder': 'Ejemplo: av xicohtencatl 102b'}),
            'colonia': forms.TextInput(attrs={'placeholder': 'Ejemplo: centro'}),
            'municipio': forms.TextInput(attrs={'placeholder': 'Ejemplo: San jose'}),
            'cp': forms.TextInput(attrs={'placeholder': 'Ejemplo:90300'}),
        }
        
        


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
            'delaEstacion': HiddenInput(),
            'nup': HiddenInput(),
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
   
class NotificacionComarForm(forms.ModelForm):
    class Meta:
        model = NotificacionCOMAR
        fields = ['delaEstacion', 'deComar', 'numeroOficio', 'nup', 'notificacionComar', 'delaComparecencia', 'delaAutoridad']
        widgets = {
            'delaEstacion': HiddenInput(),
            'nup': HiddenInput(),
            'delaComparecencia': HiddenInput(),
            # Puedes agregar más campos aquí si es necesario
        }
class FirmaAutoridadActuanteComarForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaNotificacionComar
        fields = ['firmaAutoridadActuante']

class NotificacionFiscaliaForm(forms.ModelForm):
    class Meta:
        model = NotificacionFiscalia
        fields = ['delaEstacion', 'nup','numeroOficio','delaFiscalia','delaComparecencia','condicion','delaAutoridad' ]
        widgets = {
            'delaEstacion': HiddenInput(),
            'nup': HiddenInput(),
            'delaComparecencia': HiddenInput(),
            # Puedes agregar más campos aquí si es necesario
        }

class FirmaAutoridadActuanteFiscaliaForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaNotificacionFiscalia
        fields = ['firmaAutoridadActuante']


    



class QrfirmaForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=Qrfirma
        fields = ['firmaAutoridadActuante']


class ExtranjeroDefensoriaForm(forms.ModelForm):
    class Meta:
        model  = ExtranjeroDefensoria
        fields = '__all__'

class firmasDefensoForms(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model=firmasDefenso
        fields = ['firmaAutoridadActuante']


class DocumentoRespuestaDefensoriaForm(forms.ModelForm):
    class Meta:
        model = DocumentoRespuestaDefensoria
        fields = ['archivo', 'descripcion']
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción del documento'}),
        }

    def __init__(self, *args, **kwargs):
        super(DocumentoRespuestaDefensoriaForm, self).__init__(*args, **kwargs)
        self.fields['archivo'].required = False


class NombramientoRepresentanteForm(forms.ModelForm):
    class Meta:
        model = nombramientoRepresentante
        fields = '__all__'
        widgets = {
            'oficio': forms.TextInput(attrs={'placeholder': 'Ingrese el número de oficio'}),
            'numeroExpediente': forms.TextInput(attrs={'placeholder': 'Ingrese el número de expediente'}),
            'representanteLegalExterno': forms.TextInput(attrs={'placeholder': 'Nombre del representante legal externo'}),
            'cedulaLegalExterno': forms.TextInput(attrs={'placeholder': 'Número de cédula del representante legal externo'}),
            'testigo1': forms.TextInput(attrs={'placeholder': 'Nombre completo del testigo 1'}),
            'testigo2': forms.TextInput(attrs={'placeholder': 'Nombre completo del testigo 2'}),
        }
    def __init__(self, *args, **kwargs):
            super(NombramientoRepresentanteForm, self).__init__(*args, **kwargs)
            self.fields['delaEstacion'].empty_label = "Seleccione una Estación"
            self.fields['nup'].empty_label = "Seleccione un NoProceso"
            self.fields['defensoria'].empty_label = "Seleccione una Defensoría"