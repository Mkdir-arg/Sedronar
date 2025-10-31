from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import timedelta
from .models_auditoria import LogAccion, LogDescargaArchivo, SesionUsuario, AlertaAuditoria


class ServicioAlertas:
    """Servicio para generar alertas automáticas de auditoría"""
    
    @staticmethod
    def verificar_multiples_logins():
        """Detectar múltiples inicios de sesión simultáneos"""
        hace_1_hora = timezone.now() - timedelta(hours=1)
        
        usuarios_multiples_sesiones = SesionUsuario.objects.filter(
            inicio_sesion__gte=hace_1_hora,
            activa=True
        ).values('usuario').annotate(
            sesiones_count=Count('id')
        ).filter(sesiones_count__gt=2)
        
        for item in usuarios_multiples_sesiones:
            usuario = User.objects.get(id=item['usuario'])
            
            # Verificar si ya existe alerta reciente
            alerta_existente = AlertaAuditoria.objects.filter(
                tipo=AlertaAuditoria.TipoAlerta.MULTIPLES_LOGINS,
                usuario_afectado=usuario,
                timestamp__gte=hace_1_hora,
                revisada=False
            ).exists()
            
            if not alerta_existente:
                AlertaAuditoria.objects.create(
                    tipo=AlertaAuditoria.TipoAlerta.MULTIPLES_LOGINS,
                    severidad=AlertaAuditoria.Severidad.MEDIA,
                    usuario_afectado=usuario,
                    descripcion=f"Usuario con {item['sesiones_count']} sesiones activas simultáneas",
                    detalles={'sesiones_count': item['sesiones_count']}
                )
    
    @staticmethod
    def verificar_actividad_sospechosa():
        """Detectar actividad sospechosa (muchas acciones en poco tiempo)"""
        hace_10_minutos = timezone.now() - timedelta(minutes=10)
        
        usuarios_actividad_alta = LogAccion.objects.filter(
            timestamp__gte=hace_10_minutos,
            usuario__isnull=False
        ).values('usuario').annotate(
            acciones_count=Count('id')
        ).filter(acciones_count__gt=50)  # Más de 50 acciones en 10 minutos
        
        for item in usuarios_actividad_alta:
            usuario = User.objects.get(id=item['usuario'])
            
            # Verificar si ya existe alerta reciente
            hace_1_hora = timezone.now() - timedelta(hours=1)
            alerta_existente = AlertaAuditoria.objects.filter(
                tipo=AlertaAuditoria.TipoAlerta.ACTIVIDAD_SOSPECHOSA,
                usuario_afectado=usuario,
                timestamp__gte=hace_1_hora,
                revisada=False
            ).exists()
            
            if not alerta_existente:
                AlertaAuditoria.objects.create(
                    tipo=AlertaAuditoria.TipoAlerta.ACTIVIDAD_SOSPECHOSA,
                    severidad=AlertaAuditoria.Severidad.ALTA,
                    usuario_afectado=usuario,
                    descripcion=f"Actividad inusualmente alta: {item['acciones_count']} acciones en 10 minutos",
                    detalles={'acciones_count': item['acciones_count'], 'periodo': '10_minutos'}
                )
    
    @staticmethod
    def verificar_descarga_masiva():
        """Detectar descargas masivas de archivos"""
        hace_1_hora = timezone.now() - timedelta(hours=1)
        
        usuarios_descargas_masivas = LogDescargaArchivo.objects.filter(
            timestamp__gte=hace_1_hora,
            usuario__isnull=False
        ).values('usuario').annotate(
            descargas_count=Count('id')
        ).filter(descargas_count__gt=10)  # Más de 10 descargas en 1 hora
        
        for item in usuarios_descargas_masivas:
            usuario = User.objects.get(id=item['usuario'])
            
            # Verificar si ya existe alerta reciente
            alerta_existente = AlertaAuditoria.objects.filter(
                tipo=AlertaAuditoria.TipoAlerta.DESCARGA_MASIVA,
                usuario_afectado=usuario,
                timestamp__gte=hace_1_hora,
                revisada=False
            ).exists()
            
            if not alerta_existente:
                AlertaAuditoria.objects.create(
                    tipo=AlertaAuditoria.TipoAlerta.DESCARGA_MASIVA,
                    severidad=AlertaAuditoria.Severidad.ALTA,
                    usuario_afectado=usuario,
                    descripcion=f"Descarga masiva detectada: {item['descargas_count']} archivos en 1 hora",
                    detalles={'descargas_count': item['descargas_count'], 'periodo': '1_hora'}
                )
    
    @staticmethod
    def verificar_acceso_fuera_horario():
        """Detectar accesos fuera del horario laboral"""
        ahora = timezone.now()
        hora_actual = ahora.hour
        
        # Considerar fuera de horario: antes de 7 AM o después de 10 PM
        if hora_actual < 7 or hora_actual > 22:
            hace_30_minutos = ahora - timedelta(minutes=30)
            
            logins_fuera_horario = LogAccion.objects.filter(
                accion=LogAccion.TipoAccion.LOGIN,
                timestamp__gte=hace_30_minutos,
                usuario__isnull=False
            )
            
            for login in logins_fuera_horario:
                # Verificar si ya existe alerta reciente
                hace_1_hora = ahora - timedelta(hours=1)
                alerta_existente = AlertaAuditoria.objects.filter(
                    tipo=AlertaAuditoria.TipoAlerta.ACCESO_FUERA_HORARIO,
                    usuario_afectado=login.usuario,
                    timestamp__gte=hace_1_hora,
                    revisada=False
                ).exists()
                
                if not alerta_existente:
                    AlertaAuditoria.objects.create(
                        tipo=AlertaAuditoria.TipoAlerta.ACCESO_FUERA_HORARIO,
                        severidad=AlertaAuditoria.Severidad.MEDIA,
                        usuario_afectado=login.usuario,
                        descripcion=f"Acceso fuera del horario laboral a las {login.timestamp.strftime('%H:%M')}",
                        detalles={'hora_acceso': login.timestamp.strftime('%H:%M'), 'ip': login.ip_address}
                    )
    
    @classmethod
    def ejecutar_verificaciones(cls):
        """Ejecutar todas las verificaciones de alertas"""
        try:
            cls.verificar_multiples_logins()
            cls.verificar_actividad_sospechosa()
            cls.verificar_descarga_masiva()
            cls.verificar_acceso_fuera_horario()
        except Exception as e:
            # Log del error pero no fallar
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en verificaciones de auditoría: {e}")


