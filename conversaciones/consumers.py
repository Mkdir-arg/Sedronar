import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Conversacion, Mensaje


class ConversacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversacion_id = self.scope['url_route']['kwargs']['conversacion_id']
        self.room_group_name = f'conversacion_{self.conversacion_id}'
        
        # Verificar permisos
        if not await self.tiene_permiso():
            await self.close()
            return
        
        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        mensaje = data['mensaje']
        
        # Guardar mensaje en BD
        mensaje_obj = await self.crear_mensaje(mensaje)
        
        if mensaje_obj:
            # Enviar mensaje al grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'mensaje': {
                        'id': mensaje_obj.id,
                        'contenido': mensaje_obj.contenido,
                        'remitente': mensaje_obj.remitente,
                        'fecha': mensaje_obj.fecha_envio.strftime('%H:%M'),
                        'usuario': self.scope['user'].get_full_name() or self.scope['user'].username
                    }
                }
            )
            
            # Generar alerta por respuesta del operador
            await self.generar_alerta_respuesta_operador(mensaje_obj)
    
    async def chat_message(self, event):
        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'type': 'mensaje',
            'mensaje': event['mensaje']
        }))
    
    @database_sync_to_async
    def tiene_permiso(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return False
        
        # Verificar si tiene permisos de conversaciones
        return (user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists() 
                or user.is_superuser)
    
    @database_sync_to_async
    def crear_mensaje(self, contenido):
        try:
            conversacion = Conversacion.objects.get(id=self.conversacion_id)
            user = self.scope['user']
            
            # Verificar que puede responder
            if conversacion.operador_asignado and conversacion.operador_asignado != user:
                return None
            
            # Asignar operador si no tiene
            if not conversacion.operador_asignado:
                conversacion.operador_asignado = user
                conversacion.save()
                # Generar alerta de asignación
                self.generar_alerta_asignacion(conversacion, user)
            
            mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                remitente='operador',
                contenido=contenido
            )
            return mensaje
        except:
            return None
    
    @database_sync_to_async
    def generar_alerta_asignacion(self, conversacion, operador):
        """Genera alerta cuando se asigna operador a conversación"""
        try:
            from legajos.models import AlertaCiudadano
            from legajos.services_alertas import AlertasService
            
            # Buscar ciudadano relacionado si existe
            ciudadano = None
            if hasattr(conversacion, 'ciudadano_relacionado'):
                ciudadano = conversacion.ciudadano_relacionado
            
            if ciudadano:
                alerta = AlertaCiudadano.objects.create(
                    ciudadano=ciudadano,
                    tipo='OPERADOR_ASIGNADO',
                    prioridad='BAJA',
                    mensaje=f'Operador {operador.get_full_name() or operador.username} asignado a conversación'
                )
                AlertasService._enviar_notificacion_alerta(alerta)
        except:
            pass
    
    async def generar_alerta_respuesta_operador(self, mensaje):
        """Genera alerta por respuesta rápida del operador"""
        try:
            await self.database_sync_to_async(self._crear_alerta_respuesta)(mensaje)
        except:
            pass
    
    @database_sync_to_async
    def _crear_alerta_respuesta(self, mensaje):
        """Crea alerta de respuesta del operador"""
        try:
            from legajos.models import AlertaCiudadano
            from legajos.services_alertas import AlertasService
            from django.utils import timezone
            from datetime import timedelta
            
            conversacion = mensaje.conversacion
            
            # Verificar si hay ciudadano relacionado
            ciudadano = None
            if hasattr(conversacion, 'ciudadano_relacionado'):
                ciudadano = conversacion.ciudadano_relacionado
            
            if ciudadano:
                # Verificar tiempo de respuesta
                ultimo_mensaje_ciudadano = conversacion.mensajes.filter(
                    remitente='ciudadano'
                ).order_by('-fecha_envio').first()
                
                if ultimo_mensaje_ciudadano:
                    tiempo_respuesta = mensaje.fecha_envio - ultimo_mensaje_ciudadano.fecha_envio
                    
                    # Alerta si respuesta muy rápida (< 1 minuto) - posible respuesta automática
                    if tiempo_respuesta < timedelta(minutes=1):
                        alerta = AlertaCiudadano.objects.create(
                            ciudadano=ciudadano,
                            tipo='RESPUESTA_RAPIDA',
                            prioridad='BAJA',
                            mensaje=f'Respuesta muy rápida del operador ({tiempo_respuesta.seconds}s)'
                        )
                        AlertasService._enviar_notificacion_alerta(alerta)
        except:
            pass


class ConversacionesListConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Verificar permisos
        if not await self.tiene_permiso():
            await self.close()
            return
        
        self.room_group_name = 'conversaciones_list'
        
        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def nueva_conversacion(self, event):
        # Notificar nueva conversación
        await self.send(text_data=json.dumps({
            'type': 'nueva_conversacion',
            'conversacion_id': event.get('conversacion_id'),
            'mensaje': event.get('mensaje', 'Nueva conversación disponible')
        }))
    
    async def nuevo_mensaje(self, event):
        # Notificar nuevo mensaje
        await self.send(text_data=json.dumps({
            'type': 'nuevo_mensaje',
            'conversacion_id': event.get('conversacion_id'),
            'mensaje': event.get('mensaje', '')
        }))
    
    async def actualizar_lista(self, event):
        # Notificar que se debe actualizar la lista
        await self.send(text_data=json.dumps({
            'type': 'actualizar_lista',
            'mensaje': event['mensaje']
        }))
    
    @database_sync_to_async
    def tiene_permiso(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return False
        
        return (user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists() 
                or user.is_superuser)


class AlertasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Verificar permisos
        if not await self.tiene_permiso_alertas():
            await self.close()
            return
        
        self.room_group_name = 'alertas_sistema'
        
        # Unirse al grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def nueva_alerta(self, event):
        # Notificar nueva alerta
        await self.send(text_data=json.dumps({
            'type': 'nueva_alerta',
            'alerta': event['alerta']
        }))
    
    async def alerta_critica(self, event):
        # Notificar alerta crítica
        await self.send(text_data=json.dumps({
            'type': 'alerta_critica',
            'alerta': event['alerta']
        }))
    
    async def alerta_cerrada(self, event):
        # Notificar alerta cerrada
        await self.send(text_data=json.dumps({
            'type': 'alerta_cerrada',
            'alerta_id': event['alerta_id']
        }))
    
    @database_sync_to_async
    def tiene_permiso_alertas(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return False
        
        return (user.groups.filter(name__in=['Legajos', 'Supervisores', 'Coordinadores']).exists() 
                or user.is_superuser)


class AlertasConversacionesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Verificar permisos para conversaciones
        if not await self.tiene_permiso_conversaciones():
            await self.close()
            return
        
        user_id = self.scope['user'].id
        self.room_group_name = f'conversaciones_operador_{user_id}'
        
        # Unirse al grupo específico del operador
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        # Salir del grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def nueva_alerta_conversacion(self, event):
        # Notificar nueva alerta de conversación
        await self.send(text_data=json.dumps({
            'type': 'nueva_alerta_conversacion',
            'alerta': event['alerta']
        }))
    
    @database_sync_to_async
    def tiene_permiso_conversaciones(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return False
        
        return (user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists() 
                or user.is_superuser)