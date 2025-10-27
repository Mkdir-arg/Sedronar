#!/usr/bin/env python
"""
Script para configurar el sistema de conversaciones
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from conversaciones.models import Conversacion, Mensaje


def crear_grupo_conversaciones():
    """Crear grupo Conversaciones con permisos"""
    print("Configurando grupo Conversaciones...")
    
    # Crear grupo
    grupo, created = Group.objects.get_or_create(name='Conversaciones')
    
    if created:
        print("✓ Grupo 'Conversaciones' creado")
    else:
        print("✓ Grupo 'Conversaciones' ya existe")
    
    # Obtener content types
    try:
        conversacion_ct = ContentType.objects.get_for_model(Conversacion)
        mensaje_ct = ContentType.objects.get_for_model(Mensaje)
        
        # Permisos necesarios
        permisos_codenames = [
            'view_conversacion',
            'change_conversacion', 
            'view_mensaje',
            'add_mensaje',
        ]
        
        permisos_asignados = 0
        for codename in permisos_codenames:
            try:
                if codename.endswith('conversacion'):
                    permiso = Permission.objects.get(
                        content_type=conversacion_ct,
                        codename=codename
                    )
                else:
                    permiso = Permission.objects.get(
                        content_type=mensaje_ct,
                        codename=codename
                    )
                grupo.permissions.add(permiso)
                permisos_asignados += 1
            except Permission.DoesNotExist:
                print(f"⚠ Permiso no encontrado: {codename}")
        
        print(f"✓ {permisos_asignados} permisos asignados al grupo")
        
    except Exception as e:
        print(f"⚠ Error configurando permisos: {e}")
        print("Los permisos se configurarán automáticamente después de ejecutar las migraciones")


def main():
    print("=== Configuración del Sistema de Conversaciones ===\n")
    
    crear_grupo_conversaciones()
    
    print("\n=== Configuración completada ===")
    print("\nPróximos pasos:")
    print("1. Ejecutar: docker compose exec django python manage.py migrate")
    print("2. Ejecutar: docker compose exec django python manage.py setup_conversaciones")
    print("3. Asignar usuarios al grupo 'Conversaciones' desde el admin")
    print("4. Acceder a /conversaciones/chat/ para probar el chat ciudadano")


if __name__ == '__main__':
    main()