class ServicioReportes:
    """Servicio para generar reportes de auditoría"""
    
    @staticmethod
    def reporte_actividad_usuario(usuario, fecha_desde=None, fecha_hasta=None):
        """Generar reporte de actividad de un usuario específico"""
        if not fecha_desde:
            fecha_desde = timezone.now().date() - timedelta(days=30)
        if not fecha_hasta:
            fecha_hasta = timezone.now().date()
        
        acciones = LogAccion.objects.filter(
            usuario=usuario,
            timestamp__date__range=[fecha_desde, fecha_hasta]
        )
        
        descargas = LogDescargaArchivo.objects.filter(
            usuario=usuario,
            timestamp__date__range=[fecha_desde, fecha_hasta]
        )
        
        sesiones = SesionUsuario.objects.filter(
            usuario=usuario,
            inicio_sesion__date__range=[fecha_desde, fecha_hasta]
        )
        
        return {
            'usuario': usuario,
            'periodo': {'desde': fecha_desde, 'hasta': fecha_hasta},
            'total_acciones': acciones.count(),
            'total_descargas': descargas.count(),
            'total_sesiones': sesiones.count(),
            'acciones_por_tipo': acciones.values('accion').annotate(count=Count('id')),
            'sesiones_promedio_duracion': cls._calcular_duracion_promedio_sesiones(sesiones),
        }
    
    @staticmethod
    def _calcular_duracion_promedio_sesiones(sesiones):
        """Calcular duración promedio de sesiones"""
        duraciones = []
        for sesion in sesiones:
            if sesion.fin_sesion:
                duracion = sesion.fin_sesion - sesion.inicio_sesion
                duraciones.append(duracion.total_seconds())
        
        if duraciones:
            promedio_segundos = sum(duraciones) / len(duraciones)
            return timedelta(seconds=promedio_segundos)
        return timedelta(0)