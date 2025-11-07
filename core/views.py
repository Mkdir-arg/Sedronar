# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.models import (
    Localidad,
    Municipio,
)


@login_required
@require_GET
def load_municipios(request):
    """Carga municipios filtrados por provincia."""
    provincia_id = request.GET.get("provincia_id")
    municipios = Municipio.objects.filter(provincia=provincia_id).select_related('provincia')
    return JsonResponse(list(municipios.values("id", "nombre")), safe=False)


@login_required
@require_GET
def load_localidad(request):
    """Carga localidades filtradas por municipio."""
    municipio_id = request.GET.get("municipio_id")

    if municipio_id:
        localidades = Localidad.objects.filter(municipio=municipio_id).select_related('municipio')
    else:
        localidades = Localidad.objects.none()

    return JsonResponse(list(localidades.values("id", "nombre")), safe=False)


@login_required
def inicio_view(request):
    """Vista para la página de inicio del sistema"""
    from django.contrib.auth.models import User
    from legajos.models import Ciudadano
    from datetime import datetime, timedelta
    
    # Estadísticas básicas
    total_ciudadanos = Ciudadano.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    
    # Registros del mes actual
    inicio_mes = datetime.now().replace(day=1)
    registros_mes = Ciudadano.objects.filter(creado__gte=inicio_mes).count()
    
    # Actividad de hoy
    hoy = datetime.now().date()
    actividad_hoy = Ciudadano.objects.filter(creado__date=hoy).count()
    
    context = {
        'total_ciudadanos': total_ciudadanos,
        'usuarios_activos': usuarios_activos,
        'registros_mes': registros_mes,
        'actividad_hoy': actividad_hoy,
    }
    
    return render(request, "inicio.html", context)


def error_500_view(request):
    return render(request, "500.html")
