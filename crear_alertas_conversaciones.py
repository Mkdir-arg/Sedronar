#!/usr/bin/env python3
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from conversaciones.models import Conversacion, HistorialAlertaConversacion
from django.contrib.auth.models import User

def main():
    # Buscar usuario con rol Conversaciones
    usuario = User.objects.filter(
        groups__name__in=['Conversaciones', 'OperadorCharla']
    ).first()
    
    if not usuario:
        print("❌ No hay usuarios con rol Conversaciones")
        return
    
    # Crear conversación si no existe
    conversacion, created = Conversacion.objects.get_or_create(
        id=100,
        defaults={
            'tipo': 'anonima',
            'estado': 'pendiente'
        }
    )
    
    # Crear alertas de prueba
    alertas = [
        {
            'tipo': 'NUEVA_CONVERSACION',
            'mensaje': 'Nueva conversación #100 disponible'
        },
        {
            'tipo': 'NUEVO_MENSAJE', 
            'mensaje': 'Nuevo mensaje en conversación #100'
        },
        {
            'tipo': 'RIESGO_CRITICO',
            'mensaje': 'RIESGO CRÍTICO: Palabras de riesgo detectadas'
        }
    ]
    
    for alerta_data in alertas:
        HistorialAlertaConversacion.objects.get_or_create(
            conversacion=conversacion,
            operador=usuario,
            tipo=alerta_data['tipo'],
            defaults={
                'mensaje': alerta_data['mensaje'],
                'vista': False
            }
        )
    
    print(f"✅ Alertas creadas para usuario: {usuario.username}")
    print(f"   - Conversación: #{conversacion.id}")
    print(f"   - Total alertas: {HistorialAlertaConversacion.objects.filter(operador=usuario).count()}")

if __name__ == '__main__':
    main()