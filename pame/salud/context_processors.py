from salud.models import PerfilMedico  # Asegúrate de importar tu modelo PerfilMedico

def perfil_medico(request):
    tiene_perfil_medico = False

    if request.user.is_authenticated:
        tiene_perfil_medico = PerfilMedico.objects.filter(usuario=request.user).exists()

    return {'tiene_perfil_medico': tiene_perfil_medico}