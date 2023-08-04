from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ("estancia",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = UserChangeForm.Meta.fields