#!/usr/bin/env python3
"""
Script para iniciar el servidor con optimizaciones
"""
import os
import subprocess
import sys

def start_server():
    """Inicia el servidor con Gunicorn optimizado"""
    print("🚀 Iniciando SEDRONAR con optimizaciones de performance...")
    
    # Configuración optimizada
    cmd = [
        "gunicorn",
        "--config", "gunicorn.conf.py",
        "--bind", "0.0.0.0:8000",
        "--workers", "8",
        "--worker-class", "gevent",
        "--worker-connections", "1000",
        "--max-requests", "1000",
        "--timeout", "30",
        "--keepalive", "5",
        "--preload",
        "config.wsgi:application"
    ]
    
    print("Comando:", " ".join(cmd))
    
    try:
        # Ejecutar Gunicorn
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al iniciar Gunicorn: {e}")
        print("Intentando con Django development server...")
        
        # Fallback a Django dev server
        fallback_cmd = [
            "python", "manage.py", "runserver", "0.0.0.0:8000"
        ]
        subprocess.run(fallback_cmd)

if __name__ == "__main__":
    start_server()