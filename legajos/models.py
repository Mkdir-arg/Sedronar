from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from core.models import TimeStamped, LegajoBase, Institucion
# from simple_history.models import HistoricalRecords  # Comentado temporalmente

# Alias para compatibilidad
DispositivoRed = Institucion


class Ciudadano(TimeStamped):
    """Modelo para ciudadanos del sistema de legajos"""
    
    class Genero(models.TextChoices):
        MASCULINO = "M", "Masculino"
        FEMENINO = "F", "Femenino"
        NO_BINARIO = "X", "No binario"
    
    dni = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120, db_index=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=1, choices=Genero.choices, blank=True)
    telefono = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    domicilio = models.CharField(max_length=240, blank=True)
    activo = models.BooleanField(default=True)
    
    # Historial de cambios
    # history = HistoricalRecords()  # Comentado temporalmente
    
    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"
        indexes = [
            models.Index(fields=["dni"]),
            models.Index(fields=["apellido", "nombre"]),
        ]
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"
    
    @property
    def nombre_completo(self):
        """Retorna el nombre completo del ciudadano"""
        return f"{self.nombre} {self.apellido}"


class Profesional(TimeStamped):
    """Profesionales que trabajan con legajos"""
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=60, blank=True)
    rol = models.CharField(max_length=80, blank=True)
    
    class Meta:
        verbose_name = "Profesional"
        verbose_name_plural = "Profesionales"
    
    def __str__(self):
        return f"{self.usuario.get_full_name() or self.usuario.username}"


class LegajoAtencion(LegajoBase):
    """Legajo de atención individual para ciudadanos"""
    
    class ViaIngreso(models.TextChoices):
        ESPONTANEA = "ESPONTANEA", "Consulta espontánea"
        DERIVACION = "DERIVACION", "Derivación"
        JUDICIAL = "JUDICIAL", "Judicial"
        HOSPITAL = "HOSPITAL", "Hospital/Guardia"
    
    class NivelRiesgo(models.TextChoices):
        BAJO = "BAJO", "Bajo"
        MEDIO = "MEDIO", "Medio"
        ALTO = "ALTO", "Alto"
    
    ciudadano = models.ForeignKey(
        Ciudadano, 
        on_delete=models.PROTECT, 
        related_name="legajos"
    )
    dispositivo = models.ForeignKey(
        Institucion, 
        on_delete=models.PROTECT, 
        related_name="legajos",
        verbose_name="Institución"
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="legajos_atencion_responsable",
        limit_choices_to={'groups__name': 'Responsable'},
        verbose_name="Responsable",
        help_text="Usuario con rol de Responsable asignado al legajo"
    )
    via_ingreso = models.CharField(
        max_length=20, 
        choices=ViaIngreso.choices, 
        default=ViaIngreso.ESPONTANEA
    )
    fecha_admision = models.DateField(auto_now_add=True)
    plan_vigente = models.BooleanField(default=False)
    nivel_riesgo = models.CharField(
        max_length=20, 
        choices=NivelRiesgo.choices, 
        default=NivelRiesgo.BAJO
    )
    
    # Historial de cambios
    # history = HistoricalRecords()  # Comentado temporalmente
    
    class Meta:
        verbose_name = "Acompañamiento"
        verbose_name_plural = "Acompañamientos"
        indexes = [
            models.Index(fields=["ciudadano", "dispositivo"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["nivel_riesgo", "fecha_admision"]),
        ]
    
    def __str__(self):
        return f"Legajo {self.codigo} - {self.ciudadano}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('legajos:detalle', kwargs={'pk': self.pk})
    
    def puede_cerrar(self):
        """Verifica si el legajo puede cerrarse"""
        from datetime import datetime, timedelta
        if self.estado == 'CERRADO':
            return False, "El legajo ya está cerrado"
        
        # Verificar seguimiento reciente (últimos 30 días)
        fecha_limite = datetime.now().date() - timedelta(days=30)
        tiene_seguimiento_reciente = self.seguimientos.filter(
            creado__date__gte=fecha_limite
        ).exists()
        
        if self.plan_vigente and not tiene_seguimiento_reciente:
            return False, "Requiere seguimiento reciente o justificación para cerrar"
        
        return True, "Puede cerrarse"
    
    def cerrar(self, motivo_cierre=None, usuario=None):
        """Cierra el legajo"""
        puede, mensaje = self.puede_cerrar()
        if not puede and not motivo_cierre:
            raise ValidationError(mensaje)
        
        self.estado = 'CERRADO'
        self.fecha_cierre = datetime.now().date()
        if motivo_cierre:
            if not self.notas:
                self.notas = f"Motivo de cierre: {motivo_cierre}"
            else:
                self.notas += f"\n\nMotivo de cierre: {motivo_cierre}"
        self.save()
    
    def reabrir(self, motivo_reapertura=None, usuario=None):
        """Reabre el legajo"""
        if self.estado != 'CERRADO':
            raise ValidationError("Solo se pueden reabrir legajos cerrados")
        
        self.estado = 'EN_SEGUIMIENTO'
        self.fecha_cierre = None
        if motivo_reapertura:
            if not self.notas:
                self.notas = f"Motivo de reapertura: {motivo_reapertura}"
            else:
                self.notas += f"\n\nMotivo de reapertura: {motivo_reapertura}"
        self.save()
    
    @property
    def dias_desde_admision(self):
        """Días transcurridos desde la admisión"""
        from datetime import datetime
        return (datetime.now().date() - self.fecha_admision).days
    
    @property
    def tiempo_primer_contacto(self):
        """Días hasta el primer seguimiento"""
        primer_seguimiento = self.seguimientos.order_by('creado').first()
        if primer_seguimiento:
            return (primer_seguimiento.creado.date() - self.fecha_admision).days
        return None


class Consentimiento(TimeStamped):
    """Consentimientos informados para tratamiento de datos"""
    
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.PROTECT)
    texto = models.TextField()
    firmado_por = models.CharField(max_length=160)
    fecha_firma = models.DateField()
    archivo = models.FileField(upload_to="consentimientos/", null=True, blank=True)
    vigente = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Consentimiento"
        verbose_name_plural = "Consentimientos"
    
    def __str__(self):
        return f"Consentimiento {self.ciudadano} - {self.fecha_firma}"


