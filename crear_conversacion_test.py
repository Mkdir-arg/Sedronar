#!/usr/bin/env python
"""
Script para crear una conversación de prueba y verificar actualizaciones en tiempo real
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from conversaciones.models import Conversacion, Mensaje

def crear_conversacion_prueba():
    """Crea una conversación de prueba"""
    try:
        conversacion = Conversacion.objects.create(
            tipo='anonima',
            prioridad='normal',
            estado='activa'
        )
        
        # Crear mensaje inicial
        mensaje = Mensaje.objects.create(
            conversacion=conversacion,
            remitente='ciudadano',
            contenido='Hola, necesito ayuda con información sobre drogas'
        )
        
        print(f"✅ Conversación creada: #{conversacion.id}")
        print(f"✅ Mensaje creado: {mensaje.contenido}")
        print(f"\n🔍 Ahora verifica en http://localhost:9000/conversaciones/")
        print(f"📊 El contador debería actualizarse automáticamente en 3 segundos")
        
        return conversacion
        
    except Exception as e:
        print(f"❌ Error creando conversación: {e}")
        return None

if __name__ == '__main__':
    print("🚀 Creando conversación de prueba...")
    crear_conversacion_prueba()