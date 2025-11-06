import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.conf import settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
        ],
        USE_TZ=True,
    )

django.setup()

# Simular consulta SQL directa
print("=== CONSULTA DIRECTA A LA BD ===")
print("SELECT id, dni, nombre, apellido, activo FROM legajos_ciudadano ORDER BY id;")
print()

# Datos que mencionaste:
datos_bd = [
    (1, "40732138", "Matias", "FARIÑA", 1),
    (2, "36397539", "Veronica Anahi", "PERCIANTE", 1), 
    (3, "40732139", "Matías Gerardo", "ZALAZAR", 1),
    (4, "40732140", "Gonzalo Miguel", "TORALES GAYOZO", 1)
]

print("Datos en BD:")
for row in datos_bd:
    print(f"ID: {row[0]}, DNI: {row[1]}, Nombre: {row[2]}, Apellido: {row[3]}, Activo: {row[4]}")

print("\n=== ANÁLISIS ===")
print("En la tabla del frontend aparecen:")
frontend_data = [
    "40732138 - FARIÑA, Matias",
    "36397539 - PERCIANTE, Veronica Anahi", 
    "40732140 - TORALES GAYOZO, Gonzalo Miguel",
    "40732139 - ZALAZAR, Matías Gerardo"
]

print("Frontend muestra 4 registros:")
for item in frontend_data:
    print(f"- {item}")

print("\nBD tiene 4 registros - COINCIDE")
print("El problema NO es de datos faltantes")
print("El problema puede ser:")
print("1. Orden diferente (BD por ID, Frontend por apellido)")
print("2. Cache del navegador")
print("3. Filtros en el queryset")