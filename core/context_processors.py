from .models import DispositivoRed

def dispositivos_context(request):
    """Agrega dispositivos al contexto global"""
    if request.user.is_authenticated and request.user.is_superuser:
        return {
            'todos_dispositivos': DispositivoRed.objects.filter(activo=True).order_by('nombre')
        }
    return {
        'todos_dispositivos': []
    }