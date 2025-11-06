import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Institucion

print("=== INSTITUCIONES EN LA BASE DE DATOS ===\n")
instituciones = Institucion.objects.all()
print(f"Total instituciones: {instituciones.count()}\n")

for inst in instituciones:
    print(f"ID: {inst.id}")
    print(f"Nombre: {inst.nombre}")
    print(f"CUIT: {inst.cuit}")
    print(f"Estado registro: {inst.estado_registro}")
    print(f"Activo: {inst.activo}")
    print("-" * 50)
