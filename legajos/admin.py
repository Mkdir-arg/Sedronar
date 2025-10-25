from django.contrib import admin
from .models import Ciudadano, Profesional, LegajoAtencion, Consentimiento, EvaluacionInicial


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
    list_display = ("codigo", "ciudadano", "dispositivo", "estado", "nivel_riesgo", "plan_vigente")
    list_filter = ("estado", "nivel_riesgo", "dispositivo__tipo", "via_ingreso")
    search_fields = ("codigo", "ciudadano__dni", "ciudadano__apellido", "ciudadano__nombre")
    readonly_fields = ("id", "codigo", "creado", "modificado", "fecha_apertura")
    
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