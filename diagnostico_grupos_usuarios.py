#!/usr/bin/env python
"""
Script de diagnóstico para verificar la asignación de grupos a usuarios
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from users.models import Profile

def diagnosticar_usuarios_grupos():
    """Diagnostica el estado actual de usuarios y grupos"""
    print("=== DIAGNÓSTICO DE USUARIOS Y GRUPOS ===\n")
    
    # Verificar grupos existentes
    grupos = Group.objects.all()
    print(f"Grupos disponibles ({grupos.count()}):")
    for grupo in grupos:
        print(f"  - {grupo.name} (ID: {grupo.id})")
    print()
    
    # Verificar usuarios y sus grupos
    usuarios = User.objects.all()
    print(f"Usuarios registrados ({usuarios.count()}):")
    for usuario in usuarios:
        grupos_usuario = usuario.groups.all()
        print(f"  - {usuario.username}:")
        print(f"    Email: {usuario.email}")
        print(f"    Grupos: {[g.name for g in grupos_usuario] if grupos_usuario else 'Sin grupos'}")
        
        # Verificar perfil
        try:
            perfil = usuario.profile
            print(f"    Perfil: Rol={perfil.rol}, Provincial={perfil.es_usuario_provincial}")
        except Profile.DoesNotExist:
            print(f"    Perfil: No existe")
        print()

def crear_usuario_test():
    """Crea un usuario de prueba para verificar la asignación de grupos"""
    print("=== CREANDO USUARIO DE PRUEBA ===\n")
    
    # Verificar si ya existe
    if User.objects.filter(username='test_grupos').exists():
        print("Usuario test_grupos ya existe. Eliminando...")
        User.objects.filter(username='test_grupos').delete()
    
    # Crear usuario
    usuario = User.objects.create_user(
        username='test_grupos',
        email='test@example.com',
        password='test123',
        first_name='Test',
        last_name='Usuario'
    )
    
    # Obtener grupos para asignar
    grupos_disponibles = Group.objects.all()[:2]  # Tomar los primeros 2 grupos
    
    if grupos_disponibles:
        print(f"Asignando grupos: {[g.name for g in grupos_disponibles]}")
        usuario.groups.set(grupos_disponibles)
        
        # Verificar asignación
        grupos_asignados = usuario.groups.all()
        print(f"Grupos asignados: {[g.name for g in grupos_asignados]}")
        
        if grupos_asignados.count() == grupos_disponibles.count():
            print("✅ Asignación de grupos EXITOSA")
        else:
            print("❌ Error en la asignación de grupos")
    else:
        print("No hay grupos disponibles para asignar")
    
    # Crear perfil
    Profile.objects.create(
        user=usuario,
        rol='Test',
        es_usuario_provincial=False
    )
    
    print(f"Usuario de prueba creado: {usuario.username}")

def verificar_formulario():
    """Simula el proceso del formulario"""
    print("=== SIMULANDO PROCESO DEL FORMULARIO ===\n")
    
    from users.forms import UserCreationForm
    
    # Datos de prueba
    form_data = {
        'username': 'test_form',
        'email': 'testform@example.com',
        'password': 'test123',
        'first_name': 'Test',
        'last_name': 'Form',
        'groups': list(Group.objects.all()[:1].values_list('id', flat=True)),  # Primer grupo
        'es_usuario_provincial': False,
        'rol': 'Test Form'
    }
    
    print(f"Datos del formulario: {form_data}")
    
    # Crear formulario
    form = UserCreationForm(data=form_data)
    
    if form.is_valid():
        print("✅ Formulario válido")
        
        # Eliminar usuario si existe
        if User.objects.filter(username='test_form').exists():
            User.objects.filter(username='test_form').delete()
        
        # Guardar usuario
        usuario = form.save()
        
        # Verificar resultado
        grupos_asignados = usuario.groups.all()
        print(f"Usuario creado: {usuario.username}")
        print(f"Grupos asignados: {[g.name for g in grupos_asignados]}")
        
        if grupos_asignados.count() > 0:
            print("✅ Formulario asigna grupos correctamente")
        else:
            print("❌ Error: Formulario NO asigna grupos")
            
    else:
        print("❌ Formulario inválido:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")

if __name__ == '__main__':
    try:
        diagnosticar_usuarios_grupos()
        crear_usuario_test()
        verificar_formulario()
        
    except Exception as e:
        print(f"Error durante el diagnóstico: {e}")
        import traceback
        traceback.print_exc()