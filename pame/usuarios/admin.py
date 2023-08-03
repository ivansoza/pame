from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Usuario


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Usuario
    list_display = [
        "username",
        "estancia",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("estancia",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("estancia",)}),)


admin.site.register(Usuario, CustomUserAdmin)

