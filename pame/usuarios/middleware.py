from django.contrib.sessions.models import Session
from django.utils import timezone

class PreventMultipleLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Obtiene la sesión actual del usuario
            user_sessions = Session.objects.filter(
                expire_date__gte=timezone.now(),
                session_key=request.session.session_key,
            ).exclude(session_key=request.session.session_key)

            # Invalida todas las sesiones anteriores del usuario
            user_sessions.delete()

        response = self.get_response(request)
        return response
