from django import forms
<<<<<<< HEAD
=======
from .models import OficioPuestaDisposicionINM, OficioPuestaDisposicionAC, ExtranjeroAC
from django.core.validators import RegexValidator
from django.forms import inlineformset_factory
>>>>>>> origin/jose

from .models import Extranjero, Acompanante, Nacionalidad, TipoDisposicion, PuestaDisposicion, ComplementoINM, ComplementonAC

class TipoDisposicionForm(forms.ModelForm):
    model = TipoDisposicion
    fields = '__all__'

class ComplementoINMForm(forms.ModelForm):
    model = ComplementoINM
    fields ='__all__'

<<<<<<< HEAD
class ComplementoACForm(forms.ModelForm):
    model = ComplementonAC
    fields ='__all__'
    
=======
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

    oficioPuesta = forms.FileInput(
        
    )

    certificadoMedico = forms.FileInput(
      
    )

   

    

class ExtranjeroForm(forms.ModelForm):
    class Meta:
        model = ExtranjeroAC
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
        label='Hora de Registro', input_formats=['%I:%M %p'],
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
        label='Nombre',
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ingresa tu nombre'})
    )

    apellidoPaternoE = forms.CharField(
        label='Apellido Paterno',
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ingresa el Primero Apellido'})
    )

    apellidoE = forms.CharField(
        label='Apellido Materno',
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message='Solo se permiten letras'
        )],
        widget=forms.TextInput(attrs={'placeholder':'Ingresa el Segundo Apellido'})
    )

    firmaE = forms.ImageField(
        label='Firma',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    huellaE = forms.ImageField(
        label='Huella',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    nacionalidad = forms.CharField(
        label='Nacionalidad',
        widget=forms.TextInput(attrs={'placeholder':'Selecciona la Nacionalidad'})
    )

    genero = forms.CharField(
        label='Genero',
        widget=forms.TextInput(attrs={'placeholder':'Selecciona el Genero'})
    )
    
    fechaNacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        widget=forms.DateInput(attrs={'type':'date'})
    )

    documentoIdentidad = forms.ImageField(
        label='Documento de Identidad',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    fotografiaExtranjero = forms.ImageField(
        label='Documento de Identidad',
        widget=forms.ClearableFileInput(attrs={'multiple': True})
    )

    viajaSolo = forms.BooleanField(
        label='Viaja Solo'
    )

class pruebaForm(forms.ModelForm):
    class Meta:
        model = OficioPuestaDisposicionAC
        fields = '__all__'

extranjeroFormSet = inlineformset_factory(OficioPuestaDisposicionAC, ExtranjeroAC, fields='__all__')
>>>>>>> origin/jose
