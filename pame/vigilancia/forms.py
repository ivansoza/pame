from django import forms
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM, Estacion, Biometrico
import datetime

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
        self.fields['fechaOficio'].widget.attrs['readonly'] = 'readonly'  # Marcar como solo lectura

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
         # widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    oficioComision = forms.FileField(
         label= "Oficio de Comisión:",
         widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    puntoRevision = forms.CharField(
        label= "Punto de Revision:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Punto 1'})
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
         # widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )

    oficioComision = forms.FileField(
         label= "Oficio de Comisión:",
         widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )

    puntoRevision = forms.CharField(
        label= "Punto de Revision:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Punto 1'})
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
        label= "Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type':'text','class':'form-control datepicker', 'id':'datepicker', 'placeholder':"dd/mm/yyyy"}),

    )
    numeroExtranjero = forms.CharField(
        label= "Numero:",
    )
   
    nombreExtranjero = forms.CharField(
        label= "Nombre(s):",
    )
    apellidoPaternoExtranjero = forms.CharField(
        label= "Apellido Paterno:",
    )
    apellidoMaternoExtranjero = forms.CharField(
        label= "Apellido Materno:",
    )

    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",

    )
  
   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaIMN','estatus'] 
        widgets = {
            # Otros campos y widgets
            'estatus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaIMN': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }

class editExtranjeroINMForm(forms.ModelForm):
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
        label= "Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type':'text','class':'form-control datepicker', 'id':'datepicker', 'placeholder':"dd/mm/yyyy"}),

    )
    numeroExtranjero = forms.CharField(
        label= "Numero:",
    )
    
    nombreExtranjero = forms.CharField(
        label= "Nombre(s):",
    )
    apellidoPaternoExtranjero = forms.CharField(
        label= "Apellido Paterno:",
    )
    apellidoMaternoExtranjero = forms.CharField(
        label= "Apellido Materno:",
    )
   
   
    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",

    )
  
   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaAC','estatus']
        widgets = {
            # Otros campos y widgets
            'estatus': forms.TextInput(attrs={'readonly': 'readonly'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaAC': forms.Select(attrs={'class': 'form-control'}),
             'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }
# class AcompananteForm(forms.ModelForm):
#     class Meta:
#         model = Acompanante
#         fields = ['delAcompanante', 'relacion']

class editExtranjeroACForms(forms.ModelForm):
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
