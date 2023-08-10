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
        fields = '__all__'

        def _init_(self, *args, **kwargs):
          super()._init_(*args, **kwargs)
           # Excluye el campo que deseas excluir
          del self.fields['deLaPuestaAC']

class extranjeroFormsAC(forms.ModelForm):
    class Meta:
        model = Extranjero
        fields = '__all__'

        def _init_(self, *args, **kwargs):
          super()._init_(*args, **kwargs)
           # Excluye el campo que deseas excluir
          del self.fields['deLaPuestaINM']