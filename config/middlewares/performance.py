import time
from django.core.cache import cache
from django.http import HttpResponse

class PerformanceMiddleware:
    """Middleware para optimizaciones de performance"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        
        # ETags para cache del navegador
        if request.method == 'GET':
            etag = cache.get(f"etag:{request.path}")
            if etag and request.META.get('HTTP_IF_NONE_MATCH') == etag:
                return HttpResponse(status=304)
        
        response = self.get_response(request)
        
        # Agregar headers de performance
        if hasattr(response, 'status_code') and response.status_code == 200:
            processing_time = time.time() - start_time
            response['X-Processing-Time'] = f"{processing_time:.3f}s"
            
            # Cache control para recursos estáticos
            if request.path.startswith('/static/'):
                response['Cache-Control'] = 'public, max-age=31536000'  # 1 año
            elif request.path.startswith('/media/'):
                response['Cache-Control'] = 'public, max-age=86400'  # 1 día
            
            # ETag para páginas dinámicas
            if request.method == 'GET' and not request.path.startswith(('/static/', '/media/')):
                etag = f'"{hash(response.content)}"'
                response['ETag'] = etag
                cache.set(f"etag:{request.path}", etag, 300)
        
        return response