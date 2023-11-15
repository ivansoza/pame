from django import forms
from .models import CertificadoMedico, PerfilMedico, CertificadoMedicoEgreso, Consulta, constanciaNoLesiones, ReferenciaMedica, OPCIONES_BOOL, LESIONES_BOOL, REFERENCIA_BOOL
from .models import DocumentosReferencia, FirmaMedico
from .widgets import ClearableMultipleFilesInput
from .fields import MultipleFilesField
class certificadoMedicoForms(forms.ModelForm):
    tratamiento = forms.ChoiceField(
        label='¿El extranjero requiere tratamiento?',
        choices=OPCIONES_BOOL,
        widget=forms.RadioSelect,  # Puedes usar CheckboxInput si prefieres una casilla de verificación
    )

    class Meta:
        model = CertificadoMedico
        fields = '__all__'
    
class perfilMedicoforms(forms.ModelForm):
    class Meta:
        model = PerfilMedico
        fields = '__all__'

class certificadoMedicoEgresoForms(forms.ModelForm):
    class Meta:
        model = CertificadoMedicoEgreso
        fields = '__all__'

class consultaForms(forms.ModelForm):
    tratamiento = forms.CharField(
        label='Tratamiento',
        widget=forms.Textarea(attrs={'rows': 9, 'cols': 40}),
        help_text='Separar tratamiento he instrucciones del mismo por una (,)'
    )
    referencia = forms.ChoiceField(
        label='¿El extranjero requiere referencia Medica?',
        choices=REFERENCIA_BOOL,
        widget=forms.RadioSelect,
    )
    class Meta:
        model = Consulta
        fields = '__all__'

class lesionesForm(forms.ModelForm):
    presentaLesion = forms.ChoiceField(
        label='¿El extranjero presenta lesiones?',
        choices=LESIONES_BOOL,
        widget=forms.RadioSelect,
    )
    class Meta:
        model = constanciaNoLesiones
        fields = '__all__'

class referenciaMedicaforms(forms.ModelForm):
    class Meta:
        model = ReferenciaMedica
        fields = '__all__'
class MultipleFilesField(forms.FileField):
    def to_python(self, value):
        return value


class DocumentosReferenciaForm(forms.ModelForm):
    documento = MultipleFilesField(
    widget=ClearableMultipleFilesInput(
        attrs={'multiple': True}), help_text='Puede subir más de un archivo')
    class Meta:
        model = DocumentosReferencia
        fields = ['descripcion','documento','deReferencia']

class FirmaMedicoForm(forms.ModelForm):
    firma_imagen = forms.CharField(widget=forms.HiddenInput()) # Esto es para la cadena dataURL

    class Meta:
        model = FirmaMedico
        fields = ['firma_imagen']