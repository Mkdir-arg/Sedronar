from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Conversacion(models.Model):
    TIPO_CHOICES = [
        ('anonima', 'Anónima'),
        ('personal', 'Personal'),
    ]
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cerrada', 'Cerrada'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')
    dni_ciudadano = models.CharField(max_length=8, blank=True, null=True)
    sexo_ciudadano = models.CharField(max_length=1, blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    operador_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
        
    def __str__(self):
        if self.tipo == 'personal' and self.dni_ciudadano:
            return f"Conversación {self.tipo} - DNI: {self.dni_ciudadano}"
        return f"Conversación {self.tipo} - #{self.id}"


class Mensaje(models.Model):
    REMITENTE_CHOICES = [
        ('ciudadano', 'Ciudadano'),
        ('operador', 'Operador'),
    ]
    
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.CharField(max_length=10, choices=REMITENTE_CHOICES)
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['fecha_envio']
        
    def __str__(self):
        return f"{self.remitente}: {self.contenido[:50]}..."


class HistorialAsignacion(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='historial_asignaciones')
    operador_anterior = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones_anteriores')
    operador_nuevo = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones_nuevas')
    usuario_que_asigna = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='asignaciones_realizadas')
    fecha_asignacion = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-fecha_asignacion']
        
    def __str__(self):
        return f"Conversación #{self.conversacion.id} - {self.operador_anterior} → {self.operador_nuevo}"