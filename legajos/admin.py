from django.contrib import admin
from .models import Ciudadano, Profesional, LegajoAtencion, Consentimiento, EvaluacionInicial, Objetivo, PlanIntervencion, SeguimientoContacto, Derivacion, EventoCritico, Adjunto, AlertaEventoCritico


@admin.register(Ciudadano)
class CiudadanoAdmin(admin.ModelAdmin):
    list_display = ("dni", "apellido", "nombre", "activo", "creado")
    search_fields = ("dni", "apellido", "nombre")
    list_filter = ("activo", "genero")
    ordering = ("apellido", "nombre")
    readonly_fields = ("creado", "modificado")
    
    fieldsets = (
        ("Información Personal", {
            "fields": ("dni", "nombre", "apellido", "fecha_nacimiento", "genero")
        }),
        ("Contacto", {
            "fields": ("telefono", "email", "domicilio")
        }),
        ("Estado", {
            "fields": ("activo",)
        }),
        ("Auditoría", {
            "fields": ("creado", "modificado"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Profesional)
class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ("usuario", "rol", "matricula")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "rol", "matricula")
    list_filter = ("rol",)


@admin.register(LegajoAtencion)
class LegajoAtencionAdmin(admin.ModelAdmin):
    list_display = ("codigo_corto", "ciudadano", "dispositivo", "estado", "nivel_riesgo", "plan_vigente", "fecha_apertura")
    list_filter = ("estado", "nivel_riesgo", "dispositivo__provincia", "dispositivo__tipo", "via_ingreso", "plan_vigente")
    search_fields = ("codigo", "ciudadano__dni", "ciudadano__apellido", "ciudadano__nombre")
    readonly_fields = ("id", "codigo", "creado", "modificado", "fecha_apertura", "dias_desde_admision")
    
    def codigo_corto(self, obj):
        return f"{obj.codigo[:8]}..."
    codigo_corto.short_description = 'Código'
    
    fieldsets = (
        ("Información Básica", {
            "fields": ("codigo", "ciudadano", "dispositivo", "responsable")
        }),
        ("Admisión", {
            "fields": ("via_ingreso", "fecha_admision", "nivel_riesgo")
        }),
        ("Estado", {
            "fields": ("estado", "fecha_cierre", "plan_vigente", "confidencialidad")
        }),
        ("Observaciones", {
            "fields": ("notas",)
        }),
        ("Auditoría", {
            "fields": ("id", "creado", "modificado"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Consentimiento)
class ConsentimientoAdmin(admin.ModelAdmin):
    list_display = ("ciudadano", "firmado_por", "fecha_firma", "vigente")
    list_filter = ("vigente", "fecha_firma")
    search_fields = ("ciudadano__dni", "ciudadano__apellido", "ciudadano__nombre")
    readonly_fields = ("creado", "modificado")


@admin.register(EvaluacionInicial)
class EvaluacionInicialAdmin(admin.ModelAdmin):
    list_display = ("legajo", "riesgo_suicida", "violencia", "creado")
    list_filter = ("riesgo_suicida", "violencia", "creado")
    search_fields = ("legajo__codigo", "legajo__ciudadano__dni", "legajo__ciudadano__apellido")
    readonly_fields = ("creado", "modificado")
    
    fieldsets = (
        ("Información Básica", {
            "fields": ("legajo",)
        }),
        ("Evaluación Clínica", {
            "fields": ("situacion_consumo", "antecedentes")
        }),
        ("Evaluación Psicosocial", {
            "fields": ("red_apoyo", "condicion_social")
        }),
        ("Tamizajes y Riesgos", {
            "fields": ("tamizajes", "riesgo_suicida", "violencia")
        }),
        ("Auditoría", {
            "fields": ("creado", "modificado"),
            "classes": ("collapse",)
        }),
    )


@admin.register(Objetivo)
class ObjetivoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'legajo', 'cumplido']
    list_filter = ['cumplido']
    search_fields = ['descripcion', 'legajo__codigo']


@admin.register(PlanIntervencion)
class PlanIntervencionAdmin(admin.ModelAdmin):
    list_display = ['legajo', 'profesional', 'vigente', 'creado']
    list_filter = ['vigente', 'creado']
    search_fields = ['legajo__codigo']


@admin.register(SeguimientoContacto)
class SeguimientoContactoAdmin(admin.ModelAdmin):
    list_display = ['legajo', 'tipo', 'profesional', 'adherencia', 'creado']
    list_filter = ['tipo', 'adherencia', 'creado']
    search_fields = ['legajo__codigo', 'descripcion', 'profesional__usuario__username']
    date_hierarchy = 'creado'


@admin.register(Derivacion)
class DerivacionAdmin(admin.ModelAdmin):
    list_display = ['legajo', 'origen', 'destino', 'urgencia', 'estado', 'creado']
    list_filter = ['urgencia', 'estado', 'origen__provincia', 'destino__provincia', 'creado']
    search_fields = ['legajo__codigo', 'motivo', 'origen__nombre', 'destino__nombre']
    date_hierarchy = 'creado'


@admin.register(EventoCritico)
class EventoCriticoAdmin(admin.ModelAdmin):
    list_display = ['legajo', 'tipo', 'creado']
    list_filter = ['tipo', 'creado']
    search_fields = ['legajo__codigo', 'detalle']


@admin.register(Adjunto)
class AdjuntoAdmin(admin.ModelAdmin):
    list_display = ['etiqueta', 'content_type', 'object_id', 'creado']
    list_filter = ['content_type', 'creado']
    search_fields = ['etiqueta']


@admin.register(AlertaEventoCritico)
class AlertaEventoCriticoAdmin(admin.ModelAdmin):
    list_display = ['evento', 'responsable', 'fecha_cierre']
    list_filter = ['fecha_cierre', 'evento__tipo']
    search_fields = ['evento__legajo__codigo', 'responsable__username']
    readonly_fields = ['fecha_cierre']