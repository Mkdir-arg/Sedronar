from .settings import *
import os

# Configuración para 1000+ usuarios concurrentes
DEBUG = False
ALLOWED_HOSTS = ['*']  # Configurar dominios específicos en producción

# Base de datos con replicación
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': 'sedronar-mysql-master',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 3600,  # 1 hora
        'CONN_HEALTH_CHECKS': True,
    },
    'replica': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': 'sedronar-mysql-slave',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
        'CONN_MAX_AGE': 3600,
    }
}

# Router para lectura/escritura
DATABASE_ROUTERS = ['config.db_router.DatabaseRouter']

# Cache distribuido
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://sedronar-redis-cluster:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 100},
        },
        'TIMEOUT': 3600,
    }
}

# Configuración de workers
GUNICORN_WORKERS = 8
GUNICORN_WORKER_CLASS = 'gevent'
GUNICORN_WORKER_CONNECTIONS = 1000

# Logging para producción
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.handlers.RotatingFileHandler',
    'filename': '/var/log/sedronar/app.log',
    'maxBytes': 50*1024*1024,  # 50MB
    'backupCount': 5,
    'formatter': 'verbose',
}