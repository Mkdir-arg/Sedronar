from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import AlertaCiudadano
from .services_alertas import AlertasService


@login_required
def alertas_dashboard(request):
    """Vista principal del dashboard de alertas"""
    alertas_criticas = AlertaCiudadano.objects.filter(
        activa=True,
        prioridad='CRITICA'
    ).select_related('ciudadano', 'legajo').order_by('-creado')[:10]
    
    alertas_altas = AlertaCiudadano.objects.filter(
        activa=True,
        prioridad='ALTA'
    ).select_related('ciudadano', 'legajo').order_by('-creado')[:10]
    
    alertas_medias = AlertaCiudadano.objects.filter(
        activa=True,
        prioridad='MEDIA'
    ).select_related('ciudadano', 'legajo').order_by('-creado')[:10]
    
    # Estadísticas
    stats = {
        'total': AlertaCiudadano.objects.filter(activa=True).count(),
        'criticas': alertas_criticas.count(),
        'altas': alertas_altas.count(),
        'medias': alertas_medias.count(),
    }
    
    context = {
        'alertas_criticas': alertas_criticas,
        'alertas_altas': alertas_altas,
        'alertas_medias': alertas_medias,
        'stats': stats,
    }
    
    return render(request, 'legajos/alertas_dashboard.html', context)


@login_required
def cerrar_alerta_ajax(request, alerta_id):
    """Cierra una alerta vía AJAX"""
    if request.method == 'POST':
        success = AlertasService.cerrar_alerta(alerta_id, request.user)
        return JsonResponse({'success': success})
    
    return JsonResponse({'success': False})


@login_required
def alertas_count_ajax(request):
    """Obtiene el contador de alertas para el navbar"""
    count = AlertaCiudadano.objects.filter(activa=True).count()
    criticas = AlertaCiudadano.objects.filter(activa=True, prioridad='CRITICA').count()
    
    return JsonResponse({
        'count': count,
        'criticas': criticas
    })