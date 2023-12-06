from django import forms 
from .models import Responsable, Autoridades, AutoridadesActuantes, Traductores, RepresentantesLegales
from django.core.validators import RegexValidator



class ResponsableForm(forms.ModelForm):
    nombre = forms.CharField(
        label= "Nombre:", 
        min_length=3, 
        max_length=35,
        validators= [RegexValidator(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',message="Solo se permiten letras y espacios en el nombre.")],
        widget=forms.TextInput(attrs={'placeholder':'Ej: Arley Ivan'})
        )

    apellidoPat = forms.CharField(
        label="Apellido Paterno:", 
        min_length=3, 
        max_length=35,
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message="Solo se permiten letras y espacios en el apellido materno.",
            code='invalid_apellido_materno'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: López'})
    )

    apellidoMat= forms.CharField(
        label="Apellido Materno:", 
        min_length=3, 
        max_length=35,
        validators=[RegexValidator(
            r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
            message="Solo se permiten letras y espacios en el apellido materno.",
            code='invalid_apellido_materno'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: Maldonado'})

    )

    email = forms.CharField(
        label= "Correo electrónico",
        validators=[
            RegexValidator(
                r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message="El correo electrónico no es válido."
            )
        ],
        widget=forms.EmailInput(attrs={'placeholder': 'Ej: ejemplo@dominio.com'})

    )

    telefono = forms.CharField(
         label="Teléfono:", 
        validators=[RegexValidator(
            r'^\d+$',
            message="Solo se permiten números en el teléfono.",
            code='invalid_telefono'
        )],
        widget=forms.TextInput(attrs={'placeholder': 'Ej: 1234567890'})

    )

    class Meta:
        model = Responsable
        fields = ["nombre","apellidoPat","apellidoMat","email","telefono"]

class AutoridadesForms(forms.ModelForm):
    class Meta:
        model = Autoridades
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ejemplo: Luis '}),
            'apellidoPaterno': forms.TextInput(attrs={'placeholder': 'Ejemplo:  Huerta '}),
            'apellidoMaterno': forms.TextInput(attrs={'placeholder': 'Ejemplo: Garcia '}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5518954598'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ejemplo:ejemplo@.com.mx'}),
        }
        

class AutoridadesActuantesForms(forms.ModelForm):
    class Meta:
        model = AutoridadesActuantes
        fields = '__all__'

class TraductoresForms(forms.ModelForm):
    class Meta:
        model = Traductores
        fields ='__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ejemplo: Adrian '}),
            'apellido_paterno': forms.TextInput(attrs={'placeholder': 'Ejemplo:  Huerta '}),
            'apellido_materno': forms.TextInput(attrs={'placeholder': 'Ejemplo: Garcia '}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ejemplo: 5518954598'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ejemplo:ejemplo@outlook.com.mx'}),
        }

class RepresentanteLegalForm(forms.ModelForm):
    email_validator = RegexValidator(
        regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
        message="Por favor, introduce un correo electrónico válido."
    )

    class Meta:
        model = RepresentantesLegales
        fields = ['nombre', 'apellido_paterno', 'apellido_materno', 'telefono', 'email', 'cedula', 'defensoria']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'apellido_paterno': forms.TextInput(attrs={'placeholder': 'Apellido Paterno'}),
            'apellido_materno': forms.TextInput(attrs={'placeholder': 'Apellido Materno'}),
            'telefono': forms.TextInput(attrs={'placeholder': '+1234567890'}),
            'email': forms.EmailInput(attrs={'placeholder': 'ejemplo@dominio.com'}),
            'cedula': forms.TextInput(attrs={'placeholder': 'Número de Cédula'}),
            'defensoria': forms.TextInput(attrs={'placeholder': 'Nombre de la Defensoría'}),
        }

    def __init__(self, *args, **kwargs):
        super(RepresentanteLegalForm, self).__init__(*args, **kwargs)
        self.fields['email'].validators.append(self.email_validator)

class RepresentanteLegalStatusForm(forms.ModelForm):
    class Meta:
        model = RepresentantesLegales
        fields = ['estatus']