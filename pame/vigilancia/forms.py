from django import forms
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM, Estacion, Biometrico, PuestaDisposicionVP, descripcion
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM, Estacion, Biometrico, PuestaDisposicionVP, UserFace,AsignacionRepresentante,HuellaTemp
import datetime
from django.core.exceptions import ValidationError
from traslados.models import Traslado
from .models import Firma
from catalogos.models import Relacion , AutoridadesActuantes, RepresentantesLegales
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

class ValidacionArchivosPDF(forms.Form):
    def clean_archivof(self, field_name):
        archivo = self.cleaned_data.get(field_name)
        if archivo:
            # Validacion por tipo de archivo 
            nombre_archivo = archivo.name
            extension = nombre_archivo.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png']:
                raise forms.ValidationError(f'La firma debe ser JPG o PNG')
            
            # Validar por tamaño de archivo, menor a 1 MB
            max_tamano = 512 * 512 # 1/2 MB
            if archivo.size > max_tamano:
                raise forms.ValidationError(f'La firma debe ser menor a 512 kb')
            
        return archivo

class puestDisposicionINMForm(forms.ModelForm, ValidacionArchivos):
    
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

    

    oficioPuesta = forms.FileField(
        label= "Oficio de Puesta:",
        required=False,

         # widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    
    def clean_oficioPuesta(self):
        return self.clean_archivo('oficioPuesta')
    
    oficioComision = forms.FileField(
        label= "Oficio de Comisión:",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    def clean_oficioComision(self):
        return self.clean_archivo('oficioComision')
    
    puntoRevision = forms.CharField(
        label= "Punto de Revisión:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Central de autobuses'})
    )
    
    class Meta:
        model = PuestaDisposicionINM
        fields ='__all__'
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Obtén el usuario actual de los argumentos
        super(puestDisposicionINMForm, self).__init__(*args, **kwargs)

        if user:
            # Filtra las opciones del campo nombreAutoridadSignaUno y nombreAutoridadSignaDos
            self.fields['nombreAutoridadSignaUno'].queryset = AutoridadesActuantes.objects.filter(estacion=user.estancia)
            self.fields['nombreAutoridadSignaDos'].queryset = AutoridadesActuantes.objects.filter(estacion=user.estancia)



class puestaDisposicionACForm(forms.ModelForm, ValidacionArchivos):
   

    
    numeroOficio = forms.CharField(
        label= "Número de Oficio:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: 162729'})

    )
    fechaOficio = forms.DateField(
        label= "Fecha de Oficio:",
        widget= forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

   


    
    

    oficioPuesta = forms.FileField(
        label= "Oficio de Puesta:",
        required=False

         # widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
     )
    
    def clean_oficioPuesta(self):
        return self.clean_archivo('oficioPuesta')

    oficioComision = forms.FileField(
        label= "Oficio de Comisión:",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}) 
    )

    def clean_oficioComision(self):
        return self.clean_archivo('oficioComision')

    puntoRevision = forms.CharField(
        label= "Punto de Revisión:",

        widget=forms.TextInput(attrs={'placeholder':'Ej: Central de autobuses'})
    )

    dependencia = forms.CharField(
        label= "Dependencia:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Dependencia 1'})
    )

    numeroCarpeta = forms.CharField(
        label= "Número de Carpeta:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: 1934392'})
    )
    
    entidadFederativa = forms.CharField(
        label= "Entidad Federativa:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Entidad 1'})
    )
    municipio = forms.CharField(
        label= "Municipio:",
        widget=forms.TextInput(attrs={'placeholder':'Ej: Apizaco'})
    )

    certificadoMedico = forms.FileField(
        label= "Certificado Médico:",
        required=False,

        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    def clean_certificadoMedico(self):
        return self.clean_archivo('certificadoMedico')

    class Meta:
        model = PuestaDisposicionAC
        fields ='__all__'
        widgets = {
            # Otros campos y widgets
            'deLaEstacion': forms.Select(attrs={'class': 'form-control'}),
           
        }



class extranjeroFormsInm(forms.ModelForm, ValidacionArchivos):
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
    
    def clean_documentoIdentidad(self):
        return self.clean_archivo('documentoIdentidad')
   
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
        widget=forms.DateInput(attrs={'placeholder':"Ej:Perez"}),
        required=False  # Esto hace que el campo no sea obligatorio

    )

    domicilio = forms.CharField(
        label= "Domicilio y/o Residencia:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Av. Moctezuma"}),
    )
    origen = forms.CharField(
        label= "Origen:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Medellin"}),
    )
    ocupacion = forms.CharField(
        label= "Ocupación:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Docente"}),
    )
    nombreDelPadre = forms.CharField(
        label="Nombre completo del padre:",
        widget=forms.TextInput(attrs={'placeholder': "Ej: Juan Pérez"}),
        required=False  # Esto hace que el campo no sea obligatorio

    )

    nombreDelaMadre = forms.CharField(
        label="Nombre completo de la madre:",
        widget=forms.TextInput(attrs={'placeholder': "Ej: Ana García"}),
        required=False  # Esto hace que el campo no sea obligatorio

    
    )

   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','origen','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaIMN','estado_Civil','grado_academico','ocupacion','nombreDelPadre','nombreDelaMadre','domicilio','nacionalidad_Padre','nacionalidad_Madre','domicilio','edad'] 
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
        fields = ['nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','origen','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','estado_Civil','grado_academico','ocupacion','nombreDelPadre','nombreDelaMadre','domicilio','nacionalidad_Padre','nacionalidad_Madre','domicilio','edad','deLaPuestaIMN','deLaPuestaAC','deLaPuestaVP'] 
        widgets = {
            # Otros campos y widgets
            #'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
            'deLaPuestaIMN': forms.Select(attrs={'class': 'form-control'}),
            'viajaSolo': forms.RadioSelect(choices=((True, 'Sí'), (False, 'No')))
        }


