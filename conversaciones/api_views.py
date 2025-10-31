from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Conversacion, Mensaje


@login_required
@api_view(['GET'])
def alertas_conversaciones_count(request):
    """Contador de conversaciones con mensajes no leídos"""
    if not request.user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists():
        return JsonResponse({'count': 0})
    
    # Contar alertas no vistas en el historial
    from .models import HistorialAlertaConversacion
    total_alertas = HistorialAlertaConversacion.objects.filter(
        operador=request.user,
        vista=False
    ).count()
    
    return JsonResponse({
        'count': total_alertas,
        'tipo': 'conversaciones'
    })


@login_required
@api_view(['GET'])
def alertas_conversaciones_preview(request):
    """Preview de mensajes no leídos para el dropdown"""
    if not request.user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists():
        return JsonResponse({'results': []})
    
    # Obtener últimos mensajes no leídos
    mensajes = Mensaje.objects.filter(
        conversacion__operador_asignado=request.user,
        conversacion__estado='activa',
        remitente='ciudadano',
        leido=False
    ).select_related('conversacion').order_by('-fecha_envio')[:5]
    
    results = []
    for mensaje in mensajes:
        results.append({
            'id': f'conv_{mensaje.conversacion.id}_{mensaje.id}',
            'conversacion_id': mensaje.conversacion.id,
            'mensaje': f'Nuevo mensaje en conversación #{mensaje.conversacion.id}',
            'contenido': mensaje.contenido[:100] + '...' if len(mensaje.contenido) > 100 else mensaje.contenido,
            'fecha': mensaje.fecha_envio.strftime('%d/%m/%Y %H:%M'),
            'prioridad': 'MEDIA',
            'ciudadano_nombre': f'Conversación #{mensaje.conversacion.id}'
        })
    
    # Agregar nuevas conversaciones sin asignar
    from .models import NuevaConversacionAlerta
    nuevas = NuevaConversacionAlerta.objects.filter(
        operador=request.user,
        vista=False,
        conversacion__estado='pendiente'
    ).select_related('conversacion').order_by('-creado')[:3]
    
    for nueva in nuevas:
        results.append({
            'id': f'nueva_conv_{nueva.conversacion.id}',
            'conversacion_id': nueva.conversacion.id,
            'mensaje': f'Nueva conversación #{nueva.conversacion.id} disponible',
            'contenido': 'Conversación sin asignar esperando atención',
            'fecha': nueva.creado.strftime('%d/%m/%Y %H:%M'),
            'prioridad': 'ALTA',
            'ciudadano_nombre': f'Nueva Conversación #{nueva.conversacion.id}'
        })
    
    return JsonResponse({'results': results})


@login_required
@api_view(['POST'])
def marcar_mensajes_leidos(request, conversacion_id):
    """Marcar mensajes como leídos cuando se abre la conversación"""
    try:
        conversacion = Conversacion.objects.get(
            id=conversacion_id,
            operador_asignado=request.user
        )
        
        # Marcar mensajes del ciudadano como leídos
        Mensaje.objects.filter(
            conversacion=conversacion,
            remitente='ciudadano',
            leido=False
        ).update(leido=True)
        
        return JsonResponse({'success': True})
    except Conversacion.DoesNotExist:
        return JsonResponse({'error': 'Conversación no encontrada'}, status=404)