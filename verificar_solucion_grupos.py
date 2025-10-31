#!/usr/bin/env python
"""
Script para verificar que la solución de asignación de grupos funciona correctamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group
from users.forms import UserCreationForm

def test_creacion_usuario_con_grupos():
    """Prueba la creación de un usuario con grupos usando el formulario"""
    print("=== PRUEBA DE CREACIÓN DE USUARIO CON GRUPOS ===\n")
    
    # Eliminar usuario de prueba si existe
    if User.objects.filter(username='test_solucion').exists():
        User.objects.filter(username='test_solucion').delete()
        print("Usuario de prueba anterior eliminado")
    
    # Obtener grupos para asignar
    grupos_test = Group.objects.filter(name__in=['Administrador', 'Usuario Ver'])
    
    # Datos del formulario
    form_data = {
        'username': 'test_solucion',
        'email': 'test_solucion@example.com',
        'password': 'test123456',
        'first_name': 'Test',
        'last_name': 'Solucion',
        'groups': list(grupos_test.values_list('id', flat=True)),
        'es_usuario_provincial': False,
        'rol': 'Usuario de Prueba'
    }
    
    print(f"Creando usuario con grupos: {[g.name for g in grupos_test]}")
    
    # Crear formulario y validar
    form = UserCreationForm(data=form_data)
    
    if form.is_valid():
        # Guardar usuario
        usuario = form.save()
        
        # Verificar resultado
        grupos_asignados = usuario.groups.all()
        print(f"✅ Usuario creado: {usuario.username}")
        print(f"✅ Grupos asignados: {[g.name for g in grupos_asignados]}")
        
        # Verificar perfil
        try:
            perfil = usuario.profile
            print(f"✅ Perfil creado: Rol={perfil.rol}")
        except:
            print("❌ Error: Perfil no creado")
        
        # Verificar que los grupos coinciden
        if set(grupos_asignados) == set(grupos_test):
            print("✅ ÉXITO: Los grupos se asignaron correctamente")
            return True
        else:
            print("❌ ERROR: Los grupos no coinciden")
            return False
    else:
        print("❌ ERROR: Formulario inválido")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
        return False

def verificar_usuarios_existentes():
    """Verifica el estado actual de todos los usuarios"""
    print("\n=== ESTADO ACTUAL DE USUARIOS ===\n")
    
    usuarios_sin_grupos = []
    usuarios_con_grupos = []
    
    for usuario in User.objects.all():
        grupos = usuario.groups.all()
        if grupos.exists():
            usuarios_con_grupos.append((usuario.username, [g.name for g in grupos]))
        else:
            usuarios_sin_grupos.append(usuario.username)
    
    print(f"Usuarios CON grupos ({len(usuarios_con_grupos)}):")
    for username, grupos in usuarios_con_grupos:
        print(f"  - {username}: {grupos}")
    
    print(f"\nUsuarios SIN grupos ({len(usuarios_sin_grupos)}):")
    for username in usuarios_sin_grupos:
        print(f"  - {username}")
    
    return len(usuarios_sin_grupos) == 0

if __name__ == '__main__':
    try:
        # Verificar estado actual
        todos_tienen_grupos = verificar_usuarios_existentes()
        
        # Probar creación de nuevo usuario
        creacion_exitosa = test_creacion_usuario_con_grupos()
        
        print(f"\n=== RESUMEN ===")
        print(f"Todos los usuarios tienen grupos: {'✅ SÍ' if todos_tienen_grupos else '❌ NO'}")
        print(f"Creación de nuevos usuarios funciona: {'✅ SÍ' if creacion_exitosa else '❌ NO'}")
        
        if todos_tienen_grupos and creacion_exitosa:
            print("🎉 PROBLEMA RESUELTO: La asignación de grupos funciona correctamente")
        else:
            print("⚠️  Aún hay problemas pendientes")
            
    except Exception as e:
        print(f"Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()