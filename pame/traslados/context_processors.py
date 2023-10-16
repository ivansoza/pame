from .models import Traslado
from datetime import datetime, timedelta
from django.utils import timezone

def tiempo_desde(fecha):
    ahora = timezone.now()
    diferencia = ahora - fecha

    segundos = diferencia.total_seconds()
    
    if segundos < 60:
        return "1 min"
    elif segundos < 3600:
        return f"{diferencia.seconds // 60} min"
    elif segundos < 86400:
        return f"{diferencia.seconds // 3600} hrs"
    elif segundos < 604800:
        return f"{diferencia.days} días"
    elif segundos < 2592000:
        semanas = diferencia.days // 7
        return f"{semanas} sem"
    else:
        meses = diferencia.days // 30
        return f"{meses} mes"
    

def obtener_traslados_solicitud(usuario):
    estancia_usuario = usuario.estancia
    traslados_solicitud = Traslado.objects.filter(status=0, estacion_destino=estancia_usuario)
    return traslados_solicitud


def numero_traslados(request):
    if not request.user.is_authenticated:
        return {'traslados_solicitud': 0, 'tiempo_ultimo_traslado': None}

    traslados_solicitud = obtener_traslados_solicitud(request.user)
    
    if traslados_solicitud.exists():
        ultimo_traslado = traslados_solicitud.latest('fechaSolicitud')
        tiempo_ultimo = tiempo_desde(ultimo_traslado.fechaSolicitud)
    else:
        tiempo_ultimo = None

    return {'traslados_solicitud': traslados_solicitud.count(), 'tiempo_ultimo_traslado': tiempo_ultimo}


def total_notificaciones(request):
    if not request.user.is_authenticated:
        return {'total_notificaciones': 0}
    traslados_solicitud_count = obtener_traslados_solicitud(request.user).count()
    # Aquí agregarías cualquier otra lógica para otras notificaciones:
    # mensajes_nuevos = ...
    # solicitudes_amistad = ...
    total = traslados_solicitud_count  # + mensajes_nuevos + solicitudes_amistad
    return {'total_notificaciones': total}


# Agregar un clasificador de grupos 

def user_groups(request):
    groups = [group.name for group in request.user.groups.all()]
    return {'user_groups': groups}