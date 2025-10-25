from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStamped, LegajoBase, DispositivoRed


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
    
    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"
        indexes = [
            models.Index(fields=["dni"]),
            models.Index(fields=["apellido", "nombre"]),
        ]
    
    def __str__(self):
        return f"{self.apellido}, {self.nombre} ({self.dni})"


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
        DispositivoRed, 
        on_delete=models.PROTECT, 
        related_name="legajos"
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
    
    class Meta:
        verbose_name = "Legajo de Atención"
        verbose_name_plural = "Legajos de Atención"
        indexes = [
            models.Index(fields=["ciudadano", "dispositivo"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["nivel_riesgo", "fecha_admision"]),
        ]
    
    def __str__(self):
        return f"Legajo {self.codigo} - {self.ciudadano}"


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