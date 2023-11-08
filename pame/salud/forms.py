from django import forms
from .models import CertificadoMedico, PerfilMedico

class certificadoMedicoForms(forms.ModelForm):
    class Meta:
        model = CertificadoMedico
        fields = '__all__'
    
class perfilMedicoforms(forms.ModelForm):
    class Meta:
        model = PerfilMedico
        fields = '__all__'

