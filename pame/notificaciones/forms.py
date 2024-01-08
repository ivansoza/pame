# forms.py
from django import forms
from .models import Defensorias, FirmaNombramientoExterno, FirmaNombramientoInterno,notificacionesAceptadas,Relacion,Qrfirma, NotificacionConsular, FirmaNotificacionConsular
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


class NombramientoRepresentanteExternoForm(forms.ModelForm):


    class Meta:
        model = nombramientoRepresentante
        fields = ['nup', 'autoridadActuante', 'representanteLegalExterno', 'grado_representante_externo', 'cedulaLegalExterno', 'traductor', 'testigo1', 'grado_academico_testigo1', 'testigo2', 'grado_academico_testigo2']
    
    def __init__(self, *args, **kwargs):
        super(NombramientoRepresentanteExternoForm, self).__init__(*args, **kwargs)
        self.fields['autoridadActuante'].empty_label = "Seleccione una Autoridad Actuante"
        self.fields['grado_representante_externo'].choices = [('','Seleccione el Grado Académico')] + list(self.fields['grado_representante_externo'].choices)[1:]
        self.fields['grado_academico_testigo1'].choices = [('','Seleccione el Grado Académico')] + list(self.fields['grado_representante_externo'].choices)[1:]
        self.fields['grado_academico_testigo2'].choices = [('','Seleccione el Grado Académico')] + list(self.fields['grado_representante_externo'].choices)[1:]
        self.fields['traductor'].empty_label= "Seleccione un Traductor"
        self.fields['autoridadActuante'].required = True 
        self.fields['representanteLegalExterno'].required = True  
        self.fields['representanteLegalExterno'].widget.attrs['placeholder']='Ejemplo: María Lopez'
        self.fields['cedulaLegalExterno'].widget.attrs['placeholder']='Ejemplo: 323232323234'
        self.fields['testigo1'].widget.attrs['placeholder']= 'Ejemplo: Juan Manuel Lopez'
        self.fields['testigo2'].widget.attrs['placeholder']='Ejemplo: Julio Cesar Munive'
# forms para firma de externo
            
class FirmaAutoridadActuanteNombramientoExternoForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoExterno
        fields = ['firmaAutoridadActuante']

class FirmaRepresentanteLegalNombramientoExternoForm(forms.ModelForm):
    firmaRepresentanteLegal = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoExterno
        fields = ['firmaRepresentanteLegal']

class FirmaTraductorNombramientoExternoForm(forms.ModelForm):
    firmaTraductor = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoExterno
        fields = ['firmaTraductor']
class FirmaTestigo1NombramientoExternoForm(forms.ModelForm):
    firmaTestigo1 = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoExterno
        fields = ['firmaTestigo1']

class FirmaTestigo2NombramientoExternoForm(forms.ModelForm):
    firmaTestigo2 = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoExterno
        fields = ['firmaTestigo2']

class FirmaExtranjeroNombramientoExternoForm(forms.ModelForm):
    firmaExtranjero = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoExterno
        fields = ['firmaExtranjero']


# forms para firma de interno 

class FirmaAutoridadActuanteNombramientoInternoForm(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoInterno
        fields = ['firmaAutoridadActuante']

class FirmaRepresentanteLegalNombramientoInternoForm(forms.ModelForm):
    firmaRepresentanteLegal = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoInterno
        fields = ['firmaRepresentanteLegal']

class FirmaTraductorNombramientoInternoForm(forms.ModelForm):
    firmaTraductor = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoInterno
        fields = ['firmaTraductor']
class FirmaTestigo1NombramientoInternoForm(forms.ModelForm):
    firmaTestigo1 = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoInterno
        fields = ['firmaTestigo1']

class FirmaTestigo2NombramientoInternoForm(forms.ModelForm):
    firmaTestigo2 = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoInterno
        fields = ['firmaTestigo2']

class FirmaExtranjeroNombramientoInternoForm(forms.ModelForm):
    firmaExtranjero = forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = FirmaNombramientoInterno
        fields = ['firmaExtranjero']