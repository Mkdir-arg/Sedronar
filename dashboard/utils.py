"""Utilidades básicas de dashboard."""

import logging
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from django.contrib.auth.models import User
from legajos.models import Ciudadano

logger = logging.getLogger(__name__)

def table_exists(table_name):
    """Check if a DB table exists without exploding when DB is unavailable."""
    try:
        vendor = connection.vendor
    except ImproperlyConfigured:
        logger.debug("Base de datos no configurada; omitiendo chequeo de %s", table_name)
        return False

    try:
        if vendor == "mysql":
            with connection.cursor() as cursor:
                cursor.execute("SHOW TABLES LIKE %s", [table_name])
                return cursor.fetchone() is not None
        return table_name in connection.introspection.table_names()
    except (OperationalError, ProgrammingError, AttributeError) as error:
        logger.debug("No se pudo comprobar la existencia de %s (%s); se asume ausente", table_name, error)
        return False

CACHE_TIMEOUT = getattr(settings, "DASHBOARD_CACHE_TIMEOUT", 300)

def contar_usuarios():
    """Contar la cantidad total de usuarios."""
    cache_key = "contar_usuarios"
    cached_value = cache.get(cache_key)
    if cached_value is None:
        cached_value = User.objects.count()
        cache.set(cache_key, cached_value, timeout=CACHE_TIMEOUT)
    return cached_value

def contar_ciudadanos():
    """Contar la cantidad total de ciudadanos."""
    cache_key = "contar_ciudadanos"
    cached_value = cache.get(cache_key)
    if cached_value is None:
        cached_value = Ciudadano.objects.count()
        cache.set(cache_key, cached_value, timeout=CACHE_TIMEOUT)
    return cached_value