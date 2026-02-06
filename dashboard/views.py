from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.decorators import method_decorator
from datetime import datetime, timedelta
from dashboard.utils import contar_usuarios, contar_ciudadanos
from legajos.models import LegajoAtencion, Ciudadano, SeguimientoContacto, AlertaCiudadano
from users.models import User
from core.cache_decorators import cache_view

@method_decorator(cache_view(timeout=60), name='dispatch')
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from dashboard.utils import (
            contar_usuarios, contar_ciudadanos, contar_legajos,
            contar_seguimientos_hoy, contar_alertas_activas
        )
        
        # Datos con caché
        context["total_usuarios"] = contar_usuarios()
        context["total_ciudadanos"] = contar_ciudadanos()
        
        legajo_stats = contar_legajos()
        context["total_legajos"] = legajo_stats['total']
        context["legajos_activos"] = legajo_stats['activos']
        
        context["seguimientos_hoy"] = contar_seguimientos_hoy()
        context["alertas_activas"] = contar_alertas_activas()
        context["actividad_hoy"] = context["seguimientos_hoy"]
        
        # Solo datos dinámicos sin caché
        hace_24h = timezone.now() - timedelta(hours=24)
        context["usuarios_activos"] = User.objects.filter(
            last_login__gte=hace_24h
        ).count()
        
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        context["registros_mes"] = LegajoAtencion.objects.filter(
            fecha_apertura__gte=inicio_mes
        ).count()
        
        return context