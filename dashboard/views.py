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
        
        # Datos básicos del sistema (optimizados con una sola consulta)
        from django.db.models import Count, Q
        
        # Consulta optimizada para usuarios
        hace_24h = timezone.now() - timedelta(hours=24)
        user_stats = User.objects.aggregate(
            total_activos=Count('id', filter=Q(is_active=True)),
            activos_24h=Count('id', filter=Q(last_login__gte=hace_24h))
        )
        context["total_usuarios"] = user_stats['total_activos']
        context["usuarios_activos"] = user_stats['activos_24h']
        
        # Consulta optimizada para legajos
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        legajo_stats = LegajoAtencion.objects.aggregate(
            total=Count('id'),
            activos=Count('id', filter=Q(estado__in=['ABIERTO', 'EN_SEGUIMIENTO'])),
            mes=Count('id', filter=Q(fecha_apertura__gte=inicio_mes))
        )
        context["total_legajos"] = legajo_stats['total']
        context["legajos_activos"] = legajo_stats['activos']
        context["registros_mes"] = legajo_stats['mes']
        
        # Consultas optimizadas para actividad
        context["total_ciudadanos"] = Ciudadano.objects.count()
        context["seguimientos_hoy"] = SeguimientoContacto.objects.filter(creado__date=hoy).count()
        context["alertas_activas"] = AlertaCiudadano.objects.filter(activa=True).count()
        
        # Actividad de hoy para mostrar en el dashboard
        context["actividad_hoy"] = context["seguimientos_hoy"]
        
        return context