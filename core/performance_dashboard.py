from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
from django.utils import timezone
from datetime import timedelta
from .performance_analyzer import PerformanceAnalyzer
import json

def is_admin(user):
    return user.is_superuser or user.groups.filter(name__in=['Administrador', 'Ciudadanos']).exists()

@login_required
@user_passes_test(is_admin)
def performance_dashboard(request):
    """Performance monitoring dashboard"""
    return render(request, 'core/performance_dashboard.html')

from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    description="API para obtener métricas de performance en tiempo real",
    responses={200: 'Métricas de performance del sistema'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def performance_api(request):
    """API endpoint for performance data"""
    from config.middlewares.query_counter import QueryCountMiddleware
    
    # Get session stats from middleware
    session_stats = QueryCountMiddleware.get_session_stats()
    
    analyzer = PerformanceAnalyzer()
    report = analyzer.generate_report()
    
    # Override with session data
    report.update({
        'total_queries': session_stats['total_queries'],
        'total_requests': session_stats['total_requests'],
        'slow_requests': session_stats['slow_requests'],
        'n1_detected': session_stats['n1_detected_count'] > 0,
        'similar_queries': session_stats['n1_detected_count'],
        'performance_score': max(20, 100 - min(50, session_stats['slow_requests'] * 5) - min(30, session_stats['n1_detected_count'] * 3)),
        'real_time': {
            'active_connections': session_stats['total_requests'],
            'timestamp': timezone.now().isoformat(),
            'memory_usage': _get_memory_usage(),
            'session_start': session_stats['last_reset'].isoformat(),
        }
    })
    
    return JsonResponse(report)

@extend_schema(
    description="API para análisis detallado de patrones de consultas",
    responses={200: 'Análisis de patrones de queries'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def query_analysis_api(request):
    """Detailed query analysis API"""
    queries = connection.queries[-100:]  # Last 100 queries
    analyzer = PerformanceAnalyzer()
    
    analysis = {
        'query_count': len(queries),
        'patterns': analyzer.analyze_queries(queries),
        'slow_queries': analyzer.get_slow_queries(queries),
        'recommendations': []
    }
    
    # Generate specific recommendations
    if analysis['patterns']['n1_detected']:
        analysis['recommendations'].append({
            'priority': 'high',
            'type': 'N+1 Detection',
            'message': f"Detected {analysis['patterns']['similar_queries']} similar queries. Consider using select_related() or prefetch_related().",
            'action': 'Review recent code changes and add query optimizations'
        })
    
    if len(analysis['slow_queries']) > 0:
        analysis['recommendations'].append({
            'priority': 'medium',
            'type': 'Slow Queries',
            'message': f"Found {len(analysis['slow_queries'])} slow queries.",
            'action': 'Add database indexes or optimize query logic'
        })
    
    return JsonResponse(analysis)

@extend_schema(
    description="API para obtener sugerencias de optimización",
    responses={200: 'Sugerencias de optimización de performance'}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def optimization_suggestions_api(request):
    """API for optimization suggestions"""
    model_name = request.GET.get('model', '')
    
    suggestions = [
        {
            'category': 'Query Optimization',
            'items': [
                {
                    'title': 'Use select_related()',
                    'description': 'For ForeignKey relationships to reduce queries',
                    'example': f'{model_name}.objects.select_related("foreign_key_field")',
                    'impact': 'High'
                },
                {
                    'title': 'Use prefetch_related()',
                    'description': 'For reverse relationships and ManyToMany fields',
                    'example': f'{model_name}.objects.prefetch_related("reverse_field")',
                    'impact': 'High'
                },
                {
                    'title': 'Use only() for field limitation',
                    'description': 'When you only need specific fields',
                    'example': f'{model_name}.objects.only("field1", "field2")',
                    'impact': 'Medium'
                }
            ]
        }
    ]
    
    return JsonResponse({'suggestions': suggestions})

def _get_memory_usage():
    """Get current memory usage (simplified)"""
    try:
        import psutil
        process = psutil.Process()
        return {
            'memory_percent': process.memory_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024
        }
    except ImportError:
        return {'memory_percent': 0, 'memory_mb': 0}