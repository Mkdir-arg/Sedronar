import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Configuración mínima
import sys
sys.path.insert(0, 'c:\\Users\\usuar\\Sedronar')

# Configurar Django con settings mínimos
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
            'legajos',
            'core',
        ],
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        },
        USE_TZ=True,
    )

django.setup()

from legajos.models import Ciudadano
from django.core.cache import cache

print("=== TEST CIUDADANOS ===")
print(f"Total ciudadanos: {Ciudadano.objects.count()}")
print("Cache limpiado")
cache.clear()