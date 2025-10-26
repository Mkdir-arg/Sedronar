import openai
from django.conf import settings
from django.contrib.auth.models import User
from legajos.models import Ciudadano
from .models import ChatbotKnowledge


class ChatbotAIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
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
        
        # Agregar conocimiento personalizado
        knowledge = ChatbotKnowledge.objects.filter(is_active=True)
        if knowledge.exists():
            context += "\n\nCONOCIMIENTO ADICIONAL:\n"
            for item in knowledge:
                context += f"- {item.title}: {item.content}\n"
        
        return context
    
    def get_system_stats(self):
        """Obtiene estadísticas básicas del sistema"""
        try:
            total_ciudadanos = Ciudadano.objects.count()
            total_usuarios = User.objects.count()
            return f"Estadísticas actuales: {total_ciudadanos} ciudadanos registrados, {total_usuarios} usuarios del sistema."
        except:
            return "No se pudieron obtener las estadísticas del sistema."
    
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
                for msg in conversation_history[-5:]:
                    messages.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            # Agregar mensaje actual
            messages.append({"role": "user", "content": message})
            
            response = openai.ChatCompletion.create(
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
                'content': f"Lo siento, ocurrió un error al procesar tu consulta. Por favor, intenta nuevamente o contacta al administrador del sistema.",
                'tokens_used': 0,
                'error': str(e)
            }