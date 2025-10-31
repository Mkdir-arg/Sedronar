from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

from .models import Conversacion, Mensaje
from legajos.services_alertas import AlertasService


@receiver(post_save, sender=Conversacion)
def alerta_nueva_conversacion(sender, instance, created, **kwargs):
    """Genera alerta cuando se crea nueva conversación"""
    if created:
        try:
            if hasattr(instance, 'ciudadano_relacionado') and instance.ciudadano_relacionado:
                from legajos.models import AlertaCiudadano
                
                alerta = AlertaCiudadano.objects.create(
                    ciudadano=instance.ciudadano_relacionado,
                    tipo='NUEVA_CONVERSACION',
                    prioridad='MEDIA',
                    mensaje=f'Nueva conversación iniciada por {instance.ciudadano_relacionado.nombre_completo}'
                )
                AlertasService._enviar_notificacion_alerta(alerta)
        except Exception as e:
            print(f"Error generando alerta de nueva conversación: {e}")


@receiver(pre_save, sender=Conversacion)
def alerta_conversacion_cerrada(sender, instance, **kwargs):
    """Genera alerta cuando se cierra conversación"""
    if instance.pk:
        try:
            conversacion_anterior = Conversacion.objects.get(pk=instance.pk)
            if conversacion_anterior.estado != 'CERRADA' and instance.estado == 'CERRADA':
                if hasattr(instance, 'ciudadano_relacionado') and instance.ciudadano_relacionado:
                    from legajos.models import AlertaCiudadano
                    
                    # Calcular duración de la conversación
                    duracion = timezone.now() - instance.creado
                    
                    alerta = AlertaCiudadano.objects.create(
                        ciudadano=instance.ciudadano_relacionado,
                        tipo='CONVERSACION_CERRADA',
                        prioridad='BAJA',
                        mensaje=f'Conversación cerrada. Duración: {duracion.seconds//60} minutos'
                    )
                    AlertasService._enviar_notificacion_alerta(alerta)
        except Conversacion.DoesNotExist:
            pass
        except Exception as e:
            print(f"Error generando alerta de conversación cerrada: {e}")


@receiver(post_save, sender=Mensaje)
def verificar_tiempo_respuesta(sender, instance, created, **kwargs):
    """Verifica tiempo de respuesta en conversaciones"""
    if created and instance.remitente == 'ciudadano':
        try:
            conversacion = instance.conversacion
            
            # Verificar si hay operador asignado
            if not conversacion.operador_asignado:
                return
            
            # Buscar último mensaje del operador
            ultimo_msg_operador = conversacion.mensajes.filter(
                remitente='operador',
                fecha_envio__lt=instance.fecha_envio
            ).order_by('-fecha_envio').first()
            
            if ultimo_msg_operador:
                # Verificar si el ciudadano respondió muy rápido (posible crisis)
                tiempo_respuesta = instance.fecha_envio - ultimo_msg_operador.fecha_envio
                
                if tiempo_respuesta < timedelta(minutes=2):
                    if hasattr(conversacion, 'ciudadano_relacionado') and conversacion.ciudadano_relacionado:
                        from legajos.models import AlertaCiudadano
                        
                        alerta = AlertaCiudadano.objects.create(
                            ciudadano=conversacion.ciudadano_relacionado,
                            tipo='RESPUESTA_RAPIDA_CIUDADANO',
                            prioridad='MEDIA',
                            mensaje=f'Ciudadano respondió muy rápido ({tiempo_respuesta.seconds}s) - posible urgencia'
                        )
                        AlertasService._enviar_notificacion_alerta(alerta)
        except Exception as e:
            print(f"Error verificando tiempo de respuesta: {e}")