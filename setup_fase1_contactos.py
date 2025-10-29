#!/usr/bin/env python
"""
Script para configurar la Fase 1 del sistema de contactos
Ejecutar después de aplicar las migraciones
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth.models import Group, User
from legajos.models_contactos import RolProfesional

def main():
    print("=== CONFIGURACIÓN FASE 1: SISTEMA DE CONTACTOS ===\n")
    
    # 1. Cargar fixtures iniciales
    print("1. Cargando grupos de usuarios...")
    try:
        call_command('loaddata', 'legajos/fixtures/contactos_initial_data.json')
        print("✓ Grupos cargados correctamente")
    except Exception as e:
        print(f"⚠ Error cargando fixtures: {e}")
    
    # 2. Configurar roles y permisos
    print("\n2. Configurando roles y permisos...")
    try:
        call_command('setup_roles_contactos')
        print("✓ Roles y permisos configurados")
    except Exception as e:
        print(f"⚠ Error configurando roles: {e}")
    
    # 3. Verificar grupos creados
    print("\n3. Verificando grupos creados:")
    grupos = Group.objects.filter(name__in=[
        'Psicologo', 'Psiquiatra', 'Medico', 'Trabajador Social',
        'Operador Socioterapeutico', 'Coordinador', 'Director',
        'Enfermero', 'Terapista Ocupacional', 'Abogado'
    ])
    
    for grupo in grupos:
        permisos_count = grupo.permissions.count()
        print(f"  - {grupo.name}: {permisos_count} permisos")
    
    # 4. Mostrar próximos pasos
    print("\n=== FASE 1 COMPLETADA ===")
    print("\nPróximos pasos:")
    print("1. Verificar que las migraciones se aplicaron correctamente")
    print("2. Probar el admin de Django con los nuevos modelos")
    print("3. Asignar usuarios a los grupos correspondientes")
    print("4. Continuar con la Fase 2: APIs y Serializers")
    
    print(f"\nModelos disponibles en admin:")
    print("- Historial de Contactos")
    print("- Vínculos Familiares") 
    print("- Profesionales Tratantes")
    print("- Dispositivos Vinculados")
    print("- Contactos de Emergencia")

if __name__ == '__main__':
    main()