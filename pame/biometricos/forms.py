from django import forms
from .models import UserFace, UserFace1

class CompareFacesForm(forms.Form):
    image1 = forms.ImageField(label='Primera imagen')
    image2 = forms.ImageField(label='Segunda imagen')

class UserFaceForm(forms.ModelForm):
    class Meta:
        model = UserFace
        fields = ['nombreExtranjero', 'image']


class SearchFaceForm(forms.Form):
    image = forms.ImageField()


class SearchFaceForm1(forms.Form):
    image = forms.ImageField()