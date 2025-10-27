from django.contrib import admin
from .models import Conversacion, Mensaje


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo', 'dni_ciudadano', 'estado', 'fecha_inicio', 'operador_asignado']
    list_filter = ['tipo', 'estado', 'fecha_inicio']
    search_fields = ['dni_ciudadano', 'id']
    readonly_fields = ['fecha_inicio']


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['conversacion', 'remitente', 'contenido_corto', 'fecha_envio', 'leido']
    list_filter = ['remitente', 'fecha_envio', 'leido']
    search_fields = ['contenido']
    readonly_fields = ['fecha_envio']
    
    def contenido_corto(self, obj):
        return obj.contenido[:50] + "..." if len(obj.contenido) > 50 else obj.contenido
    contenido_corto.short_description = 'Contenido'