class EvaluacionInicial(TimeStamped):
    """Evaluación inicial clínico-psicosocial del legajo"""
    
    legajo = models.OneToOneField(
        LegajoAtencion, 
        on_delete=models.CASCADE, 
        related_name="evaluacion"
    )
    situacion_consumo = models.TextField(
        blank=True,
        verbose_name="Situación de Consumo",
        help_text="Descripción de la situación actual de consumo"
    )
    antecedentes = models.TextField(
        blank=True,
        verbose_name="Antecedentes",
        help_text="Antecedentes médicos, psiquiátricos y de consumo"
    )
    red_apoyo = models.TextField(
        blank=True,
        verbose_name="Red de Apoyo",
        help_text="Descripción de la red de apoyo familiar y social"
    )
    condicion_social = models.TextField(
        blank=True,
        verbose_name="Condición Social",
        help_text="Situación socioeconómica, vivienda, trabajo, educación"
    )
    tamizajes = models.JSONField(
        blank=True, 
        null=True,
        verbose_name="Tamizajes",
        help_text="Resultados de tamizajes aplicados (ej: ASSIST, PHQ-9)"
    )
    riesgo_suicida = models.BooleanField(
        default=False,
        verbose_name="Riesgo Suicida",
        help_text="Indica si presenta riesgo suicida"
    )
    violencia = models.BooleanField(
        default=False,
        verbose_name="Situación de Violencia",
        help_text="Indica si presenta situación de violencia"
    )
    
    class Meta:
        verbose_name = "Evaluación Inicial"
        verbose_name_plural = "Evaluaciones Iniciales"
        indexes = [
            models.Index(fields=["riesgo_suicida"]),
            models.Index(fields=["violencia"]),
        ]
    
    def __str__(self):
        return f"Evaluación - {self.legajo.codigo}"
    
    @property
    def tiene_riesgos(self):
        """Indica si tiene algún tipo de riesgo identificado"""
        return self.riesgo_suicida or self.violencia
    
    @property
    def riesgos_identificados(self):
        """Lista de riesgos identificados"""
        riesgos = []
        if self.riesgo_suicida:
            riesgos.append("Riesgo Suicida")
        if self.violencia:
            riesgos.append("Violencia")
        return riesgos
    
    @property
    def tiene_eventos_criticos(self):
        """Indica si el legajo tiene eventos críticos recientes"""
        from datetime import datetime, timedelta
        fecha_limite = datetime.now().date() - timedelta(days=30)
        return self.legajo.eventos.filter(creado__date__gte=fecha_limite).exists()


