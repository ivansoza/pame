from django import forms
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM, Estacion

class puestDisposicionINMForm(forms.ModelForm):
    numeroOficio = forms.CharField(
        label= "Número de Oficio:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: 162729'})
    )   

    fechaOficio = forms.DateField(
        label= "Fecha de Oficio:",
        widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    nombreAutoridadSigna = forms.CharField(
        label= "Nombre de Autoridad Asignada:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Guillermo Perez Perez'})
    )
    cargoAutoridadSigna = forms.CharField(
        label= "Cargo de Autoridad Asignada:",
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

    nombreAutoridadSigna = forms.CharField(
        label= "Nombre de Autoridad Asignada:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Guillermo Perez Perez'})
    )

    cargoAutoridadSigna = forms.CharField(
        label= "Cargo de Autoridad Asignada:",
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
    numeroExtranjero = forms.IntegerField(
        label= "Numero:",
    )
    estacionMigratoria = forms.CharField(
        label= "Estación Migratoria:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Mexico'}),

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
    firmaExtranjero = forms.FileField(
        label= "Firma:",
    )
    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",

    )
    fotografiaExtranjero = forms.FileField(
        label= "Fotografía de Extranjero:",

    )
    tipoEstancia = forms.CharField(
        label= "Tipo de Estancia:",
    )
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','estacionMigratoria','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','firmaExtranjero','huellaExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','fotografiaExtranjero','viajaSolo','tipoEstancia','deLaPuestaIMN'] 
        widgets = {
            # Otros campos y widgets
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaIMN': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type':"checkbox"}),
          
        }


class extranjeroFormsAC(forms.ModelForm):

    fechaNacimiento = forms.DateField(
        label= "Fecha de Nacimiento:",
        widget=forms.DateInput(attrs={'type':'text','class':'form-control datepicker', 'id':'datepicker', 'placeholder':"dd/mm/yyyy"}),

    )
    numeroExtranjero = forms.IntegerField(
        label= "Numero:",
    )
    estacionMigratoria = forms.CharField(
        label= "Estación Migratoria:",
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
  
    tipoEstancia = forms.CharField(
        label= "Tipo de Estancia:",
    )
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','estacionMigratoria','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaAC']
        widgets = {
            # Otros campos y widgets
            'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaAC': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.CheckboxInput(attrs={'class': 'form-check-input', 'type':"checkbox"}),
        }

class ExtranjeroDatosBiometricosFormAC(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = ['firmaExtranjero', 'huellaExtranjero', 'fotografiaExtranjero']


