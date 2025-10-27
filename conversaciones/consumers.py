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
            
            mensaje = Mensaje.objects.create(
                conversacion=conversacion,
                remitente='operador',
                contenido=contenido
            )
            return mensaje
        except:
            return None


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
            'conversacion': event['conversacion']
        }))
    
    async def nuevo_mensaje(self, event):
        # Notificar nuevo mensaje
        await self.send(text_data=json.dumps({
            'type': 'nuevo_mensaje',
            'conversacion_id': event['conversacion_id'],
            'mensaje': event['mensaje']
        }))
    
    @database_sync_to_async
    def tiene_permiso(self):
        user = self.scope['user']
        if not user.is_authenticated:
            return False
        
        return (user.groups.filter(name__in=['Conversaciones', 'OperadorCharla']).exists() 
                or user.is_superuser)