from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from .models import Conversacion, ColaAsignacion, MetricasOperador
import logging

logger = logging.getLogger(__name__)


class AsignadorAutomatico:
    """Servicio para asignación automática de conversaciones"""
    
    @staticmethod
    def obtener_operador_disponible():
        """Obtiene el operador más adecuado para asignar una conversación (solo operadores logueados)"""
        try:
            from django.contrib.sessions.models import Session
            from django.utils import timezone
            
            # Obtener usuarios actualmente logueados
            sesiones_activas = Session.objects.filter(expire_date__gte=timezone.now())
            usuarios_logueados = []
            
            for sesion in sesiones_activas:
                data = sesion.get_decoded()
                user_id = data.get('_auth_user_id')
                if user_id:
                    usuarios_logueados.append(int(user_id))
            
            # Buscar operadores disponibles que estén logueados
            cola_disponible = ColaAsignacion.objects.filter(
                activo=True,
                operador_id__in=usuarios_logueados,
                conversaciones_actuales__lt=models.F('max_conversaciones')
            ).order_by('conversaciones_actuales', 'ultima_asignacion').first()
            
            if cola_disponible:
                return cola_disponible.operador
            
            # Si no hay operadores disponibles con capacidad, buscar el menos cargado que esté logueado
            cola_menos_cargada = ColaAsignacion.objects.filter(
                activo=True,
                operador_id__in=usuarios_logueados
            ).order_by('conversaciones_actuales').first()
            
            return cola_menos_cargada.operador if cola_menos_cargada else None
            
        except Exception as e:
            logger.error(f"Error al obtener operador disponible: {e}")
            return None
    
    @staticmethod
    def asignar_conversacion_automatica(conversacion):
        """Asigna automáticamente una conversación al operador más adecuado"""
        try:
            operador = AsignadorAutomatico.obtener_operador_disponible()
            
            if operador:
                conversacion.asignar_operador(operador)
                
                # Actualizar cola del operador
                cola, created = ColaAsignacion.objects.get_or_create(
                    operador=operador,
                    defaults={'max_conversaciones': 5}
                )
                cola.actualizar_contador()
                cola.ultima_asignacion = timezone.now()
                cola.save()
                
                logger.info(f"Conversación {conversacion.id} asignada automáticamente a {operador.username}")
                return True
            else:
                logger.warning(f"No hay operadores disponibles para conversación {conversacion.id}")
                return False
                
        except Exception as e:
            logger.error(f"Error al asignar conversación automáticamente: {e}")
            return False
    
    @staticmethod
    def configurar_operador(operador, max_conversaciones=5, activo=True):
        """Configura un operador en el sistema de cola"""
        cola, created = ColaAsignacion.objects.get_or_create(
            operador=operador,
            defaults={
                'max_conversaciones': max_conversaciones,
                'activo': activo
            }
        )
        
        if not created:
            cola.max_conversaciones = max_conversaciones
            cola.activo = activo
            cola.save()
        
        cola.actualizar_contador()
        return cola
    
    @staticmethod
    def actualizar_todas_las_colas():
        """Actualiza los contadores de todas las colas"""
        for cola in ColaAsignacion.objects.all():
            cola.actualizar_contador()


