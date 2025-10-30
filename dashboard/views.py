from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Count, Q
from django.utils import timezone
from datetime import datetime, timedelta
from dashboard.utils import contar_usuarios, contar_ciudadanos
from legajos.models import LegajoAtencion, Ciudadano, SeguimientoContacto, AlertaCiudadano
from users.models import User

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos básicos del sistema
        context["total_usuarios"] = User.objects.filter(is_active=True).count()
        context["total_ciudadanos"] = Ciudadano.objects.count()
        
        # Estadísticas de legajos
        context["total_legajos"] = LegajoAtencion.objects.count()
        context["legajos_activos"] = LegajoAtencion.objects.filter(estado__in=['ABIERTO', 'EN_SEGUIMIENTO']).count()
        
        # Actividad de hoy
        hoy = timezone.now().date()
        context["seguimientos_hoy"] = SeguimientoContacto.objects.filter(creado__date=hoy).count()
        context["alertas_activas"] = AlertaCiudadano.objects.filter(activa=True).count()
        
        # Actividad del mes
        inicio_mes = hoy.replace(day=1)
        context["registros_mes"] = LegajoAtencion.objects.filter(fecha_apertura__gte=inicio_mes).count()
        
        # Usuarios activos (últimas 24 horas)
        hace_24h = timezone.now() - timedelta(hours=24)
        context["usuarios_activos"] = User.objects.filter(last_login__gte=hace_24h).count()
        
        # Actividad de hoy para mostrar en el dashboard
        context["actividad_hoy"] = context["seguimientos_hoy"]
        
        return context