class Objetivo(models.Model):
    """Objetivos del plan de intervención"""
    
    legajo = models.ForeignKey(
        LegajoAtencion, 
        on_delete=models.CASCADE, 
        related_name="objetivos"
    )
    descripcion = models.CharField(max_length=240)
    indicador_exito = models.CharField(max_length=240, blank=True)
    cumplido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Objetivo"
        verbose_name_plural = "Objetivos"
    
    def __str__(self):
        return f"Objetivo - {self.descripcion[:50]}"


class PlanIntervencion(TimeStamped):
    """Plan de intervención para el legajo"""
    
    legajo = models.ForeignKey(
        LegajoAtencion, 
        on_delete=models.CASCADE, 
        related_name="planes"
    )
    profesional = models.ForeignKey(
        Profesional, 
        on_delete=models.PROTECT
    )
    vigente = models.BooleanField(default=True)
    actividades = models.JSONField(
        blank=True, 
        null=True,
        help_text="Lista de actividades: [{\"accion\":\"Entrevista\",\"freq\":\"semanal\",\"responsable\":\"operador\"}]"
    )
    
    class Meta:
        verbose_name = "Plan de Intervención"
        verbose_name_plural = "Planes de Intervención"
        indexes = [
            models.Index(fields=["legajo", "vigente"]),
        ]
    
    def __str__(self):
        return f"Plan {self.legajo.codigo} - {'Vigente' if self.vigente else 'Histórico'}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Solo validar si el legajo ya está asignado
        if self.vigente and hasattr(self, 'legajo') and self.legajo and PlanIntervencion.objects.filter(
            legajo=self.legajo, vigente=True
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Ya existe un plan vigente para este legajo.")
    
    def save(self, *args, **kwargs):
        from django.db import transaction
        self.clean()
        with transaction.atomic():
            if self.vigente:
                PlanIntervencion.objects.select_for_update().filter(
                    legajo=self.legajo, vigente=True
                ).exclude(pk=self.pk).update(vigente=False)
                LegajoAtencion.objects.filter(pk=self.legajo_id).update(plan_vigente=True)
            super().save(*args, **kwargs)


class SeguimientoContacto(TimeStamped):
    """Contactos y seguimientos del legajo"""
    
    class TipoContacto(models.TextChoices):
        ENTREVISTA = "ENTREVISTA", "Entrevista"
        VISITA = "VISITA", "Visita"
        LLAMADA = "LLAMADA", "Llamada"
        TALLER = "TALLER", "Taller"
    
    class Adherencia(models.TextChoices):
        ADECUADA = "ADECUADA", "Adecuada"
        PARCIAL = "PARCIAL", "Parcial"
        NULA = "NULA", "Nula"
    
    legajo = models.ForeignKey(
        LegajoAtencion, 
        on_delete=models.CASCADE, 
        related_name="seguimientos"
    )
    profesional = models.ForeignKey(
        Profesional, 
        on_delete=models.PROTECT
    )
    tipo = models.CharField(
        max_length=40, 
        choices=TipoContacto.choices
    )
    descripcion = models.TextField()
    adherencia = models.CharField(
        max_length=20, 
        choices=Adherencia.choices,
        blank=True
    )
    adjuntos = models.FileField(
        upload_to="seguimientos/", 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = "Seguimiento"
        verbose_name_plural = "Seguimientos"
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["legajo", "-creado"]),
            models.Index(fields=["tipo"]),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.legajo.codigo} ({self.creado.date()})"


