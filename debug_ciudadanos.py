#!/usr/bin/env python
"""
Script de debug para verificar ciudadanos en la base de datos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from legajos.models import Ciudadano
from django.db.models import Q

def debug_ciudadanos():
    print("=== DEBUG CIUDADANOS ===")
    
    # Contar todos los ciudadanos
    total_ciudadanos = Ciudadano.objects.count()
    print(f"Total ciudadanos en BD: {total_ciudadanos}")
    
    # Contar ciudadanos activos
    ciudadanos_activos = Ciudadano.objects.filter(activo=True).count()
    print(f"Ciudadanos activos: {ciudadanos_activos}")
    
    # Contar ciudadanos excluidos (instituciones)
    ciudadanos_excluidos = Ciudadano.objects.filter(
        Q(dni='00000000') |
        Q(apellido__icontains='Institución') |
        Q(nombre__icontains='Institución')
    ).count()
    print(f"Ciudadanos excluidos (instituciones): {ciudadanos_excluidos}")
    
    # Ciudadanos que deberían aparecer en la lista
    ciudadanos_visibles = Ciudadano.objects.filter(
        activo=True
    ).exclude(
        Q(dni='00000000') |
        Q(apellido__icontains='Institución') |
        Q(nombre__icontains='Institución')
    ).count()
    print(f"Ciudadanos que deberían aparecer en lista: {ciudadanos_visibles}")
    
    # Mostrar últimos 5 ciudadanos creados
    print("\n=== ÚLTIMOS 5 CIUDADANOS CREADOS ===")
    ultimos_ciudadanos = Ciudadano.objects.order_by('-creado')[:5]
    for ciudadano in ultimos_ciudadanos:
        print(f"ID: {ciudadano.id}, DNI: {ciudadano.dni}, Nombre: {ciudadano.nombre} {ciudadano.apellido}, Activo: {ciudadano.activo}, Creado: {ciudadano.creado}")
    
    # Verificar cache
    print("\n=== VERIFICAR CACHE ===")
    from django.core.cache import cache
    try:
        cache_keys = cache.keys('*ciudadanos*')
        print(f"Claves de cache relacionadas con ciudadanos: {cache_keys}")
    except:
        print("No se pudieron obtener las claves de cache")
    
    # Limpiar cache
    print("Limpiando cache...")
    cache.clear()
    print("Cache limpiado")

if __name__ == '__main__':
    debug_ciudadanos()