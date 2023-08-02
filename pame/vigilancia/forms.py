from django import forms
from .models import OficioPuestaDisposicionINM, OficioPuestaDisposicionAC, Extranjero
from django.core.validators import RegexValidator

class OficioPuestaDisposicionINMform(forms.ModelForm):
    class Meta:
        model = OficioPuestaDisposicionINM
        fields = ['numeroOficio', 'fechaOficio', 'nombreAutoridadSigna', 'cargoAutoridadSigna',
                  'puntoRevision', 'oficioPuesta', 'oficioComision', 'delExtranjero']
        labels = {
            'numeroOficio':'Numero de Oficio',
            'fechaOficio':'Fecha',
            'nombreAutoridadSigna':"Nombre de Autoridad Asignada",
            'cargoAutoridadSigna':'Cargo de autoridad Asignada',
            'puntoRevision':'Punto de Revision',
            'oficioPuesta':'Oficio Puesta a Disposicion',
            'oficioComision':'Oficio Comision',
            'delExtranjero':'Numero del Extranjero',
        }
        widgets = {
            'numeroOficio': forms.TextInput(
                attrs={
                    'placeholder':'Numero de Oficio'
                }
            ),
            'nombreAutoridadSigna': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el nombre de la Autoridad Asignada'
                }
            ),
            'cargoAutoridadSigna': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Cargo de la Autoridad'
                }
            ),
            'puntoRevision': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Punto de Revision'
                }
            ),
            'oficioPuesta': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Numero De oficio'
                }
            ),
            'oficioComision': forms.TextInput(
                attrs={
                    'placeholder':'Ingresa el Numero de Comision'
                }
            )
        }

    def clean_numeroOficio(self):
        data = self.cleaned_data['numeroOficio']
        if not data.isdigit():
            raise forms.ValidationError('Solo debe contener numeros')
        return data
    
    def clean_oficioPuesta(self):
        data = self.cleaned_data['oficioPuesta']
        if not data.isdigit():
            raise forms.ValidationError('Solo debe contener numeros')
        return data
    
    def clean_oficioComision(self):
        data = self.cleaned_data['oficioComision']
        if not data.isdigit():
            raise forms.ValidationError('Solo debe contener numeros')
        return data
    
class OficioPuestaDisposicionACform(forms.ModelForm):
    numerooficio = forms.CharField(
        label= 'Numero de Oficio',
        validators= [RegexValidator(
            r'^[1-9]\d*$', message='Solo se permiten numeros'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'No. Oficio'})
    )

    fechaOficio = forms.CharField(
        label='Fecha Oficio',
    )

    dependencia = forms.CharField(
        label= 'Nombre Dependencia',
        validators= [RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten palabras'
        )],
        widget=forms.TextInput(attrs={'placeholder' : 'Ej: Juan'})
    )

    numeroCarpeta = forms.CharField(
        label='Numero de Carpeta',
        validators=[RegexValidator(
            r'^[1-9]\d*$', message='Solo sepermiten numeros' 
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ej: 12345'})
    )

    nombreAutoridadSigna = forms.CharField(
        label='Nombre de Autoridad Asignada',
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Nombre'})
    )

    cargoAutoridadSigna = forms.CharField(
        label='Cargo de la Autoridad Asignada',
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ej: Administrador'})
    )

    entidadFederativa = forms.CharField(
        label='Entidad Federativa',
    )

    oficioPuesta = forms.CharField(
        label='No. Oficio Puesta'
        validators=[RegexValidator(
            r'^[1-9]\d*$', message='Solo sepermiten numeros' 
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ej: 12345'})
    )

    certificadoMedico = forms.CharField(
        label='Certificado Medico'
    )

    delExtranjero = forms.CharField(
        label='Numero del extranjero'
    )

    class Meta:
        model = OficioPuestaDisposicionAC
        fields = [
            'numeroOficio',
            'fechaOficio',
            'dependencia',
            'numeroCarpeta',
            'nombreAutoridadSigna',
            'cargoAutoridadSigna',
            'entidadFederativa',
            'oficioPuesta',
            'certificadoMedico',
            'delExtranjero'
        ]

class ExtranjeroForm(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = [
            'fechaRegistro',
            'horaRegistro',
            'numeroE',
            'nombreE',
            'apellidoPaternoE',
            'apellidoMaternoE',
            'firmaE',
            'huellaE',
            'nacionalidad',
            'genero',
            'fechaNacimiento',
            'documentoIdentidad',
            'fotografiaExtranjero',
            'viajaSolo'
        ]

    fechaRegistro = forms.DateField(
        label='Fecha de Registro',
        widget=forms.DateInput(attrs={'type':'date'})
    )

    class TimePickerWidget(forms.TimeInput):
        input_type = 'time'

    horaRegistro = forms.TimeField(
        label='Hora de Registro', input_formats=['%I:%M %p']
        #Los segundos incrementan de 1 minuto
        widget=TimePickerWidget(attrs={'step': '60'})
    )

    numeroE = forms.CharField(
        label='Numero de Extranjero',
        validators=[RegexValidator(
            r'^\d+$',
            message='Solo se permiten numeros'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ej: 12345'})
    )

    nombreE = forms.CharField(
        label='Nombre'
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ingresa tu nombre'})
    )

    apellidoPaternoE = forms.CharField(
        label='Apellido Paterno'
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            mesagge='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ingresa el Primero Apellido'})
    )

    apellidoE = forms.CharField(
        label='Apellido Materno'
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            mesagge='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ingresa el Segundo Apellido'})
    )

    firmaE = forms.ImageField(
        label='Firma'
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    huellaE = forms.ImageField(
        label='Huella'
        widget=forms.ClearableFileInput(attrs={'multiple':True})
    )

    nacionalidad = forms.CharField(
        label='Nacionalidad'
        widget=forms.TextInput(attrs={'placeholder':'Selecciona la Nacionalidad'})
    )

    genero = forms.CharField(
        label='Nacionalidad'
        widget=forms.TextInput(attrs={'placeholder':'Selecciona el Genero'})
    )
    
    fechaNacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={'type':'date'})
    )

    documentoIdentidad = forms.ImageField(
        label='Documento de Identidad'
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    fotografiaExtranjero = forms.ImageField(
        label='Documento de Identidad'
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    viajaSolo = forms.BooleanField(
        label='Viaja Solo'
    )