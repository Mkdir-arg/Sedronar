"""
Script para limpiar usuarios duplicados de instituciones
Elimina usuarios con formato 'institucion_{id}' si existe otro usuario asociado a la misma institución
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Institucion

def limpiar_usuarios_duplicados():
    instituciones = Institucion.objects.prefetch_related('encargados').all()
    
    for institucion in instituciones:
        encargados = list(institucion.encargados.all())
        
        if len(encargados) > 1:
            print(f"\n🔍 Institución: {institucion.nombre} (ID: {institucion.id})")
            print(f"   Tiene {len(encargados)} usuarios asociados:")
            
            usuario_sistema = None
            usuario_real = None
            
            for user in encargados:
                print(f"   - {user.username} (Email: {user.email}, Activo: {user.is_active})")
                
                if user.username.startswith('institucion_'):
                    usuario_sistema = user
                else:
                    usuario_real = user
            
            # Si hay ambos tipos de usuarios, eliminar el del sistema y activar el real
            if usuario_sistema and usuario_real:
                print(f"\n   ✅ Acción: Eliminar '{usuario_sistema.username}' y activar '{usuario_real.username}'")
                
                # Activar usuario real
                if not usuario_real.is_active:
                    usuario_real.is_active = True
                    usuario_real.save()
                    print(f"   ✓ Usuario '{usuario_real.username}' activado")
                
                # Eliminar usuario del sistema
                institucion.encargados.remove(usuario_sistema)
                usuario_sistema.delete()
                print(f"   ✓ Usuario '{usuario_sistema.username}' eliminado")

if __name__ == '__main__':
    print("=" * 60)
    print("LIMPIEZA DE USUARIOS DUPLICADOS DE INSTITUCIONES")
    print("=" * 60)
    
    limpiar_usuarios_duplicados()
    
    print("\n" + "=" * 60)
    print("✅ Proceso completado")
    print("=" * 60)
