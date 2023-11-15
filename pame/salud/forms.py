from django import forms
from .models import CertificadoMedico, PerfilMedico, CertificadoMedicoEgreso, Consulta, constanciaNoLesiones, OPCIONES_BOOL, LESIONES_BOOL

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