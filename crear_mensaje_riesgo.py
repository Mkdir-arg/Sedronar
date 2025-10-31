#!/usr/bin/env python3
"""
Script para crear mensaje con palabras de riesgo
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from conversaciones.models import Conversacion, Mensaje
from django.contrib.auth.models import User

def main():
    conversacion = Conversacion.objects.filter(
        estado='activa',
        operador_asignado__isnull=False
    ).first()
    
    if not conversacion:
        print("❌ No hay conversaciones activas")
        return
    
    # Crear mensaje con palabra de riesgo
    mensaje = Mensaje.objects.create(
        conversacion=conversacion,
        remitente='ciudadano',
        contenido='Estoy muy mal, no puedo más, estoy pensando en suicidio',
        leido=False
    )
    
    print(f"✅ Mensaje de RIESGO creado: {mensaje.contenido}")
    print(f"   - Conversación: #{conversacion.id}")
    print(f"   - Operador: {conversacion.operador_asignado.username}")
    print("🚨 Debería generar ALERTA CRÍTICA")

if __name__ == '__main__':
    main()