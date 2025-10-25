from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from datetime import datetime, timedelta
from dashboard.utils import contar_usuarios, contar_ciudadanos
from legajos.models import LegajoAtencion, Ciudadano, SeguimientoContacto, Derivacion

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos básicos del sistema
        context["total_usuarios"] = contar_usuarios()
        context["total_ciudadanos"] = contar_ciudadanos()
        
        # Estadísticas de legajos
        context["total_legajos"] = LegajoAtencion.objects.count()
        context["legajos_abiertos"] = LegajoAtencion.objects.filter(estado='ABIERTO').count()
        context["legajos_seguimiento"] = LegajoAtencion.objects.filter(estado='EN_SEGUIMIENTO').count()
        context["legajos_riesgo_alto"] = LegajoAtencion.objects.filter(nivel_riesgo='ALTO').count()
        
        # Actividad reciente (últimos 7 días)
        fecha_limite = datetime.now().date() - timedelta(days=7)
        context["legajos_nuevos_semana"] = LegajoAtencion.objects.filter(fecha_apertura__gte=fecha_limite).count()
        context["seguimientos_semana"] = SeguimientoContacto.objects.filter(creado__date__gte=fecha_limite).count()
        context["derivaciones_pendientes"] = Derivacion.objects.filter(estado='PENDIENTE').count()
        
        # Legajos recientes para mostrar
        context["legajos_recientes"] = LegajoAtencion.objects.select_related(
            'ciudadano', 'dispositivo'
        ).order_by('-fecha_apertura')[:5]
        
        # Métricas de calidad para dashboard
        from legajos.views import ReportesView
        reportes_view = ReportesView()
        context["ttr_promedio"] = reportes_view._calcular_ttr_promedio()
        context["adherencia_adecuada"] = reportes_view._calcular_adherencia()
        
        return context