#!/usr/bin/env python
"""
Script de prueba para verificar las actualizaciones en tiempo real
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from conversaciones.models import Conversacion, Mensaje
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def test_websocket_notification():
    """Prueba las notificaciones WebSocket"""
    try:
        channel_layer = get_channel_layer()
        
        # Enviar notificación de prueba
        async_to_sync(channel_layer.group_send)(
            'conversaciones_list',
            {
                'type': 'actualizar_lista',
                'mensaje': 'Prueba de notificación en tiempo real'
            }
        )
        
        print("✅ Notificación WebSocket enviada correctamente")
        return True
    except Exception as e:
        print(f"❌ Error enviando notificación WebSocket: {e}")
        return False

def test_api_estadisticas():
    """Prueba la API de estadísticas"""
    try:
        from conversaciones.views import api_estadisticas_tiempo_real
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        
        factory = RequestFactory()
        request = factory.get('/conversaciones/api/estadisticas/')
        
        # Crear usuario de prueba con permisos
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("❌ No hay usuarios superuser para la prueba")
            return False
        
        request.user = user
        
        response = api_estadisticas_tiempo_real(request)
        
        if response.status_code == 200:
            print("✅ API de estadísticas funciona correctamente")
            return True
        else:
            print(f"❌ API de estadísticas falló con código: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando API de estadísticas: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🚀 Iniciando pruebas de tiempo real...")
    print("=" * 50)
    
    # Verificar configuración de Channels
    if hasattr(settings, 'CHANNEL_LAYERS'):
        print("✅ Django Channels configurado")
    else:
        print("❌ Django Channels no configurado")
        return
    
    # Verificar ASGI
    if hasattr(settings, 'ASGI_APPLICATION'):
        print("✅ ASGI Application configurada")
    else:
        print("❌ ASGI Application no configurada")
        return
    
    print("\n📊 Probando funcionalidades...")
    print("-" * 30)
    
    # Probar WebSocket
    test_websocket_notification()
    
    # Probar API
    test_api_estadisticas()
    
    print("\n📋 Estadísticas actuales:")
    print("-" * 30)
    
    # Mostrar estadísticas actuales
    chats_no_atendidos = Conversacion.objects.filter(operador_asignado=None, estado='activa').count()
    total_conversaciones = Conversacion.objects.count()
    
    print(f"Total de conversaciones: {total_conversaciones}")
    print(f"Chats no atendidos: {chats_no_atendidos}")
    
    print("\n✅ Pruebas completadas!")
    print("\n📝 Para usar las actualizaciones en tiempo real:")
    print("1. Asegúrate de que el servidor esté corriendo con ASGI")
    print("2. Abre la página de conversaciones en el navegador")
    print("3. Los contadores se actualizarán automáticamente")
    print("4. Las notificaciones aparecerán cuando haya cambios")

if __name__ == '__main__':
    main()