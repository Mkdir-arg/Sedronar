from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStamped, LegajoBase, DispositivoRed


class Ciudadano(TimeStamped):
    """Modelo para ciudadanos del sistema de legajos"""
    
    dni = models.CharField(max_length=20, unique=True, db_index=True)
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120, db_index=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, blank=True)
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