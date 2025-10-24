from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from dashboard.utils import contar_usuarios, contar_ciudadanos

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Datos básicos del sistema
        context["total_usuarios"] = contar_usuarios()
        context["total_ciudadanos"] = contar_ciudadanos()
        
        return context