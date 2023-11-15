from django import forms
from .models import Comparecencia


class ComparecenciaForm(forms.ModelForm):
    fechaIngresoMexico = forms.DateField(
        label="Fecha de Ingreso a México:",
        widget=forms.DateInput(attrs={'type': 'text', 'id': 'fechaIngresoMexico', 'placeholder': "DD/MM/YYYY"}),
        input_formats=['%d/%m/%Y'],
        required=True,  # Si es opcional
    )

    DOMICILIO_OPCIONES = (
        (None, "Selecciona una opción"),
        (True, "Sí"),
        (False, "No"),
    )

    domicilioEnMexico = forms.TypedChoiceField(
        label="¿Tiene domicilio en México?",
        coerce=lambda x: x == 'True',
        choices=DOMICILIO_OPCIONES,
        widget=forms.Select,
        empty_value=None
    )

    REFUGIO_OPCIONES = (
        (None, "Selecciona una opción"),
        (True, "Sí"),
        (False, "No"),
    )

    solicitaRefugio = forms.TypedChoiceField(
        label="¿Solicita refugio?",
        coerce=lambda x: x == 'True',
        choices=REFUGIO_OPCIONES,
        widget=forms.Select,
        empty_value=None
    )
    DELITO_OPCIONES = (
        (None, "Selecciona una opción"),
        (True, "Sí"),
        (False, "No"),
    )

    victimaDelito = forms.TypedChoiceField(
        label="¿Es víctima de delito?",
        coerce=lambda x: x == 'True',
        choices=DELITO_OPCIONES,
        widget=forms.Select,
        empty_value=None
    )
    class Meta:
        model = Comparecencia
        fields = ['estadoCivil', 'escolaridad', 'ocupacion', 'nacionalidad', 'DomicilioPais', 'lugarOrigen', 
                  'domicilioEnMexico', 'nombrePadre', 
                  'nacionalidadPadre', 'nombreMadre', 
                  'nacionalidadMadre', 'fechaIngresoMexico', 'lugarIngresoMexico', 'formaIngresoMexico', 
                  'declaracion', 'solicitaRefugio', 'victimaDelito', 'autoridadActuante', 'representanteLegal', 
                  'traductor', 'testigo1', 'grado_academico_testigo1', 'testigo2', 'grado_academico_testigo2']

    def __init__(self, *args, **kwargs):
        super(ComparecenciaForm, self).__init__(*args, **kwargs)
        self.fields['estadoCivil'].widget.attrs['placeholder'] = 'Estado civil'
        # Repite para los otros campos como sea necesario...
        self.fields['estadoCivil'].widget.attrs['readonly'] = True
        self.fields['escolaridad'].widget.attrs['readonly'] = True
        self.fields['ocupacion'].widget.attrs['readonly'] = True
        self.fields['nacionalidad'].widget.attrs['readonly'] = True
        self.fields['lugarOrigen'].widget.attrs['readonly'] = True
        self.fields['DomicilioPais'].widget.attrs['readonly'] = True
        self.fields['nombrePadre'].widget.attrs['readonly'] = True
        self.fields['nombreMadre'].widget.attrs['readonly'] = True
        self.fields['nacionalidadPadre'].widget.attrs['readonly'] = True
        self.fields['nacionalidadMadre'].widget.attrs['readonly'] = True
        self.fields['representanteLegal'].widget.attrs['readonly'] = True


        self.fields['declaracion'].widget.attrs['placeholder'] = 'Ingrese cualquier información relevante'
        self.fields['lugarIngresoMexico'].widget.attrs['placeholder'] = 'Ciudad, Estado'
        self.fields['formaIngresoMexico'].widget.attrs['placeholder'] = 'Ejemplo: Aeropuerto, Vehículo, A pie'
        self.fields['testigo1'].widget.attrs['placeholder'] = 'Nombre completo del Testigo 1'
        self.fields['testigo2'].widget.attrs['placeholder'] = 'Nombre completo del Testigo 2'
  

   
