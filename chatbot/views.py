from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core.paginator import Paginator
import json
from .models import Conversation, Message, ChatbotKnowledge, ChatbotFeedback
from .ai_service import ChatbotAIService


@login_required
def chat_interface(request):
    """Interfaz principal del chat"""
    conversations = Conversation.objects.filter(user=request.user)[:10]
    active_conversation = conversations.first() if conversations.exists() else None
    
    context = {
        'conversations': conversations,
        'active_conversation': active_conversation,
    }
    return render(request, 'chatbot/chat_interface.html', context)


@login_required
@csrf_exempt
def send_message(request):
    """Envía mensaje al chatbot"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        message_content = data.get('message', '').strip()
        conversation_id = data.get('conversation_id')
        
        if not message_content:
            return JsonResponse({'error': 'Mensaje vacío'}, status=400)
        
        # Obtener o crear conversación
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(
                user=request.user,
                title=message_content[:50] + "..." if len(message_content) > 50 else message_content
            )
        
        # Guardar mensaje del usuario
        user_message = Message.objects.create(
            conversation=conversation,
            role='user',
            content=message_content
        )
        
        # Obtener historial de conversación
        history = conversation.messages.all()
        
        # Generar respuesta con IA
        ai_service = ChatbotAIService()
        response_data = ai_service.generate_response(message_content, history)
        
        # Guardar respuesta del asistente
        assistant_message = Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_data['content'],
            tokens_used=response_data.get('tokens_used', 0)
        )
        
        # Actualizar timestamp de conversación
        conversation.save()
        
        return JsonResponse({
            'success': True,
            'conversation_id': conversation.id,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'timestamp': user_message.timestamp.isoformat()
            },
            'assistant_message': {
                'id': assistant_message.id,
                'content': assistant_message.content,
                'timestamp': assistant_message.timestamp.isoformat()
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def load_conversation(request, conversation_id):
    """Carga una conversación específica"""
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    messages = conversation.messages.all()
    
    messages_data = []
    for message in messages:
        messages_data.append({
            'id': message.id,
            'role': message.role,
            'content': message.content,
            'timestamp': message.timestamp.isoformat()
        })
    
    return JsonResponse({
        'conversation_id': conversation.id,
        'title': conversation.title,
        'messages': messages_data
    })


@login_required
def new_conversation(request):
    """Crea una nueva conversación"""
    conversation = Conversation.objects.create(
        user=request.user,
        title="Nueva conversación"
    )
    return JsonResponse({
        'conversation_id': conversation.id,
        'title': conversation.title
    })


@login_required
def admin_panel(request):
    """Panel de administración del chatbot"""
    if not request.user.is_staff:
        messages.error(request, 'No tienes permisos para acceder a esta sección.')
        return redirect('chatbot:chat_interface')
    
    # Estadísticas
    total_conversations = Conversation.objects.count()
    total_messages = Message.objects.count()
    total_knowledge = ChatbotKnowledge.objects.filter(is_active=True).count()
    
    # Conocimiento base
    knowledge_list = ChatbotKnowledge.objects.all().order_by('-created_at')
    paginator = Paginator(knowledge_list, 10)
    page = request.GET.get('page')
    knowledge = paginator.get_page(page)
    
    context = {
        'total_conversations': total_conversations,
        'total_messages': total_messages,
        'total_knowledge': total_knowledge,
        'knowledge': knowledge,
    }
    return render(request, 'chatbot/admin_panel.html', context)


@login_required
@csrf_exempt
def submit_feedback(request):
    """Envía feedback sobre una respuesta"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        message_id = data.get('message_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        message = get_object_or_404(Message, id=message_id)
        
        feedback, created = ChatbotFeedback.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={'rating': rating, 'comment': comment}
        )
        
        if not created:
            feedback.rating = rating
            feedback.comment = comment
            feedback.save()
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)