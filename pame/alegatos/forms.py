from django import forms
from .models import Alegatos, DocumentosAlegatos, FirmaAlegato, NoFirma, FirmasConstanciaNoFirma, presentapruebas

class ValidacionArchivos(forms.Form):
    def clean_archivo(self, field_name):
        archivo = self.cleaned_data.get(field_name)
        if archivo:
            # Validar por tipo de archivo
            nombre_archivo = archivo.name
            extension = nombre_archivo.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png', 'pdf']:
                raise forms.ValidationError(f'El documento debe ser JPG, PNG o PDF.')
            
            # Validar por tamaño de archivo, menor a 1 MB
            max_tamano = 1024 * 1024 # 1 MB en bytes
            if archivo.size > max_tamano:
                raise forms.ValidationError(f'El documento debe ser menor de 1 MB.')
            
        return archivo
    
class AlegatosForms(forms.ModelForm):
    class Meta:
        model = Alegatos
        fields = '__all__'

class DocumentosAlegatosForms(forms.ModelForm, ValidacionArchivos):
    def clean_oficioPuesta(self):
        return self.clean_archivo('documento')
    class Meta:
        model = DocumentosAlegatos
        fields = '__all__'

class FirmaAutoridadActuanteForm1(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaAlegato
        fields = ['firmaAutoridadActuante']

class FirmaRepresentanteLegalForm1(forms.ModelForm):
    firmaRepresentanteLegal = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaAlegato
        fields = ['firmaRepresentanteLegal']
    
class FirmaTestigoForm1(forms.ModelForm):
    firmaTestigo1 = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaAlegato
        fields = ['firmaTestigo1']

class FirmaTestigo2Form1(forms.ModelForm):
    firmaTestigo2 = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmaAlegato
        fields = ['firmaTestigo2']

class NoFirmaForms(forms.ModelForm):
    class Meta:
        model = NoFirma
        fields = '__all__'

class FirmaAutoridadActuanteFormNO(forms.ModelForm):
    firmaAutoridadActuante = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmasConstanciaNoFirma
        fields = ['firmaAutoridadActuante']

class FirmaRepresentanteLegalFormNO(forms.ModelForm):
    firmaRepresentanteLegal = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmasConstanciaNoFirma
        fields = ['firmaRepresentanteLegal']
    
class FirmaTestigoFormNo(forms.ModelForm):
    firmaTestigo1 = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmasConstanciaNoFirma
        fields = ['firmaTestigo1']

class FirmaTestigo2FormNo(forms.ModelForm):
    firmaTestigo2 = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = FirmasConstanciaNoFirma
        fields = ['firmaTestigo2']

class PresentaForms(forms.ModelForm):
    class Meta:
        model = presentapruebas
        fields = '__all__'
        widgets = {
         'presenta': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')), attrs={'class': 'form-check-inline'})
        }