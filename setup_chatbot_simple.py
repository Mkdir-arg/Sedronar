#!/usr/bin/env python
"""
Script simple para configurar el chatbot SEDRONAR
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chatbot.models import ChatbotKnowledge

def setup_chatbot():
    """Configura el conocimiento base del chatbot"""
    
    knowledge_items = [
        {
            'title': 'Sistema SEDRONAR',
            'content': 'SEDRONAR es el Sistema de la Secretaría Nacional de Políticas Integrales sobre Drogas de Argentina. Gestiona ciudadanos, legajos de atención y usuarios del sistema.',
            'category': 'general'
        },
        {
            'title': 'Gestión de Ciudadanos',
            'content': 'El módulo de ciudadanos permite registrar personas, gestionar su información personal y crear legajos de atención.',
            'category': 'funcionalidad'
        },
        {
            'title': 'Legajos de Atención',
            'content': 'Los legajos contienen el historial completo de atención de cada ciudadano, incluyendo evaluaciones, seguimientos y derivaciones.',
            'category': 'funcionalidad'
        }
    ]
    
    print("🤖 Configurando conocimiento base del chatbot...")
    
    for item in knowledge_items:
        knowledge, created = ChatbotKnowledge.objects.get_or_create(
            title=item['title'],
            defaults={
                'content': item['content'],
                'category': item['category'],
                'is_active': True
            }
        )
        
        if created:
            print(f"✅ Creado: {item['title']}")
        else:
            print(f"ℹ️  Ya existe: {item['title']}")
    
    print("\n🎉 ¡Chatbot configurado correctamente!")
    print("\n📋 Próximos pasos:")
    print("1. Agregar tu API Key de OpenAI al archivo .env:")
    print("   OPENAI_API_KEY=tu-api-key-aqui")
    print("2. Reiniciar el servidor Django")
    print("3. La burbuja del chatbot aparecerá en la esquina inferior derecha")
    print("4. El panel de administración está en el menú Administración > Chatbot")

if __name__ == '__main__':
    setup_chatbot()