from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Conversacion(models.Model):
    TIPO_CHOICES = [
        ('anonima', 'Anónima'),
        ('personal', 'Personal'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activa', 'Activa'),
        ('cerrada', 'Cerrada'),
    ]
    
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('normal', 'Normal'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal')
    dni_ciudadano = models.CharField(max_length=8, blank=True, null=True)
    sexo_ciudadano = models.CharField(max_length=1, blank=True, null=True)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    fecha_asignacion = models.DateTimeField(blank=True, null=True)
    fecha_primera_respuesta = models.DateTimeField(blank=True, null=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)
    operador_asignado = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    tiempo_espera_segundos = models.IntegerField(default=0)
    tiempo_respuesta_segundos = models.IntegerField(blank=True, null=True)
    satisfaccion = models.IntegerField(blank=True, null=True, choices=[(i, i) for i in range(1, 6)])
    
    class Meta:
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['estado', 'prioridad']),
            models.Index(fields=['operador_asignado', 'estado']),
            models.Index(fields=['fecha_inicio']),
        ]
        
    def __str__(self):
        if self.tipo == 'personal' and self.dni_ciudadano:
            return f"Conversación {self.tipo} - DNI: {self.dni_ciudadano}"
        return f"Conversación {self.tipo} - #{self.id}"
    
    @property
    def tiempo_espera_minutos(self):
        if self.tiempo_espera_segundos:
            return round(self.tiempo_espera_segundos / 60, 1)
        return 0
    
    @property
    def tiempo_respuesta_minutos(self):
        if self.tiempo_respuesta_segundos:
            return round(self.tiempo_respuesta_segundos / 60, 1)
        return None
    
    def calcular_metricas(self):
        """Calcula métricas de tiempo de la conversación"""
        if self.fecha_asignacion:
            self.tiempo_espera_segundos = int((self.fecha_asignacion - self.fecha_inicio).total_seconds())
        
        if self.fecha_primera_respuesta and self.fecha_inicio:
            self.tiempo_respuesta_segundos = int((self.fecha_primera_respuesta - self.fecha_inicio).total_seconds())
        
        self.save()
    
    def asignar_operador(self, operador, usuario_asignador=None):
        """Asigna operador y registra métricas"""
        operador_anterior = self.operador_asignado
        self.operador_asignado = operador
        self.fecha_asignacion = timezone.now()
        self.estado = 'activa'
        self.save()  # Guardar cambios primero
        self.calcular_metricas()
        
        # Crear historial solo si el modelo existe
        try:
            HistorialAsignacion.objects.create(
                conversacion=self,
                operador_anterior=operador_anterior,
                operador_nuevo=operador,
                usuario_que_asigna=usuario_asignador or operador
            )
        except Exception:
            pass  # Si falla crear historial, continuar
    
    def marcar_primera_respuesta(self):
        """Marca la primera respuesta del operador"""
        if not self.fecha_primera_respuesta:
            self.fecha_primera_respuesta = timezone.now()
            self.calcular_metricas()


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


class ColaAsignacion(models.Model):
    """Sistema de cola para asignación automática de conversaciones"""
    operador = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cola_asignacion')
    activo = models.BooleanField(default=True)
    max_conversaciones = models.IntegerField(default=5)
    conversaciones_actuales = models.IntegerField(default=0)
    ultima_asignacion = models.DateTimeField(blank=True, null=True)
    peso_asignacion = models.IntegerField(default=1)  # Para balanceo de carga
    
    class Meta:
        ordering = ['conversaciones_actuales', 'ultima_asignacion']
        
    def __str__(self):
        return f"{self.operador.get_full_name()} - {self.conversaciones_actuales}/{self.max_conversaciones}"
    
    def puede_recibir_conversacion(self):
        return self.activo and self.conversaciones_actuales < self.max_conversaciones
    
    def actualizar_contador(self):
        """Actualiza el contador de conversaciones actuales"""
        self.conversaciones_actuales = Conversacion.objects.filter(
            operador_asignado=self.operador,
            estado='activa'
        ).count()
        self.save()


class MetricasOperador(models.Model):
    """Métricas de rendimiento por operador"""
    operador = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metricas_conversaciones')
    conversaciones_atendidas = models.IntegerField(default=0)
    tiempo_respuesta_promedio = models.FloatField(default=0.0)  # en minutos
    satisfaccion_promedio = models.FloatField(default=0.0)
    conversaciones_cerradas = models.IntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Métricas de Operadores"
        
    def __str__(self):
        return f"Métricas - {self.operador.get_full_name()}"
    
    def actualizar_metricas(self):
        """Actualiza las métricas del operador"""
        conversaciones = Conversacion.objects.filter(operador_asignado=self.operador)
        
        self.conversaciones_atendidas = conversaciones.count()
        self.conversaciones_cerradas = conversaciones.filter(estado='cerrada').count()
        
        # Tiempo de respuesta promedio
        tiempos = conversaciones.filter(
            tiempo_respuesta_segundos__isnull=False
        ).values_list('tiempo_respuesta_segundos', flat=True)
        
        if tiempos:
            self.tiempo_respuesta_promedio = sum(tiempos) / len(tiempos) / 60  # convertir a minutos
        
        # Satisfacción promedio
        satisfacciones = conversaciones.filter(
            satisfaccion__isnull=False
        ).values_list('satisfaccion', flat=True)
        
        if satisfacciones:
            self.satisfaccion_promedio = sum(satisfacciones) / len(satisfacciones)
        
        self.save()


class NuevaConversacionAlerta(models.Model):
    """Registro temporal de nuevas conversaciones para operadores"""
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    vista = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['conversacion', 'operador']
        
    def __str__(self):
        return f'Nueva conversación #{self.conversacion.id} para {self.operador.username}'


class HistorialAlertaConversacion(models.Model):
    """Historial de alertas de conversaciones"""
    TIPO_CHOICES = [
        ('NUEVA_CONVERSACION', 'Nueva Conversación'),
        ('NUEVO_MENSAJE', 'Nuevo Mensaje'),
        ('RIESGO_CRITICO', 'Riesgo Crítico'),
    ]
    
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    mensaje = models.CharField(max_length=200)
    vista = models.BooleanField(default=False)
    fecha_vista = models.DateTimeField(null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-creado']
        
    def __str__(self):
        return f'{self.tipo} - Conv #{self.conversacion.id} - {self.operador.username}'