#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from conversaciones.models import Conversacion

def main():
    # Crear nueva conversación pendiente
    conversacion = Conversacion.objects.create(
        tipo='anonima',
        estado='pendiente',
        prioridad='normal'
    )
    
    print(f"✅ Nueva conversación creada: #{conversacion.id}")
    print(f"   - Estado: {conversacion.estado}")
    print(f"   - Fecha: {conversacion.fecha_inicio}")
    print("🔔 Debería notificar a todos los operadores de Conversaciones")

if __name__ == '__main__':
    main()