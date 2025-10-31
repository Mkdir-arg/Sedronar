#!/usr/bin/env python3
"""
Script de prueba para el sistema de alertas de conversaciones
"""

import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from conversaciones.models import Conversacion, Mensaje
from conversaciones.signals_alertas import _generar_alerta_mensaje_ciudadano


def crear_datos_prueba():
    """Crear datos de prueba para conversaciones"""
    print("🔧 Creando datos de prueba...")
    
    # Crear grupo Conversaciones si no existe
    grupo_conv, created = Group.objects.get_or_create(name='Conversaciones')
    if created:
        print("✅ Grupo 'Conversaciones' creado")
    
    # Crear usuario operador si no existe
    operador, created = User.objects.get_or_create(
        username='operador_test',
        defaults={
            'first_name': 'Operador',
            'last_name': 'Test',
            'email': 'operador@test.com'
        }
    )
    if created:
        operador.set_password('test123')
        operador.save()
        print("✅ Usuario operador creado")
    
    # Asignar al grupo
    operador.groups.add(grupo_conv)
    
    # Crear conversación de prueba
    conversacion, created = Conversacion.objects.get_or_create(
        id=999,
        defaults={
            'tipo': 'anonima',
            'estado': 'activa',
            'operador_asignado': operador
        }
    )
    if created:
        print("✅ Conversación de prueba creada")
    
    return operador, conversacion


def simular_mensaje_ciudadano(conversacion):
    """Simular un mensaje de ciudadano"""
    print("📨 Simulando mensaje de ciudadano...")
    
    mensaje = Mensaje.objects.create(
        conversacion=conversacion,
        remitente='ciudadano',
        contenido='Hola, necesito ayuda urgente por favor'
    )
    
    print(f"✅ Mensaje creado: {mensaje.contenido}")
    
    # Simular la señal manualmente
    try:
        _generar_alerta_mensaje_ciudadano(conversacion, mensaje)
        print("✅ Alerta generada correctamente")
    except Exception as e:
        print(f"❌ Error generando alerta: {e}")
    
    return mensaje


def verificar_configuracion():
    """Verificar que la configuración esté correcta"""
    print("🔍 Verificando configuración...")
    
    # Verificar que el context processor esté configurado
    from django.conf import settings
    context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
    
    if 'conversaciones.context_processors.user_groups' in context_processors:
        print("✅ Context processor configurado")
    else:
        print("❌ Context processor NO configurado")
    
    # Verificar archivos JavaScript
    import os
    js_files = [
        'static/custom/js/alertas_conversaciones.js',
        'static/custom/js/notification_sound.js'
    ]
    
    for js_file in js_files:
        if os.path.exists(js_file):
            print(f"✅ {js_file} existe")
        else:
            print(f"❌ {js_file} NO existe")


def main():
    """Función principal de prueba"""
    print("🚀 Iniciando prueba del sistema de alertas de conversaciones")
    print("=" * 60)
    
    # Verificar configuración
    verificar_configuracion()
    print()
    
    # Crear datos de prueba
    operador, conversacion = crear_datos_prueba()
    print()
    
    # Simular mensaje
    mensaje = simular_mensaje_ciudadano(conversacion)
    print()
    
    print("📋 Resumen de la prueba:")
    print(f"   - Operador: {operador.username} ({operador.get_full_name()})")
    print(f"   - Conversación ID: {conversacion.id}")
    print(f"   - Mensaje ID: {mensaje.id}")
    print(f"   - Estado conversación: {conversacion.estado}")
    print()
    
    print("🎯 Para probar completamente:")
    print("   1. Inicia el servidor: python manage.py runserver")
    print("   2. Inicia sesión como 'operador_test' (password: test123)")
    print("   3. Ve a cualquier página del sistema")
    print("   4. Ejecuta este script nuevamente para generar alertas")
    print("   5. Deberías ver la alerta en el icono de campana")
    print()
    
    print("✅ Prueba completada")


if __name__ == '__main__':
    main()