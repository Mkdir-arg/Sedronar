import psutil
import time
from django.core.cache import cache
from django.db import connection

class SystemMonitor:
    """Monitor de sistema para 1000+ usuarios"""
    
    @staticmethod
    def get_system_metrics():
        """Métricas del sistema"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'active_connections': len(connection.queries),
            'cache_hits': cache.get('cache_hits', 0),
            'timestamp': time.time()
        }
    
    @staticmethod
    def check_capacity():
        """Verifica si el sistema puede manejar más carga"""
        metrics = SystemMonitor.get_system_metrics()
        
        if metrics['cpu_percent'] > 80:
            return {'status': 'warning', 'message': 'CPU alta'}
        if metrics['memory_percent'] > 85:
            return {'status': 'warning', 'message': 'Memoria alta'}
        
        return {'status': 'ok', 'message': 'Sistema estable'}