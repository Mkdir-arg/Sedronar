from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from legajos.models import LegajoAtencion, Ciudadano, SeguimientoContacto, AlertaCiudadano
from users.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def metricas_dashboard(request):
    """Obtiene métricas principales del dashboard"""
    
    # Métricas básicas
    total_ciudadanos = Ciudadano.objects.count()
    total_legajos = LegajoAtencion.objects.count()
    legajos_activos = LegajoAtencion.objects.filter(estado__in=['ABIERTO', 'EN_SEGUIMIENTO']).count()
    alertas_activas = AlertaCiudadano.objects.filter(activa=True).count()
    
    # Seguimientos hoy
    hoy = timezone.now().date()
    seguimientos_hoy = SeguimientoContacto.objects.filter(creado__date=hoy).count()
    
    # Estados de legajos
    estados = LegajoAtencion.objects.values('estado').annotate(count=Count('id'))
    estados_dict = {estado['estado']: estado['count'] for estado in estados}
    
    # Usuarios conectados (últimas 24 horas)
    hace_24h = timezone.now() - timedelta(hours=24)
    usuarios_activos = User.objects.filter(last_login__gte=hace_24h).count()
    
    return Response({
        'metricas': {
            'ciudadanos': total_ciudadanos,
            'legajos': legajos_activos,
            'seguimientos': seguimientos_hoy,
            'alertas': alertas_activas
        },
        'estados_legajos': {
            'abiertos': estados_dict.get('ABIERTO', 0),
            'seguimiento': estados_dict.get('EN_SEGUIMIENTO', 0),
            'derivados': estados_dict.get('DERIVADO', 0),
            'cerrados': estados_dict.get('CERRADO', 0)
        },
        'usuarios_conectados': usuarios_activos
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def buscar_ciudadanos(request):
    """Búsqueda rápida de ciudadanos"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 3:
        return Response({'results': []})
    
    try:
        ciudadanos = Ciudadano.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(dni__icontains=query)
        )[:8]
        
        resultados = []
        for c in ciudadanos:
            resultados.append({
                'id': c.id,
                'nombre': f"{c.apellido}, {c.nombre}",
                'dni': c.dni
            })
        
        return Response({'results': resultados})
    except Exception as e:
        return Response({'results': [], 'error': str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def alertas_criticas(request):
    """Obtiene alertas críticas activas"""
    alertas = AlertaCiudadano.objects.filter(
        activa=True,
        prioridad__in=['CRITICA', 'ALTA']
    ).select_related('ciudadano').order_by('-fecha_creacion')[:5]
    
    alertas_data = []
    for alerta in alertas:
        alertas_data.append({
            'id': alerta.id,
            'ciudadano': f"{alerta.ciudadano.apellido}, {alerta.ciudadano.nombre}",
            'tipo': alerta.get_tipo_display(),
            'prioridad': alerta.prioridad,
            'fecha': alerta.fecha_creacion.strftime('%d/%m %H:%M'),
            'mensaje': alerta.mensaje
        })
    
    return Response({'results': alertas_data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def actividad_reciente(request):
    """Obtiene actividad reciente del sistema"""
    
    # Legajos recientes
    legajos_nuevos = LegajoAtencion.objects.select_related('ciudadano', 'responsable').order_by('-fecha_apertura')[:3]
    
    # Seguimientos recientes
    seguimientos = SeguimientoContacto.objects.select_related('legajo__ciudadano', 'creado_por').order_by('-creado')[:3]
    
    # Alertas recientes
    alertas = AlertaCiudadano.objects.select_related('ciudadano').filter(activa=True).order_by('-fecha_creacion')[:2]
    
    actividades = []
    
    # Agregar legajos
    for legajo in legajos_nuevos:
        actividades.append({
            'descripcion': f'Nuevo legajo para {legajo.ciudadano.apellido}, {legajo.ciudadano.nombre}',
            'usuario': legajo.responsable.get_full_name() if legajo.responsable else 'Sistema',
            'tiempo': _tiempo_relativo(legajo.fecha_apertura),
            'tipo': 'create',
            'icono': 'fas fa-plus'
        })
    
    # Agregar seguimientos
    for seguimiento in seguimientos:
        actividades.append({
            'descripcion': f'Seguimiento: {seguimiento.tipo_contacto}',
            'usuario': seguimiento.creado_por.get_full_name() if seguimiento.creado_por else 'Sistema',
            'tiempo': _tiempo_relativo(seguimiento.creado),
            'tipo': 'update',
            'icono': 'fas fa-check'
        })
    
    # Agregar alertas
    for alerta in alertas:
        actividades.append({
            'descripcion': f'Alerta: {alerta.get_tipo_display()}',
            'usuario': 'Sistema',
            'tiempo': _tiempo_relativo(alerta.fecha_creacion),
            'tipo': 'alert',
            'icono': 'fas fa-exclamation-triangle'
        })
    
    # Ordenar por tiempo
    actividades.sort(key=lambda x: x['tiempo'], reverse=True)
    
    return Response({'results': actividades[:8]})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tendencias_datos(request):
    """Obtiene datos para gráfico de tendencias"""
    periodo = request.GET.get('periodo', '30d')
    
    if periodo == '7d':
        dias = 7
    elif periodo == '90d':
        dias = 90
    else:
        dias = 30
    
    fecha_inicio = timezone.now().date() - timedelta(days=dias)
    
    # Datos por día
    datos = []
    labels = []
    
    for i in range(dias):
        fecha = fecha_inicio + timedelta(days=i)
        count = LegajoAtencion.objects.filter(fecha_apertura=fecha).count()
        datos.append(count)
        labels.append(fecha.strftime('%d/%m'))
    
    return Response({
        'labels': labels,
        'datos': datos
    })

def _tiempo_relativo(fecha):
    """Convierte fecha a tiempo relativo"""
    if isinstance(fecha, datetime):
        fecha = fecha.replace(tzinfo=None)
    elif hasattr(fecha, 'date'):
        fecha = datetime.combine(fecha, datetime.min.time())
    
    ahora = datetime.now()
    diff = ahora - fecha
    
    if diff.days > 0:
        return f'Hace {diff.days} día{"s" if diff.days > 1 else ""}'
    elif diff.seconds > 3600:
        horas = diff.seconds // 3600
        return f'Hace {horas} hora{"s" if horas > 1 else ""}'
    elif diff.seconds > 60:
        minutos = diff.seconds // 60
        return f'Hace {minutos} minuto{"s" if minutos > 1 else ""}'
    else:
        return 'Hace unos segundos'