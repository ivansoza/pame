from django import forms
from .models import llamadasTelefonicas

class llamadasTelefonicasForm(forms.modelForm):
    class Meta:
        model = llamadasTelefonicas
        fields = '__all__'