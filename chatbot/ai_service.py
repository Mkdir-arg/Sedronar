from openai import OpenAI
from django.conf import settings
from django.contrib.auth.models import User
from legajos.models import Ciudadano
from .models import ChatbotKnowledge


class ChatbotAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
        self.max_tokens = 500
    
    def get_system_context(self):
        """Obtiene contexto del sistema SEDRONAR"""
        context = """
        Eres un asistente virtual del Sistema SEDRONAR (Secretaría Nacional de Políticas Integrales sobre Drogas).
        
        FUNCIONALIDADES DEL SISTEMA:
        - Gestión de Ciudadanos: Registro y seguimiento de personas
        - Legajos: Historiales detallados de atención
        - Usuarios: Administración de personal del sistema
        - Dashboard: Estadísticas y reportes
        
        INSTRUCCIONES:
        - Responde solo sobre funcionalidades del sistema SEDRONAR
        - Sé conciso y profesional
        - Si no sabes algo, sugiere contactar al administrador
        - No proporciones información personal de ciudadanos
        """
        
        # Agregar conocimiento personalizado (optimizado)
        knowledge = ChatbotKnowledge.objects.filter(is_active=True).only('title', 'content')
        if knowledge.exists():
            context += "\n\nCONOCIMIENTO ADICIONAL:\n"
            for item in knowledge:
                context += f"- {item.title}: {item.content}\n"
        
        return context
    
    def get_system_stats(self):
        """Obtiene estadísticas básicas del sistema (optimizado)"""
        try:
            from django.db.models import Count
            # Usar una sola consulta para obtener ambos conteos
            stats = {
                'ciudadanos': Ciudadano.objects.count(),
                'usuarios': User.objects.count()
            }
            return f"Estadísticas actuales: {stats['ciudadanos']} ciudadanos registrados, {stats['usuarios']} usuarios del sistema."
        except Exception as e:
            return f"Error obteniendo estadísticas: {str(e)}"
    
    def generate_response(self, message, conversation_history=None):
        """Genera respuesta usando OpenAI"""
        try:
            system_prompt = self.get_system_context()
            stats = self.get_system_stats()
            
            messages = [
                {"role": "system", "content": f"{system_prompt}\n\n{stats}"}
            ]
            
            # Agregar historial de conversación (últimos 5 mensajes)
            if conversation_history:
                # Optimizar acceso a mensajes con only() si es QuerySet
                if hasattr(conversation_history, 'only'):
                    history_msgs = conversation_history.only('role', 'content')[-5:]
                else:
                    history_msgs = conversation_history[-5:]
                    
                for msg in history_msgs:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Agregar mensaje actual
            messages.append({"role": "user", "content": message})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return {
                'content': response.choices[0].message.content,
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                'content': f"Error: {str(e)}",
                'tokens_used': 0,
                'error': str(e)
            }