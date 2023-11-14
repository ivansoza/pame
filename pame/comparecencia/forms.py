from django import forms
from .models import Comparecencia


class ComparecenciaForm(forms.ModelForm):
    class Meta:
        model = Comparecencia
        fields = ['estadoCivil', 'escolaridad', 'ocupacion', 'nacionalidad', 'DomicilioPais', 'lugarOrigen', 'domicilioEnMexico', 'nombrePadre', 'apellidoPaternoPadre', 'apellidoMaternoPadre', 'nacionalidadPadre', 'nombreMadre', 'apellidoPaternoMadre', 'apellidoMaternoMadre', 'nacionalidadMadre', 'fechaIngresoMexico', 'lugarIngresoMexico', 'formaIngresoMexico', 'declaracion', 'solicitaRefugio', 'victimaDelito', 'autoridadActuante', 'representanteLegal', 'cedulaRepresentanteLegal', 'traductor', 'testigo1', 'grado_academico_testigo1', 'testigo2', 'grado_academico_testigo2']
