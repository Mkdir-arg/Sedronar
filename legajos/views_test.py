from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@login_required
def test_dashboard_contactos(request):
    """Vista de prueba para el dashboard de contactos"""
    return render(request, 'legajos/test_dashboard.html', {
        'mensaje': 'Dashboard de contactos funcionando correctamente'
    })