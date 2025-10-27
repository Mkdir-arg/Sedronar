from django.urls import path
from . import views

app_name = 'conversaciones'

urlpatterns = [
    # URLs públicas para ciudadanos
    path('chat/', views.chat_ciudadano, name='chat_ciudadano'),
    path('consultar-renaper/', views.consultar_renaper, name='consultar_renaper'),
    path('iniciar/', views.iniciar_conversacion, name='iniciar_conversacion'),
    path('<int:conversacion_id>/enviar/', views.enviar_mensaje_ciudadano, name='enviar_mensaje_ciudadano'),
    path('<int:conversacion_id>/mensajes/', views.obtener_mensajes_ciudadano, name='obtener_mensajes_ciudadano'),
    
    # URLs del backoffice
    path('', views.lista_conversaciones, name='lista'),
    path('<int:conversacion_id>/', views.detalle_conversacion, name='detalle'),
    path('<int:conversacion_id>/asignar/', views.asignar_conversacion, name='asignar'),
    path('<int:conversacion_id>/reasignar/', views.reasignar_conversacion, name='reasignar'),
    path('<int:conversacion_id>/responder/', views.enviar_mensaje_operador, name='enviar_mensaje_operador'),
    path('<int:conversacion_id>/cerrar/', views.cerrar_conversacion, name='cerrar'),
]