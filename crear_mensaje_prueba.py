#!/usr/bin/env python3
"""
Script simple para crear un mensaje de prueba
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from conversaciones.models import Conversacion, Mensaje
from django.contrib.auth.models import User

def main():
    print("🔍 Buscando conversación activa con operador asignado...")
    
    # Buscar una conversación activa con operador
    conversacion = Conversacion.objects.filter(
        estado='activa',
        operador_asignado__isnull=False
    ).first()
    
    if not conversacion:
        print("❌ No se encontró ninguna conversación activa con operador asignado")
        print("💡 Crea una conversación y asígnala a un operador primero")
        return
    
    print(f"✅ Encontrada conversación #{conversacion.id}")
    print(f"   - Operador: {conversacion.operador_asignado.username}")
    print(f"   - Estado: {conversacion.estado}")
    
    # Crear mensaje del ciudadano
    mensaje = Mensaje.objects.create(
        conversacion=conversacion,
        remitente='ciudadano',
        contenido='¡Hola! Este es un mensaje de prueba para generar alerta.',
        leido=False  # Importante: marcar como no leído
    )
    
    print(f"✅ Mensaje creado: ID {mensaje.id}")
    print(f"   - Contenido: {mensaje.contenido}")
    print(f"   - Fecha: {mensaje.fecha_envio}")
    print(f"   - Leído: {mensaje.leido}")
    
    # Verificar que el operador tenga el grupo correcto
    operador = conversacion.operador_asignado
    grupos = list(operador.groups.values_list('name', flat=True))
    print(f"   - Grupos del operador: {grupos}")
    
    if 'Conversaciones' in grupos or 'OperadorCharla' in grupos:
        print("✅ El operador tiene permisos correctos")
    else:
        print("⚠️  El operador NO tiene grupo 'Conversaciones' o 'OperadorCharla'")
    
    print("\n🎯 Para ver la alerta:")
    print("   1. Inicia sesión como:", operador.username)
    print("   2. Ve a cualquier página del sistema")
    print("   3. Deberías ver el contador en el icono de campana")
    print("   4. Haz clic en la campana para ver el mensaje")

if __name__ == '__main__':
    main()