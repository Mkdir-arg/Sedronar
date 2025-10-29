from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from datetime import datetime, timedelta

from .models_contactos import (
    HistorialContacto, VinculoFamiliar, ProfesionalTratante,
    DispositivoVinculado, ContactoEmergencia
)
from .serializers_contactos import (
    HistorialContactoSerializer, HistorialContactoListSerializer,
    VinculoFamiliarSerializer, ProfesionalTratanteSerializer,
    DispositivoVinculadoSerializer, ContactoEmergenciaSerializer,
    CiudadanoBasicoSerializer, UserBasicoSerializer
)
from .models import Ciudadano
from django.contrib.auth.models import User


class HistorialContactoViewSet(viewsets.ModelViewSet):
    queryset = HistorialContacto.objects.select_related(
        'legajo__ciudadano', 'profesional'
    ).all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo_contacto', 'estado', 'seguimiento_requerido', 'profesional']
    search_fields = ['motivo', 'resumen', 'legajo__ciudadano__nombre', 'legajo__ciudadano__apellido']
    ordering_fields = ['fecha_contacto', 'creado']
    ordering = ['-fecha_contacto']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return HistorialContactoListSerializer
        return HistorialContactoSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        legajo_id = self.request.query_params.get('legajo', None)
        if legajo_id:
            queryset = queryset.filter(legajo_id=legajo_id)
        
        fecha_desde = self.request.query_params.get('fecha_desde', None)
        fecha_hasta = self.request.query_params.get('fecha_hasta', None)
        
        if fecha_desde:
            queryset = queryset.filter(fecha_contacto__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_contacto__date__lte=fecha_hasta)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Estadísticas de contactos"""
        queryset = self.get_queryset()
        
        stats = {
            'total_contactos': queryset.count(),
            'por_tipo': dict(queryset.values_list('tipo_contacto').annotate(Count('id'))),
            'por_estado': dict(queryset.values_list('estado').annotate(Count('id'))),
            'pendientes_seguimiento': queryset.filter(seguimiento_requerido=True).count(),
            'ultimo_mes': queryset.filter(
                fecha_contacto__gte=datetime.now() - timedelta(days=30)
            ).count()
        }
        
        return Response(stats)


class VinculoFamiliarViewSet(viewsets.ModelViewSet):
    queryset = VinculoFamiliar.objects.select_related(
        'ciudadano_principal', 'ciudadano_vinculado'
    ).all()
    serializer_class = VinculoFamiliarSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tipo_vinculo', 'es_contacto_emergencia', 'es_referente_tratamiento', 'activo']
    search_fields = ['ciudadano_principal__nombre', 'ciudadano_vinculado__nombre']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        ciudadano_id = self.request.query_params.get('ciudadano', None)
        if ciudadano_id:
            queryset = queryset.filter(
                Q(ciudadano_principal_id=ciudadano_id) | 
                Q(ciudadano_vinculado_id=ciudadano_id)
            )
        return queryset
    
    @action(detail=False, methods=['get'])
    def buscar_ciudadanos(self, request):
        """Buscar ciudadanos para vincular"""
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response([])
        
        ciudadanos = Ciudadano.objects.filter(
            Q(nombre__icontains=query) | 
            Q(apellido__icontains=query) |
            Q(dni__icontains=query)
        )[:10]
        
        serializer = CiudadanoBasicoSerializer(ciudadanos, many=True)
        return Response(serializer.data)


class ProfesionalTratanteViewSet(viewsets.ModelViewSet):
    queryset = ProfesionalTratante.objects.select_related(
        'usuario', 'dispositivo', 'legajo__ciudadano'
    ).all()
    serializer_class = ProfesionalTratanteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['rol', 'es_responsable_principal', 'activo', 'dispositivo']
    search_fields = ['usuario__first_name', 'usuario__last_name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        legajo_id = self.request.query_params.get('legajo', None)
        if legajo_id:
            queryset = queryset.filter(legajo_id=legajo_id)
        return queryset
    
    @action(detail=False, methods=['get'])
    def buscar_usuarios(self, request):
        """Buscar usuarios para asignar como profesionales"""
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response([])
        
        usuarios = User.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(username__icontains=query)
        ).filter(is_active=True)[:10]
        
        serializer = UserBasicoSerializer(usuarios, many=True)
        return Response(serializer.data)


class DispositivoVinculadoViewSet(viewsets.ModelViewSet):
    queryset = DispositivoVinculado.objects.select_related(
        'dispositivo', 'referente_dispositivo', 'legajo__ciudadano'
    ).all()
    serializer_class = DispositivoVinculadoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'dispositivo']
    search_fields = ['dispositivo__nombre']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        legajo_id = self.request.query_params.get('legajo', None)
        if legajo_id:
            queryset = queryset.filter(legajo_id=legajo_id)
        return queryset


class ContactoEmergenciaViewSet(viewsets.ModelViewSet):
    queryset = ContactoEmergencia.objects.select_related('legajo__ciudadano').all()
    serializer_class = ContactoEmergenciaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['disponibilidad_24hs', 'activo']
    search_fields = ['nombre', 'relacion']
    ordering = ['prioridad']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        legajo_id = self.request.query_params.get('legajo', None)
        if legajo_id:
            queryset = queryset.filter(legajo_id=legajo_id)
        return queryset