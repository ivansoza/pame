from django import forms
from .models import CertificadoMedico

class certificadoMedicoForms(forms.ModelForm):
    class Meta:
        model = CertificadoMedico
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(certificadoMedicoForms, self).__init__(*args, **kwargs)
        for campo in self.fields:
            self.fields[campo].widget.attrs['disabled'] = 'disabled'

