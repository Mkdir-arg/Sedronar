from .models import EventoCritico, AlertaEventoCritico


def alertas_eventos_criticos(request):
    """Context processor para mostrar alertas de eventos críticos al responsable"""
    
    if not request.user.is_authenticated:
        return {}
    
    # Obtener eventos críticos de legajos donde el usuario es responsable
    # y que no han sido vistos por el responsable
    eventos_pendientes = EventoCritico.objects.filter(
        legajo__responsable=request.user
    ).exclude(
        alertas_vistas__responsable=request.user
    ).select_related('legajo__ciudadano').order_by('-creado')[:5]  # Máximo 5 alertas
    
    return {
        'eventos_criticos_pendientes': eventos_pendientes
    }