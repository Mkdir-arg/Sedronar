import time
import threading
from django.core.cache import cache
from django.http import HttpResponse

class ConcurrencyLimitMiddleware:
    """Middleware para controlar concurrencia y evitar sobrecarga"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.active_requests = threading.local()
        
    def __call__(self, request):
        # Contador de requests activos
        current_load = cache.get('active_requests', 0)
        
        # Límite de seguridad para evitar colapso
        if current_load > 1500:  # Límite de emergencia
            return HttpResponse(
                "Sistema temporalmente sobrecargado. Intente en unos segundos.",
                status=503
            )
        
        # Incrementar contador
        cache.set('active_requests', current_load + 1, 60)
        
        try:
            response = self.get_response(request)
        finally:
            # Decrementar contador
            current_load = cache.get('active_requests', 1)
            cache.set('active_requests', max(0, current_load - 1), 60)
        
        return response

class RequestMetricsMiddleware:
    """Middleware para métricas de performance en tiempo real"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Calcular tiempo de respuesta
        response_time = time.time() - start_time
        
        # Guardar métricas en cache
        metrics_key = f"metrics:{int(time.time() // 60)}"  # Por minuto
        current_metrics = cache.get(metrics_key, {'count': 0, 'total_time': 0})
        current_metrics['count'] += 1
        current_metrics['total_time'] += response_time
        cache.set(metrics_key, current_metrics, 300)
        
        # Headers de debug
        response['X-Response-Time'] = f"{response_time:.3f}s"
        response['X-Active-Requests'] = cache.get('active_requests', 0)
        
        return response