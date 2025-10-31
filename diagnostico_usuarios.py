#!/usr/bin/env python
"""
Script de diagnóstico para verificar usuarios y grupos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from users.models import Profile

def diagnosticar_usuarios():
    print("=== DIAGNÓSTICO DE USUARIOS Y GRUPOS ===\n")
    
    # Listar todos los usuarios
    usuarios = User.objects.all()
    print(f"Total de usuarios: {usuarios.count()}")
    
    for usuario in usuarios:
        print(f"\n--- Usuario: {usuario.username} ---")
        print(f"Email: {usuario.email}")
        print(f"Nombre completo: {usuario.first_name} {usuario.last_name}")
        print(f"Activo: {usuario.is_active}")
        print(f"Staff: {usuario.is_staff}")
        print(f"Superuser: {usuario.is_superuser}")
        
        # Grupos del usuario
        grupos = usuario.groups.all()
        if grupos:
            print(f"Grupos: {', '.join([g.name for g in grupos])}")
        else:
            print("Grupos: Ninguno")
        
        # Perfil del usuario
        try:
            perfil = usuario.profile
            print(f"Usuario provincial: {perfil.es_usuario_provincial}")
            print(f"Provincia: {perfil.provincia}")
            print(f"Rol: {perfil.rol}")
        except Profile.DoesNotExist:
            print("Perfil: No existe")
    
    # Listar todos los grupos
    print(f"\n=== GRUPOS DISPONIBLES ===")
    grupos = Group.objects.all()
    print(f"Total de grupos: {grupos.count()}")
    
    for grupo in grupos:
        usuarios_en_grupo = grupo.user_set.count()
        print(f"- {grupo.name} ({usuarios_en_grupo} usuarios)")
    
    # Verificar usuarios sin grupos
    usuarios_sin_grupos = User.objects.filter(groups__isnull=True)
    if usuarios_sin_grupos:
        print(f"\n=== USUARIOS SIN GRUPOS ({usuarios_sin_grupos.count()}) ===")
        for usuario in usuarios_sin_grupos:
            print(f"- {usuario.username}")
    
    # Verificar usuarios sin perfil
    usuarios_sin_perfil = User.objects.filter(profile__isnull=True)
    if usuarios_sin_perfil:
        print(f"\n=== USUARIOS SIN PERFIL ({usuarios_sin_perfil.count()}) ===")
        for usuario in usuarios_sin_perfil:
            print(f"- {usuario.username}")

def reparar_usuarios():
    print("\n=== REPARANDO USUARIOS ===")
    
    # Crear perfiles faltantes
    usuarios_sin_perfil = User.objects.filter(profile__isnull=True)
    for usuario in usuarios_sin_perfil:
        Profile.objects.create(user=usuario)
        print(f"Perfil creado para: {usuario.username}")
    
    print("Reparación completada.")

if __name__ == "__main__":
    diagnosticar_usuarios()
    
    respuesta = input("\n¿Desea reparar usuarios sin perfil? (s/n): ")
    if respuesta.lower() == 's':
        reparar_usuarios()