from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Count
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import (
    AlertaCiudadano, LegajoAtencion, Ciudadano, EvaluacionInicial,
    PlanIntervencion, EventoCritico, Derivacion, Consentimiento
)
from .models_contactos import HistorialContacto, VinculoFamiliar


class AlertasService:
    """Servicio para generar y gestionar alertas automáticas"""
    
    @staticmethod
    def generar_alertas_ciudadano(ciudadano_id):
        """Genera todas las alertas para un ciudadano específico"""
        try:
            ciudadano = Ciudadano.objects.get(id=ciudadano_id)
            legajos = LegajoAtencion.objects.filter(ciudadano=ciudadano)
            
            # Limpiar alertas existentes no críticas
            AlertaCiudadano.objects.filter(
                ciudadano=ciudadano,
                activa=True,
                prioridad__in=['MEDIA', 'BAJA']
            ).update(activa=False)
            
            alertas_generadas = []
            
            for legajo in legajos:
                alertas_generadas.extend(AlertasService._generar_alertas_legajo(legajo))
            
            # Alertas generales del ciudadano
            alertas_generadas.extend(AlertasService._generar_alertas_generales(ciudadano))
            
            return alertas_generadas
            
        except Exception as e:
            print(f"Error generando alertas: {e}")
            return []
    
    @staticmethod
    def _generar_alertas_legajo(legajo):
        """Genera alertas específicas de un legajo"""
        alertas = []
        
        # 1. Riesgo Alto
        if legajo.nivel_riesgo == 'ALTO':
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'RIESGO_ALTO', 'ALTA',
                f'Legajo con nivel de riesgo alto'
            ))
        
        # 2. Sin Evaluación Inicial
        if not hasattr(legajo, 'evaluacion'):
            dias_sin_eval = (timezone.now().date() - legajo.fecha_apertura).days
            if dias_sin_eval > 15:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'SIN_EVALUACION', 'MEDIA',
                    f'Sin evaluación inicial hace {dias_sin_eval} días'
                ))
        
        # 3. Evaluación con riesgos
        try:
            evaluacion = legajo.evaluacion
            if evaluacion.riesgo_suicida:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'RIESGO_SUICIDA', 'CRITICA',
                    'Riesgo suicida identificado en evaluación'
                ))
            if evaluacion.violencia:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'VIOLENCIA', 'CRITICA',
                    'Situación de violencia identificada'
                ))
        except:
            pass
        
        # 4. Sin Plan de Intervención
        if legajo.estado in ['ABIERTO', 'EN_SEGUIMIENTO'] and not legajo.plan_vigente:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'SIN_PLAN', 'MEDIA',
                'Legajo activo sin plan de intervención'
            ))
        
        # 5. Sin Contacto Prolongado
        ultimo_contacto = HistorialContacto.objects.filter(
            legajo=legajo
        ).order_by('-fecha_contacto').first()
        
        if ultimo_contacto:
            dias_sin_contacto = (timezone.now().date() - ultimo_contacto.fecha_contacto.date()).days
            if dias_sin_contacto > 30:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'SIN_CONTACTO', 'ALTA',
                    f'Sin contacto hace {dias_sin_contacto} días'
                ))
        
        # 6. Contactos Fallidos
        contactos_fallidos = HistorialContacto.objects.filter(
            legajo=legajo,
            estado='NO_CONTESTA',
            fecha_contacto__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        if contactos_fallidos >= 3:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'CONTACTOS_FALLIDOS', 'MEDIA',
                f'{contactos_fallidos} contactos fallidos en el último mes'
            ))
        
        # 7. Eventos Críticos Recientes
        eventos_recientes = EventoCritico.objects.filter(
            legajo=legajo,
            creado__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        if eventos_recientes > 0:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'EVENTO_CRITICO', 'CRITICA',
                f'{eventos_recientes} evento(s) crítico(s) en la última semana'
            ))
        
        # 8. Derivaciones Pendientes
        derivaciones_pendientes = Derivacion.objects.filter(
            legajo=legajo,
            estado='PENDIENTE',
            creado__lte=timezone.now() - timedelta(days=7)
        ).count()
        
        if derivaciones_pendientes > 0:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'DERIVACION_PENDIENTE', 'MEDIA',
                f'{derivaciones_pendientes} derivación(es) pendiente(s)'
            ))
        
        # 9. Seguimientos Vencidos
        try:
            from .models import SeguimientoContacto
            seguimientos_vencidos = SeguimientoContacto.objects.filter(
                legajo=legajo,
                fecha_proximo_contacto__lt=timezone.now().date(),
                fecha_proximo_contacto__isnull=False
            ).count()
            
            if seguimientos_vencidos > 0:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'SEGUIMIENTO_VENCIDO', 'ALTA',
                    f'{seguimientos_vencidos} seguimiento(s) vencido(s)'
                ))
        except:
            pass
        
        # 10. Adherencia Baja
        try:
            seguimientos_recientes = SeguimientoContacto.objects.filter(
                legajo=legajo,
                creado__gte=timezone.now() - timedelta(days=30),
                adherencia__in=['BAJA', 'NULA']
            ).count()
            
            if seguimientos_recientes >= 2:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'ADHERENCIA_BAJA', 'ALTA',
                    f'Adherencia baja en {seguimientos_recientes} seguimientos recientes'
                ))
        except:
            pass
        
        return alertas
    
    @staticmethod
    def _generar_alertas_generales(ciudadano):
        """Genera alertas generales del ciudadano"""
        alertas = []
        
        # 1. Sin Red Familiar
        vinculos = VinculoFamiliar.objects.filter(
            ciudadano_principal=ciudadano,
            activo=True
        ).count()
        
        if vinculos == 0:
            alertas.append(AlertasService._crear_alerta(
                ciudadano, None, 'SIN_RED_FAMILIAR', 'BAJA',
                'Sin vínculos familiares registrados'
            ))
        
        # 2. Sin Consentimiento
        consentimiento_vigente = Consentimiento.objects.filter(
            ciudadano=ciudadano,
            vigente=True
        ).exists()
        
        if not consentimiento_vigente:
            alertas.append(AlertasService._crear_alerta(
                ciudadano, None, 'SIN_CONSENTIMIENTO', 'MEDIA',
                'Sin consentimiento informado vigente'
            ))
        
        return alertas
    
    @staticmethod
    def _crear_alerta(ciudadano, legajo, tipo, prioridad, mensaje):
        """Crea una alerta si no existe una similar activa"""
        alerta_existente = AlertaCiudadano.objects.filter(
            ciudadano=ciudadano,
            legajo=legajo,
            tipo=tipo,
            activa=True
        ).first()
        
        if not alerta_existente:
            alerta = AlertaCiudadano.objects.create(
                ciudadano=ciudadano,
                legajo=legajo,
                tipo=tipo,
                prioridad=prioridad,
                mensaje=mensaje
            )
            
            # Enviar notificación WebSocket
            AlertasService._enviar_notificacion_alerta(alerta)
            
            return alerta
        
        return alerta_existente
    
    @staticmethod
    def _enviar_notificacion_alerta(alerta):
        """Envía notificación WebSocket para nueva alerta"""
        try:
            channel_layer = get_channel_layer()
            
            alerta_data = {
                'id': alerta.id,
                'ciudadano': alerta.ciudadano.nombre_completo,
                'ciudadano_id': alerta.ciudadano.id,
                'tipo': alerta.tipo,
                'prioridad': alerta.prioridad,
                'mensaje': alerta.mensaje,
                'fecha': alerta.creado.strftime('%d/%m/%Y %H:%M'),
                'legajo_id': alerta.legajo.id if alerta.legajo else None
            }
            
            # Notificación general
            async_to_sync(channel_layer.group_send)(
                'alertas_sistema',
                {
                    'type': 'nueva_alerta',
                    'alerta': alerta_data
                }
            )
            
            # Notificación especial para alertas críticas
            if alerta.prioridad == 'CRITICA':
                async_to_sync(channel_layer.group_send)(
                    'alertas_sistema',
                    {
                        'type': 'alerta_critica',
                        'alerta': alerta_data
                    }
                )
        except Exception as e:
            print(f"Error enviando notificación WebSocket: {e}")
    
    @staticmethod
    def obtener_alertas_ciudadano(ciudadano_id):
        """Obtiene todas las alertas activas de un ciudadano"""
        return AlertaCiudadano.objects.filter(
            ciudadano_id=ciudadano_id,
            activa=True
        ).order_by('prioridad', '-creado')
    
    @staticmethod
    def cerrar_alerta(alerta_id, usuario=None):
        """Cierra una alerta específica"""
        try:
            alerta = AlertaCiudadano.objects.get(id=alerta_id, activa=True)
            alerta.cerrar(usuario)
            
            # Notificar cierre de alerta
            try:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    'alertas_sistema',
                    {
                        'type': 'alerta_cerrada',
                        'alerta_id': alerta_id
                    }
                )
            except:
                pass
            
            return True
        except AlertaCiudadano.DoesNotExist:
            return False
    
    @staticmethod
    def generar_alerta_mensaje_ciudadano(conversacion):
        """Genera alerta cuando ciudadano envía mensaje"""
        try:
            if hasattr(conversacion, 'ciudadano_relacionado') and conversacion.ciudadano_relacionado:
                if not conversacion.operador_asignado:
                    alerta = AlertaCiudadano.objects.create(
                        ciudadano=conversacion.ciudadano_relacionado,
                        tipo='MENSAJE_SIN_OPERADOR',
                        prioridad='ALTA',
                        mensaje='Nuevo mensaje de ciudadano sin operador asignado'
                    )
                    AlertasService._enviar_notificacion_alerta(alerta)
        except Exception as e:
            print(f"Error generando alerta de mensaje: {e}")
    
    @staticmethod
    def generar_alerta_seguimiento_vencido(seguimiento):
        """Genera alerta cuando un seguimiento está vencido"""
        try:
            if seguimiento.fecha_proximo_contacto and seguimiento.fecha_proximo_contacto < timezone.now().date():
                dias_vencido = (timezone.now().date() - seguimiento.fecha_proximo_contacto).days
                prioridad = 'CRITICA' if dias_vencido > 7 else 'ALTA'
                
                alerta = AlertaCiudadano.objects.create(
                    ciudadano=seguimiento.legajo.ciudadano,
                    legajo=seguimiento.legajo,
                    tipo='SEGUIMIENTO_VENCIDO',
                    prioridad=prioridad,
                    mensaje=f'Seguimiento vencido hace {dias_vencido} días'
                )
                
                AlertasService._enviar_notificacion_alerta(alerta)
                return alerta
        except Exception as e:
            print(f"Error generando alerta de seguimiento vencido: {e}")
            return None
    
    @staticmethod
    def generar_alerta_evento_critico(legajo, tipo_evento, descripcion):
        """Genera alerta inmediata por evento crítico"""
        try:
            alerta = AlertaCiudadano.objects.create(
                ciudadano=legajo.ciudadano,
                legajo=legajo,
                tipo='EVENTO_CRITICO_INMEDIATO',
                prioridad='CRITICA',
                mensaje=f'EVENTO CRÍTICO: {tipo_evento} - {descripcion}'
            )
            
            AlertasService._enviar_notificacion_alerta(alerta)
            return alerta
        except Exception as e:
            print(f"Error generando alerta crítica: {e}")
            return None