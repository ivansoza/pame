from django import forms
from .models import Alegatos, DocumentosAlegatos

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

    