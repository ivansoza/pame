from django import forms
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM, Estacion

class puestDisposicionINMForm(forms.ModelForm):
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

class extranjeroFormsInm(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = ['fechaRegistro', 'horaRegistro','numeroExtranjero','estacionMigratoria','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','firmaExtranjero','huellaExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','fotografiaExtranjero','viajaSolo','tipoEstancia','deLaPuestaIMN'] 
        

class extranjeroFormsAC(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = ['fechaRegistro', 'horaRegistro','numeroExtranjero','estacionMigratoria','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','firmaExtranjero','huellaExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','fotografiaExtranjero','viajaSolo','tipoEstancia','deLaPuestaAC']


