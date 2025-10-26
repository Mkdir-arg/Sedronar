#!/usr/bin/env python
"""
Script de instalación para el módulo Chatbot SEDRONAR
Ejecutar: python setup_chatbot.py
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_chatbot():
    """Configura el módulo chatbot"""
    
    print("🤖 Configurando Chatbot SEDRONAR...")
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    try:
        # 1. Crear migraciones
        print("📝 Creando migraciones...")
        execute_from_command_line(['manage.py', 'makemigrations', 'chatbot'])
        
        # 2. Aplicar migraciones
        print("🔄 Aplicando migraciones...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        # 3. Cargar datos iniciales
        print("📚 Cargando conocimiento inicial...")
        execute_from_command_line(['manage.py', 'loaddata', 'chatbot/fixtures/initial_knowledge.json'])
        
        print("✅ ¡Chatbot configurado exitosamente!")
        print("\n📋 Próximos pasos:")
        print("1. Agregar OPENAI_API_KEY a tu archivo .env")
        print("2. Reiniciar el servidor Django")
        print("3. Acceder a /chatbot/ para probar")
        print("4. Usar /chatbot/admin/ para gestionar conocimiento")
        
    except Exception as e:
        print(f"❌ Error durante la configuración: {e}")
        sys.exit(1)

if __name__ == '__main__':
    setup_chatbot()