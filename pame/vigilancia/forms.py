from django import forms
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM, Estacion, Biometrico, PuestaDisposicionVP
import datetime
from django.core.exceptions import ValidationError
from traslados.models import Traslado

class puestDisposicionINMForm(forms.ModelForm):
    numeroOficio = forms.CharField(
        label= "Número de Oficio:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: 162729'})
    )   

    fechaOficio = forms.DateField(
        label= "Fecha de Oficio:",
        widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer la fecha actual como valor por defecto
        self.fields['fechaOficio'].initial = datetime.date.today()

    nombreAutoridadSignaUno = forms.CharField(
        label= "Nombre de Autoridad Asignada 1:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Guillermo Perez Perez'})
    )
    cargoAutoridadSignaUno = forms.CharField(
        label= "Cargo de Autoridad Asignada 1:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Administrador'})
    )

    nombreAutoridadSignaDos = forms.CharField(
        label= "Nombre de Autoridad Asignada 2:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Guillermo Perez Perez'})
    )
    cargoAutoridadSignaDos = forms.CharField(
        label= "Cargo de Autoridad Asignada 2:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Administrador'})
    )


    oficioPuesta = forms.FileField(
        label= "Oficio de Puesta:",
        required=False,

         # widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    oficioComision = forms.FileField(
        label= "Oficio de Comisión:",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    puntoRevision = forms.CharField(
        label= "Punto de Revision:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Central de autobuses'})
    )
    
    
    class Meta:
        model = PuestaDisposicionINM
        fields ='__all__'



class puestaDisposicionACForm(forms.ModelForm):

    
    numeroOficio = forms.CharField(
        label= "Número de Oficio:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: 162729'})

    )
    fechaOficio = forms.DateField(
        label= "Fecha de Oficio:",
        widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    nombreAutoridadSignaUno = forms.CharField(
        label= "Nombre de Autoridad Asignada 1:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Guillermo Perez Perez'})
    )

    cargoAutoridadSignaUno = forms.CharField(
        label= "Cargo de Autoridad Asignada 1:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Administrador'})
    )

    nombreAutoridadSignaDos = forms.CharField(
        label= "Nombre de Autoridad Asignada 2:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Guillermo Perez Perez'})
    )

    cargoAutoridadSignaDos = forms.CharField(
        label= "Cargo de Autoridad Asignada 2:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Administrador'})
    )

    oficioPuesta = forms.FileField(
        label= "Oficio de Puesta:",
        required=False

         # widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )

    oficioComision = forms.FileField(
        label= "Oficio de Comisión:",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )

    puntoRevision = forms.CharField(
        label= "Punto de Revision:",

        widget=forms.TextInput(attrs={'placeholder':'Ej: Central de autobuses'})
    )

    dependencia = forms.CharField(
        label= "Dependencia:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Dependencia 1'})
    )

    numeroCarpeta = forms.CharField(
        label= "Número de Carpeta:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Carpeta 1'})
    )
    
    entidadFederativa = forms.CharField(
        label= "Entidad Federativa:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Entidad 1'})
    )
    certificadoMedico = forms.FileField(
        label= "Certificado Medico:",
        required=False,

        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    class Meta:
        model = PuestaDisposicionAC
        fields ='__all__'
        widgets = {
            # Otros campos y widgets
            'deLaEstacion': forms.Select(attrs={'class': 'form-control'}),
           
        }



class extranjeroFormsInm(forms.ModelForm):
    fechaNacimiento = forms.DateField(
        label="Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'date', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
    )

    def clean_fechaNacimiento(self):
        data = self.cleaned_data['fechaNacimiento']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise ValidationError('Debe de ser mayor de 18 años.')        
        if age > 110:
            raise ValidationError('La edad ingresada no es válida. Por favor, verifica la fecha de nacimiento.')
        return data
    
    numeroExtranjero = forms.CharField(
        label= "Numero:",
    )
   
    nombreExtranjero = forms.CharField(
        label= "Nombre(s):",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Luis"}),

    )
    apellidoPaternoExtranjero = forms.CharField(
        label= "Apellido Paterno:",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Lopez"}),

    )

    apellidoMaternoExtranjero = forms.CharField(
        label= "Apellido Materno:",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Juarez"}),

    )
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaIMN'] 
        widgets = {
            # Otros campos y widgets
            'estatus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaIMN': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))

        }

class editExtranjeroINMForm(forms.ModelForm):

    fechaNacimiento = forms.DateField(
        label="Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'date', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
    )

    def clean_fechaNacimiento(self):
        data = self.cleaned_data['fechaNacimiento']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise ValidationError('Debe de ser mayor de 18 años.')        
        if age > 110:
            raise ValidationError('La edad ingresada no es válida. Por favor, verifica la fecha de nacimiento.')
        return data
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaIMN','estatus'] 
        widgets = {
            # Otros campos y widgets
            #'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaIMN': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }


class BiometricoFormINM(forms.ModelForm):
    class Meta:
        model = Biometrico
        fields = '__all__'  # Incluye todos los campos del modelo

class BiometricoFormAC(forms.ModelForm):
    class Meta:
        model = Biometrico
        fields = '__all__'  # Incluye todos los campos del modelo


class extranjeroFormsAC(forms.ModelForm):

    fechaNacimiento = forms.DateField(
        label="Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'date', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
    )

    def clean_fechaNacimiento(self):
        data = self.cleaned_data['fechaNacimiento']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise ValidationError('Debe de ser mayor de 18 años.')        
        if age > 110:
            raise ValidationError('La edad ingresada no es válida. Por favor, verifica la fecha de nacimiento.')
        return data
  
    
    numeroExtranjero = forms.CharField(
        label= "Numero:",
    )
    
    nombreExtranjero = forms.CharField(
        label= "Nombre(s):",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Luis"}),

    )
    apellidoPaternoExtranjero = forms.CharField(
        label= "Apellido Paterno:",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Lopez"}),

    )

    apellidoMaternoExtranjero = forms.CharField(
        label= "Apellido Materno:",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Juarez"}),

    )
   
   
   
   
    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",

    )
  
   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaAC']
        widgets = {
            # Otros campos y widgets
            'estatus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaAC': forms.Select(attrs={'class': 'form-control'}),
             'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }


class editExtranjeroACForms(forms.ModelForm):

    fechaNacimiento = forms.DateField(
        label="Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'date', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
    )

    def clean_fechaNacimiento(self):
        data = self.cleaned_data['fechaNacimiento']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise ValidationError('Debe de ser mayor de 18 años.')        
        if age > 110:
            raise ValidationError('La edad ingresada no es válida. Por favor, verifica la fecha de nacimiento.')
        return data
    class Meta:
      model = Extranjero
      fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaAC','estatus']
      widgets = {
            # Otros campos y widgets
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaAC': forms.Select(attrs={'class': 'form-control'}),
             'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
      }

class AcompananteForm(forms.ModelForm):
    class Meta:
        model = Acompanante
        fields = ['relacion']

#----------------- formulario puesta Disposicion VP ----------------------------------------------------

class puestaVPForm(forms.ModelForm):
    class Meta:
        model = PuestaDisposicionVP
        fields = '__all__'

class extranjeroFormsVP(forms.ModelForm):
    fechaNacimiento = forms.DateField(
        label="Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'date', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
    )

    def clean_fechaNacimiento(self):
        data = self.cleaned_data['fechaNacimiento']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise ValidationError('Debe de ser mayor de 18 años.')        
        if age > 110:
            raise ValidationError('La edad ingresada no es válida. Por favor, verifica la fecha de nacimiento.')
        return data

    numeroExtranjero = forms.CharField(
        label= "Numero:",
    )
    nombreExtranjero = forms.CharField(
        label= "Nombre(s):",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Luis"}),
    )
    apellidoPaternoExtranjero = forms.CharField(
        label= "Apellido Paterno:",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Lopez"}),
    )
    apellidoMaternoExtranjero = forms.CharField(
        label= "Apellido Materno:",
        widget=forms.DateInput(attrs={'placeholder':"Ej:Lopez"}),
    )
    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",
    )
  
   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaVP'] 
        widgets = {
            # Otros campos y widgets
            'estatus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaVP': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }

class editExtranjeroVPForm(forms.ModelForm):

    fechaNacimiento = forms.DateField(
        label="Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'date', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
    )

    def clean_fechaNacimiento(self):
        data = self.cleaned_data['fechaNacimiento']
        today = datetime.date.today()
        age = today.year - data.year - ((today.month, today.day) < (data.month, data.day))
        if age < 18:
            raise ValidationError('Debe de ser mayor de 18 años.')        
        if age > 110:
            raise ValidationError('La edad ingresada no es válida. Por favor, verifica la fecha de nacimiento.')
        return data
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaVP','estatus'] 
        widgets = {
            # Otros campos y widgets
            #'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaVP': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }


class BiometricoFormVP(forms.ModelForm):
    class Meta:
        model = Biometrico
        fields = '__all__'  # Incluye todos los campos del modelo


class TrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['numeroUnicoProceso', 'estacion_origen', 'estacion_destino', 'nombreAutoridadEnvia']