#!/usr/bin/env python
"""
Script para probar la creación de usuarios con grupos específicos
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from users.forms import UserCreationForm
from users.models import Profile

def test_crear_usuario_con_grupos():
    """Prueba crear un usuario con grupos específicos usando el formulario"""
    print("=== PRUEBA DE CREACIÓN DE USUARIO CON GRUPOS ===\n")
    
    # Limpiar usuario de prueba si existe
    if User.objects.filter(username='test_grupos_web').exists():
        User.objects.filter(username='test_grupos_web').delete()
        print("Usuario de prueba anterior eliminado")
    
    # Obtener algunos grupos para asignar
    grupos_disponibles = Group.objects.filter(name__in=['Administrador', 'Responsable'])
    print(f"Grupos disponibles para asignar: {[g.name for g in grupos_disponibles]}")
    
    if not grupos_disponibles.exists():
        print("❌ No hay grupos disponibles para la prueba")
        return
    
    # Simular datos del formulario web
    form_data = {
        'username': 'test_grupos_web',
        'email': 'test_web@example.com',
        'password': 'test123456',
        'first_name': 'Test',
        'last_name': 'Web',
        'groups': list(grupos_disponibles.values_list('id', flat=True)),
        'es_usuario_provincial': False,
        'rol': 'Test Web'
    }
    
    print(f"Datos del formulario:")
    for key, value in form_data.items():
        if key == 'groups':
            grupos_nombres = [Group.objects.get(id=gid).name for gid in value]
            print(f"  {key}: {value} ({grupos_nombres})")
        else:
            print(f"  {key}: {value}")
    print()
    
    # Crear y validar formulario
    form = UserCreationForm(data=form_data)
    
    if form.is_valid():
        print("✅ Formulario válido")
        
        # Verificar que los grupos están en cleaned_data
        grupos_cleaned = form.cleaned_data.get('groups', [])
        print(f"Grupos en cleaned_data: {[g.name for g in grupos_cleaned]}")
        
        # Guardar usuario
        print("Guardando usuario...")
        usuario = form.save()
        
        # Verificar resultado inmediatamente
        grupos_asignados = usuario.groups.all()
        print(f"Usuario creado: {usuario.username}")
        print(f"Grupos asignados inmediatamente: {[g.name for g in grupos_asignados]}")
        
        # Verificar perfil
        try:
            perfil = usuario.profile
            print(f"Perfil creado: Rol={perfil.rol}, Provincial={perfil.es_usuario_provincial}")
        except Profile.DoesNotExist:
            print("❌ No se creó el perfil")
        
        # Verificar después de refrescar desde BD
        usuario.refresh_from_db()
        grupos_bd = usuario.groups.all()
        print(f"Grupos después de refresh: {[g.name for g in grupos_bd]}")
        
        if grupos_bd.count() == grupos_disponibles.count():
            print("✅ ÉXITO: Grupos asignados correctamente")
        else:
            print("❌ ERROR: Los grupos no se asignaron correctamente")
            print(f"  Esperados: {grupos_disponibles.count()}")
            print(f"  Asignados: {grupos_bd.count()}")
            
    else:
        print("❌ Formulario inválido:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")

def test_usuario_existente_sin_grupos():
    """Verifica usuarios existentes que no tienen grupos"""
    print("\n=== VERIFICANDO USUARIOS SIN GRUPOS ===\n")
    
    usuarios_sin_grupos = User.objects.filter(groups__isnull=True)
    print(f"Usuarios sin grupos ({usuarios_sin_grupos.count()}):")
    
    for usuario in usuarios_sin_grupos:
        print(f"  - {usuario.username} (Email: {usuario.email})")
        
        # Intentar asignar un grupo manualmente
        grupo_admin = Group.objects.filter(name='Administrador').first()
        if grupo_admin:
            print(f"    Asignando grupo 'Administrador'...")
            usuario.groups.add(grupo_admin)
            
            # Verificar
            if usuario.groups.filter(name='Administrador').exists():
                print(f"    ✅ Grupo asignado correctamente")
            else:
                print(f"    ❌ Error al asignar grupo")

if __name__ == '__main__':
    try:
        test_crear_usuario_con_grupos()
        test_usuario_existente_sin_grupos()
        
    except Exception as e:
        print(f"Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()