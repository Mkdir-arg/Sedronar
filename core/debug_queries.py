# pylint: skip-file
# ARCHIVO TEMPORALMENTE DESHABILITADO - REFERENCIAS A MÓDULO CIUDADANOS ELIMINADO
# TODO: Actualizar para usar legajos.models cuando sea necesario

#!/usr/bin/env python3

import logging
import os
import sys

import django
from django.contrib.auth.models import User
from django.db import connection, reset_queries
from django.test import RequestFactory

# from legajos.models import Ciudadano
# from legajos.views import CiudadanoDetailView


if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("django")

# Configurar Django (solo si se ejecuta directamente)
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    django.setup()


def debug_ciudadano_detail_queries():
    """Función temporalmente deshabilitada"""
    logger.info("⚠️ debug_queries.py temporalmente deshabilitado")
    return False


def show_query_analysis():
    """Función temporalmente deshabilitada"""
    logger.info("⚠️ debug_queries.py temporalmente deshabilitado")


def debug_view_queries(view_class, url_pattern, model_class, view_name, pk=None, pk_kwarg="pk"):
    """Función temporalmente deshabilitada"""
    logger.info("⚠️ debug_queries.py temporalmente deshabilitado")
    return False, 0


def debug_all_views():
    """Función temporalmente deshabilitada"""
    logger.info("⚠️ debug_queries.py temporalmente deshabilitado")
    return {}


if __name__ == "__main__":
    logger.info("⚠️ debug_queries.py temporalmente deshabilitado")
    sys.exit(0)