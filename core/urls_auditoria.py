from django.urls import path
from . import views_auditoria

app_name = 'auditoria'

urlpatterns = [
    # Dashboard principal
    path('', views_auditoria.dashboard_auditoria, name='dashboard'),
    
    # Logs
    path('logs/acciones/', views_auditoria.logs_acciones, name='logs_acciones'),
    path('logs/descargas/', views_auditoria.logs_descargas, name='logs_descargas'),
    path('logs/exportar/', views_auditoria.exportar_logs, name='exportar_logs'),
    
    # Sesiones
    path('sesiones/', views_auditoria.sesiones_usuario, name='sesiones'),
    
    # Alertas
    path('alertas/', views_auditoria.alertas_auditoria, name='alertas'),
    path('alertas/<int:alerta_id>/revisar/', views_auditoria.marcar_alerta_revisada, name='marcar_alerta_revisada'),
    
    # Historial de cambios
    path('historial/', views_auditoria.historial_cambios, name='historial_cambios'),
]