class MetricasService:
    """Servicio para cálculo y actualización de métricas"""
    
    @staticmethod
    def calcular_metricas_globales():
        """Calcula métricas globales del sistema de conversaciones"""
        from django.db.models import Avg, Count, Q
        from datetime import datetime, timedelta
        
        ahora = timezone.now()
        hoy = ahora.date()
        semana_pasada = hoy - timedelta(days=7)
        mes_pasado = hoy - timedelta(days=30)
        
        metricas = {
            # Conversaciones totales
            'total_conversaciones': Conversacion.objects.count(),
            'conversaciones_hoy': Conversacion.objects.filter(fecha_inicio__date=hoy).count(),
            'conversaciones_semana': Conversacion.objects.filter(fecha_inicio__date__gte=semana_pasada).count(),
            'conversaciones_mes': Conversacion.objects.filter(fecha_inicio__date__gte=mes_pasado).count(),
            
            # Estados
            'pendientes': Conversacion.objects.filter(estado='pendiente').count(),
            'activas': Conversacion.objects.filter(estado='activa').count(),
            'cerradas_hoy': Conversacion.objects.filter(estado='cerrada', fecha_cierre__date=hoy).count(),
            
            # Tiempos de respuesta
            'tiempo_respuesta_promedio': Conversacion.objects.filter(
                tiempo_respuesta_segundos__isnull=False
            ).aggregate(promedio=Avg('tiempo_respuesta_segundos'))['promedio'] or 0,
            
            'tiempo_espera_promedio': Conversacion.objects.filter(
                tiempo_espera_segundos__gt=0
            ).aggregate(promedio=Avg('tiempo_espera_segundos'))['promedio'] or 0,
            
            # Satisfacción
            'satisfaccion_promedio': Conversacion.objects.filter(
                satisfaccion__isnull=False
            ).aggregate(promedio=Avg('satisfaccion'))['promedio'] or 0,
            
            # Operadores
            'operadores_activos': ColaAsignacion.objects.filter(activo=True).count(),
            'operadores_disponibles': ColaAsignacion.objects.filter(
                activo=True,
                conversaciones_actuales__lt=models.F('max_conversaciones')
            ).count(),
        }
        
        # Convertir segundos a minutos
        metricas['tiempo_respuesta_promedio_min'] = round(metricas['tiempo_respuesta_promedio'] / 60, 1)
        metricas['tiempo_espera_promedio_min'] = round(metricas['tiempo_espera_promedio'] / 60, 1)
        
        return metricas
    
    @staticmethod
    def actualizar_metricas_operador(operador):
        """Actualiza las métricas de un operador específico"""
        metricas, created = MetricasOperador.objects.get_or_create(
            operador=operador
        )
        metricas.actualizar_metricas()
        return metricas
    
    @staticmethod
    def actualizar_todas_las_metricas():
        """Actualiza las métricas de todos los operadores"""
        operadores = User.objects.filter(
            groups__name__in=['Conversaciones', 'OperadorCharla']
        )
        
        for operador in operadores:
            MetricasService.actualizar_metricas_operador(operador)


class NotificacionService:
    """Servicio para notificaciones en tiempo real"""
    
    @staticmethod
    def notificar_nueva_conversacion(conversacion):
        """Notifica a los operadores sobre una nueva conversación"""
        # TODO: Implementar con WebSockets cuando esté configurado
        try:
            # from channels.layers import get_channel_layer
            # from asgiref.sync import async_to_sync
            # 
            # channel_layer = get_channel_layer()
            # async_to_sync(channel_layer.group_send)(
            #     'conversaciones_operadores',
            #     {
            #         'type': 'nueva_conversacion',
            #         'conversacion': {
            #             'id': conversacion.id,
            #             'tipo': conversacion.get_tipo_display(),
            #             'prioridad': conversacion.get_prioridad_display(),
            #             'dni': conversacion.dni_ciudadano or 'Anónimo',
            #             'fecha': conversacion.fecha_inicio.strftime('%H:%M')
            #         }
            #     }
            # )
            logger.info(f"Notificación enviada para conversación {conversacion.id}")
        except Exception as e:
            logger.error(f"Error al enviar notificación: {e}")
    
    @staticmethod
    def notificar_mensaje(conversacion, mensaje):
        """Notifica sobre un nuevo mensaje en una conversación"""
        # TODO: Implementar con WebSockets
        try:
            # Notificar en el canal específico de la conversación
            # y en el canal general de operadores
            logger.info(f"Mensaje notificado en conversación {conversacion.id}")
        except Exception as e:
            logger.error(f"Error al notificar mensaje: {e}")