class Derivacion(TimeStamped):
    """Derivaciones entre dispositivos"""
    
    class Urgencia(models.TextChoices):
        BAJA = "BAJA", "Baja"
        MEDIA = "MEDIA", "Media"
        ALTA = "ALTA", "Alta"
    
    class Estado(models.TextChoices):
        PENDIENTE = "PENDIENTE", "Pendiente"
        ACEPTADA = "ACEPTADA", "Aceptada"
        RECHAZADA = "RECHAZADA", "Rechazada"
    
    legajo = models.ForeignKey(
        LegajoAtencion, 
        on_delete=models.CASCADE, 
        related_name="derivaciones"
    )
    origen = models.ForeignKey(
        Institucion, 
        on_delete=models.PROTECT, 
        related_name="derivaciones_origen",
        verbose_name="Institución Origen"
    )
    destino = models.ForeignKey(
        Institucion, 
        on_delete=models.PROTECT, 
        related_name="derivaciones_destino",
        verbose_name="Institución Destino"
    )
    motivo = models.TextField()
    urgencia = models.CharField(
        max_length=20, 
        choices=Urgencia.choices, 
        default=Urgencia.MEDIA
    )
    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.PENDIENTE
    )
    respuesta = models.CharField(max_length=120, blank=True)
    fecha_aceptacion = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Derivación"
        verbose_name_plural = "Derivaciones"
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["legajo", "estado"]),
            models.Index(fields=["urgencia"]),
        ]
    
    def __str__(self):
        return f"Derivación {self.origen.nombre} → {self.destino.nombre}"
    
    def clean(self):
        if hasattr(self, 'destino') and self.destino and not self.destino.activo:
            raise ValidationError("No es posible derivar a un dispositivo inactivo.")
        if hasattr(self, 'origen') and self.origen and hasattr(self, 'destino') and self.destino and self.origen == self.destino:
            raise ValidationError("No se puede derivar al mismo dispositivo.")


class EventoCritico(TimeStamped):
    """Eventos críticos del legajo"""
    
    class TipoEvento(models.TextChoices):
        SOBREDOSIS = "SOBREDOSIS", "Sobredosis"
        CRISIS = "CRISIS", "Crisis aguda"
        VIOLENCIA = "VIOLENCIA", "Violencia"
        INTERNACION = "INTERNACION", "Internación"
    
    legajo = models.ForeignKey(
        LegajoAtencion, 
        on_delete=models.CASCADE, 
        related_name="eventos"
    )
    tipo = models.CharField(
        max_length=40, 
        choices=TipoEvento.choices
    )
    detalle = models.TextField()
    notificado_a = models.JSONField(
        blank=True, 
        null=True,
        help_text="Lista de familiares/autoridades notificadas"
    )
    
    class Meta:
        verbose_name = "Evento Crítico"
        verbose_name_plural = "Eventos Críticos"
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["legajo", "tipo"]),
            models.Index(fields=["-creado"]),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.legajo.codigo} ({self.creado.date()})"


class Adjunto(TimeStamped):
    """Adjuntos genéricos para cualquier modelo"""
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey("content_type", "object_id")
    archivo = models.FileField(upload_to="adjuntos/")
    etiqueta = models.CharField(max_length=120, blank=True)
    
    class Meta:
        verbose_name = "Adjunto"
        verbose_name_plural = "Adjuntos"
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
    
    def __str__(self):
        return f"Adjunto - {self.etiqueta or self.archivo.name}"


