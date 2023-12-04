def estacion_usuario(request):
    estacion = None
    if request.user.is_authenticated and hasattr(request.user, 'estancia'):
        estacion = request.user.estancia
    return {'estacion_usuario': estacion}