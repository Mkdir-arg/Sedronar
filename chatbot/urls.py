from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('send/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/', views.load_conversation, name='load_conversation'),
    path('new/', views.new_conversation, name='new_conversation'),
    path('admin/', views.admin_panel, name='admin_panel'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
]