from django import forms
from .models import Extranjero, Acompanante, Nacionalidad, PuestaDisposicionAC, PuestaDisposicionINM

class puestDisposicionINMForm(forms.ModelForm):
    class Meta:
        model = PuestaDisposicionINM
        fields ='__all__'

class puestaDisposicionACForm(forms.ModelForm):
    class Mate:
        model = PuestaDisposicionAC
        fields ='__all__'

class extranjeroFormsInm(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = ['fechaRegistro', 'horaRegistro','numeroExtranjero','estacionMigratoria','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','firmaExtranjero','huellaExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','fotografiaExtranjero','viajaSolo','tipoEstancia','deLaPuestaIMN'] 
        

class extranjeroFormsAC(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = ['fechaRegistro', 'horaRegistro','numeroExtranjero','estacionMigratoria','nombreExtranjero','apellidoPaternoExtranjero','apellidoMaternoExtranjero','firmaExtranjero','huellaExtranjero','nacionalidad','genero','fechaNacimiento','documentoIdentidad','fotografiaExtranjero','viajaSolo','tipoEstancia']