class BiometricoFormINM(forms.ModelForm, ValidacionArchivosPDF):
    class Meta:
        model = Biometrico
        fields = '__all__'  # Incluye todos los campos del modelo

    def clean_firmaExtranjero(self):
        return self.clean_archivof('firmaExtranjero')

class BiometricoFormAC(forms.ModelForm,ValidacionArchivosPDF):
    class Meta:
        model = Biometrico
        fields = '__all__'  # Incluye todos los campos del modelo

    def clean_firmaExtranjero(self):
        return self.clean_archivof('firmaExtranjero')

class extranjeroFormsAC(forms.ModelForm, ValidacionArchivos):

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
        widget=forms.DateInput(attrs={'placeholder':"Ej:Perez"}),
        required=False  # Esto hace que el campo no sea obligatorio

    )

    domicilio = forms.CharField(
        label= "Domicilio y/o Residencia:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Av. Moctezuma"}),
    )
    origen = forms.CharField(
        label= "Origen:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Medellin"}),
    )
    ocupacion = forms.CharField(
        label= "Ocupación:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Docente"}),
    )
    nombreDelPadre = forms.CharField(
        label="Nombre completo del padre:",
        widget=forms.TextInput(attrs={'placeholder': "Ej: Juan Pérez"}),
        required=False  # Esto hace que el campo no sea obligatorio

    )

    nombreDelaMadre = forms.CharField(
        label="Nombre completo de la madre:",
        widget=forms.TextInput(attrs={'placeholder': "Ej: Ana García"}),
        required=False  # Esto hace que el campo no sea obligatorio

    
    )

   
    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",
        required=False
    )

    def clean_documentoIdentidad(self):
        return self.clean_archivo('documentoIdentidad')
   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','domicilio','fechaNacimiento','edad','nacionalidad','genero','estado_Civil','grado_academico','ocupacion','documentoIdentidad','tipoEstancia','deLaPuestaAC','nombreDelPadre','nacionalidad_Padre','nombreDelaMadre','nacionalidad_Madre','origen']
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
      fields = ['nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','origen','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','estado_Civil','grado_academico','ocupacion','nombreDelPadre','nombreDelaMadre','domicilio','nacionalidad_Padre','nacionalidad_Madre','domicilio','edad','deLaPuestaIMN','deLaPuestaAC','deLaPuestaVP']
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

    relacion = forms.ModelChoiceField(
        queryset=Relacion.objects.all(),
        to_field_name='tipoRelacion',  # Ajusta esto al campo que quieras usar como valor
        empty_label='Selecciona una relación'
    )
    

