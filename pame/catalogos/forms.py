from django import forms 
from .models import Responsable
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