class AlertaEventoCritico(TimeStamped):
    """Registro de alertas vistas por responsables"""
    
    evento = models.ForeignKey(
        EventoCritico,
        on_delete=models.CASCADE,
        related_name="alertas_vistas"
    )
    responsable = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="alertas_eventos_vistas"
    )
    fecha_cierre = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Alerta Evento Crítico"
        verbose_name_plural = "Alertas Eventos Críticos"
        unique_together = ["evento", "responsable"]
        indexes = [
            models.Index(fields=["responsable", "fecha_cierre"]),
        ]
    
    def __str__(self):
        return f"Alerta {self.evento.tipo} vista por {self.responsable.username}"


class AlertaCiudadano(TimeStamped):
    """Sistema de alertas automáticas para ciudadanos"""
    
    class TipoAlerta(models.TextChoices):
        RIESGO_ALTO = "RIESGO_ALTO", "Riesgo Alto"
        RIESGO_SUICIDA = "RIESGO_SUICIDA", "Riesgo Suicida"
        VIOLENCIA = "VIOLENCIA", "Situación de Violencia"
        SIN_CONTACTO = "SIN_CONTACTO", "Sin Contacto Prolongado"
        SIN_EVALUACION = "SIN_EVALUACION", "Sin Evaluación Inicial"
        SIN_PLAN = "SIN_PLAN", "Sin Plan de Intervención"
        EVENTO_CRITICO = "EVENTO_CRITICO", "Evento Crítico Reciente"
        DERIVACION_PENDIENTE = "DERIVACION_PENDIENTE", "Derivación Pendiente"
        SIN_RED_FAMILIAR = "SIN_RED_FAMILIAR", "Sin Red Familiar"
        SIN_CONSENTIMIENTO = "SIN_CONSENTIMIENTO", "Sin Consentimiento"
        CONTACTOS_FALLIDOS = "CONTACTOS_FALLIDOS", "Contactos Fallidos"
        PLAN_VENCIDO = "PLAN_VENCIDO", "Plan Vencido"
    
    class Prioridad(models.TextChoices):
        CRITICA = "CRITICA", "Crítica"
        ALTA = "ALTA", "Alta"
        MEDIA = "MEDIA", "Media"
        BAJA = "BAJA", "Baja"
    
    ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.CASCADE,
        related_name="alertas"
    )
    legajo = models.ForeignKey(
        LegajoAtencion,
        on_delete=models.CASCADE,
        related_name="alertas",
        null=True,
        blank=True
    )
    tipo = models.CharField(max_length=30, choices=TipoAlerta.choices)
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices)
    mensaje = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    cerrada_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="alertas_cerradas"
    )
    
    class Meta:
        verbose_name = "Alerta de Ciudadano"
        verbose_name_plural = "Alertas de Ciudadanos"
        ordering = ["-creado"]
        indexes = [
            models.Index(fields=["ciudadano", "activa"]),
            models.Index(fields=["tipo", "prioridad"]),
            models.Index(fields=["legajo", "activa"]),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.ciudadano}"
    
    def cerrar(self, usuario=None):
        """Cerrar la alerta"""
        self.activa = False
        self.fecha_cierre = timezone.now()
        self.cerrada_por = usuario
        self.save()
    
    @property
    def color_css(self):
        """Retorna las clases CSS según la prioridad"""
        colores = {
            'CRITICA': 'bg-red-100 text-red-800 border-red-200',
            'ALTA': 'bg-orange-100 text-orange-800 border-orange-200',
            'MEDIA': 'bg-yellow-100 text-yellow-800 border-yellow-200',
            'BAJA': 'bg-blue-100 text-blue-800 border-blue-200',
        }
        return colores.get(self.prioridad, 'bg-gray-100 text-gray-800 border-gray-200')


# Importar modelos de contactos
from .models_contactos import (
    HistorialContacto, VinculoFamiliar, ProfesionalTratante,
    DispositivoVinculado, ContactoEmergencia
)

# Importar timezone
from django.utils import timezone