#----------------- formulario puesta Disposicion VP ----------------------------------------------------

class puestaVPForm(forms.ModelForm):
    class Meta:
        model = PuestaDisposicionVP
        fields = '__all__'

class extranjeroFormsVP(forms.ModelForm, ValidacionArchivos):
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
        widget=forms.DateInput(attrs={'placeholder':"Ej:Perez"}),
        required=False  # Esto hace que el campo no sea obligatorio

    )

    domicilio = forms.CharField(
        label= "Domicilio y/o Residencia:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Av. Moctezuma"}),
    )
    origen = forms.CharField(
        label= "Origen:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Medellin"}),
    )
    ocupacion = forms.CharField(
        label= "Ocupación:",
        widget=forms.DateInput(attrs={'placeholder':"Ej: Docente"}),
    )
    nombreDelPadre = forms.CharField(
        label="Nombre completo del padre:",
        widget=forms.TextInput(attrs={'placeholder': "Ej: Juan Pérez"}),
        required=False  # Esto hace que el campo no sea obligatorio

    )

    nombreDelaMadre = forms.CharField(
        label="Nombre completo de la madre:",
        widget=forms.TextInput(attrs={'placeholder': "Ej: Ana García"}),
        required=False  # Esto hace que el campo no sea obligatorio

    
    )

    
    documentoIdentidad = forms.FileField(
        label= "Documento de Identidad:",
    )

    def clean_documentoIdentidad(self):
        return self.clean_archivo('documentoIdentidad')
  
   
    class Meta:
        model = Extranjero
        fields = ['numeroExtranjero','deLaEstacion','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','nacionalidad','origen','genero','fechaNacimiento','documentoIdentidad','viajaSolo','tipoEstancia','deLaPuestaVP','estado_Civil','grado_academico','ocupacion','nombreDelPadre','nombreDelaMadre','domicilio','nacionalidad_Padre','nacionalidad_Madre','domicilio','edad','origen'] 
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
        fields = ['nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','domicilio','fechaNacimiento','edad','nacionalidad','genero','estado_Civil','grado_academico','ocupacion','documentoIdentidad','tipoEstancia','nombreDelPadre','nacionalidad_Padre','nombreDelaMadre','nacionalidad_Madre','deLaPuestaIMN','deLaPuestaAC','deLaPuestaVP'] 
        widgets = {
            # Otros campos y widgets
            #'nacionalidad': forms.Select(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-control'}),
        }


class BiometricoFormVP(forms.ModelForm,ValidacionArchivosPDF):
    class Meta:
        model = Biometrico
        fields = '__all__'  # Incluye todos los campos del modelo

    def clean_firmaExtranjero(self):
        return self.clean_archivof('firmaExtranjero')


class TrasladoForm(forms.ModelForm):
    class Meta:
        model = Traslado
        fields = ['numeroUnicoProceso', 'estacion_origen', 'estacion_destino', 'nombreAutoridadEnvia']


class CompareFacesForm(forms.Form):
    image1 = forms.ImageField(label='Primera imagen')
    image2 = forms.ImageField(label='Segunda imagen')


class descripcionForms(forms.ModelForm):
    class Meta:
        model=descripcion
        fields='__all__'

class UserFaceForm(forms.ModelForm):
    class Meta:
        model = UserFace
        fields = ['nombreExtranjero', 'image']


class SearchFaceForm(forms.Form):
    image = forms.ImageField()

class FirmaExtranjeroForm(forms.ModelForm):
    class Meta:
        model = Biometrico
        fields = ['firmaExtranjero']



class FirmaForm(forms.ModelForm):
    firma_imagen = forms.CharField(widget=forms.HiddenInput()) # Esto es para la cadena dataURL

    class Meta:
        model = Firma
        fields = ['firma_imagen']

class AsignacionRepresentanteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        estacion_usuario = kwargs.pop('estacion_usuario', None)
        super().__init__(*args, **kwargs)
        if estacion_usuario:
            self.fields['representante_legal'].queryset = RepresentantesLegales.objects.filter(
                estatus='Activo',
                estacion=estacion_usuario
            )

    class Meta:
        model = AsignacionRepresentante
        fields = ['representante_legal']
        
class HuellaTempForm(forms.ModelForm):
    model = HuellaTemp
    fields='__all__'    