#!/usr/bin/env python
"""
Script para probar las alertas de eventos críticos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from legajos.models import EventoCritico, AlertaEventoCritico, LegajoAtencion

def test_alertas():
    print("=== TEST DE ALERTAS DE EVENTOS CRÍTICOS ===\n")
    
    # Obtener todos los usuarios responsables
    responsables = User.objects.filter(groups__name='Responsable')
    print(f"Usuarios con rol 'Responsable': {responsables.count()}")
    for resp in responsables:
        print(f"  - {resp.username} ({resp.get_full_name()})")
    
    print()
    
    # Obtener todos los eventos críticos
    eventos = EventoCritico.objects.all().order_by('-creado')
    print(f"Total de eventos críticos: {eventos.count()}")
    
    for evento in eventos[:5]:  # Mostrar solo los últimos 5
        print(f"  - {evento.get_tipo_display()} - Legajo: {evento.legajo.codigo}")
        print(f"    Responsable: {evento.legajo.responsable}")
        print(f"    Fecha: {evento.creado}")
        
        # Verificar si ya fue visto
        alerta_vista = AlertaEventoCritico.objects.filter(
            evento=evento,
            responsable=evento.legajo.responsable
        ).exists()
        print(f"    ¿Ya visto?: {'Sí' if alerta_vista else 'No'}")
        print()
    
    print("\n=== EVENTOS PENDIENTES POR RESPONSABLE ===")
    
    for responsable in responsables:
        eventos_pendientes = EventoCritico.objects.filter(
            legajo__responsable=responsable
        ).exclude(
            alertas_vistas__responsable=responsable
        ).count()
        
        print(f"{responsable.username}: {eventos_pendientes} eventos pendientes")
    
    print("\n=== LEGAJOS CON RESPONSABLE ===")
    legajos_con_responsable = LegajoAtencion.objects.filter(responsable__isnull=False).count()
    total_legajos = LegajoAtencion.objects.count()
    print(f"Legajos con responsable: {legajos_con_responsable}/{total_legajos}")

if __name__ == "__main__":
    test_alertas()