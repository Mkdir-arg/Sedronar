from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import (
    Ciudadano, LegajoAtencion, EvaluacionInicial,
    PlanIntervencion, SeguimientoContacto, Derivacion, EventoCritico
)
from .serializers import (
    CiudadanoSerializer, LegajoAtencionSerializer, EvaluacionInicialSerializer,
    PlanIntervencionSerializer, SeguimientoContactoSerializer, 
    DerivacionSerializer, EventoCriticoSerializer
)


@extend_schema_view(
    list=extend_schema(description="Lista todos los ciudadanos"),
    create=extend_schema(description="Crea un nuevo ciudadano"),
    retrieve=extend_schema(description="Obtiene un ciudadano específico"),
    update=extend_schema(description="Actualiza un ciudadano"),
    partial_update=extend_schema(description="Actualiza parcialmente un ciudadano"),
    destroy=extend_schema(description="Elimina un ciudadano")
)
class CiudadanoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ciudadanos.
    
    Permite realizar operaciones CRUD sobre los ciudadanos del sistema.
    """
    queryset = Ciudadano.objects.all()
    serializer_class = CiudadanoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dni', 'genero', 'activo']
    search_fields = ['nombre', 'apellido', 'dni']
    ordering_fields = ['apellido', 'nombre', 'creado']
    ordering = ['apellido', 'nombre']


@extend_schema_view(
    list=extend_schema(description="Lista todos los legajos de atención"),
    create=extend_schema(description="Crea un nuevo legajo de atención"),
    retrieve=extend_schema(description="Obtiene un legajo específico"),
    update=extend_schema(description="Actualiza un legajo"),
    partial_update=extend_schema(description="Actualiza parcialmente un legajo"),
    destroy=extend_schema(description="Elimina un legajo")
)
class LegajoAtencionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar legajos de atención.
    
    Permite realizar operaciones CRUD sobre los legajos de atención.
    """
    queryset = LegajoAtencion.objects.select_related('ciudadano', 'dispositivo', 'responsable')
    serializer_class = LegajoAtencionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'nivel_riesgo', 'via_ingreso', 'dispositivo']
    search_fields = ['codigo', 'ciudadano__nombre', 'ciudadano__apellido', 'ciudadano__dni']
    ordering_fields = ['fecha_admision', 'creado']
    ordering = ['-fecha_admision']

    @extend_schema(description="Cierra un legajo de atención")
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """Cierra un legajo de atención"""
        legajo = self.get_object()
        motivo = request.data.get('motivo_cierre', '')
        
        try:
            legajo.cerrar(motivo_cierre=motivo, usuario=request.user)
            return Response({'status': 'Legajo cerrado exitosamente'})
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(description="Reabre un legajo de atención cerrado")
    @action(detail=True, methods=['post'])
    def reabrir(self, request, pk=None):
        """Reabre un legajo de atención"""
        legajo = self.get_object()
        motivo = request.data.get('motivo_reapertura', '')
        
        try:
            legajo.reabrir(motivo_reapertura=motivo, usuario=request.user)
            return Response({'status': 'Legajo reabierto exitosamente'})
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema_view(
    list=extend_schema(description="Lista todas las evaluaciones iniciales"),
    create=extend_schema(description="Crea una nueva evaluación inicial"),
    retrieve=extend_schema(description="Obtiene una evaluación específica"),
    update=extend_schema(description="Actualiza una evaluación"),
    partial_update=extend_schema(description="Actualiza parcialmente una evaluación"),
    destroy=extend_schema(description="Elimina una evaluación")
)
class EvaluacionInicialViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar evaluaciones iniciales.
    """
    queryset = EvaluacionInicial.objects.select_related('legajo')
    serializer_class = EvaluacionInicialSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['riesgo_suicida', 'violencia']


@extend_schema_view(
    list=extend_schema(description="Lista todos los planes de intervención"),
    create=extend_schema(description="Crea un nuevo plan de intervención"),
    retrieve=extend_schema(description="Obtiene un plan específico"),
    update=extend_schema(description="Actualiza un plan"),
    partial_update=extend_schema(description="Actualiza parcialmente un plan"),
    destroy=extend_schema(description="Elimina un plan")
)
class PlanIntervencionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar planes de intervención.
    """
    queryset = PlanIntervencion.objects.select_related('legajo', 'profesional')
    serializer_class = PlanIntervencionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['vigente', 'legajo']


@extend_schema_view(
    list=extend_schema(description="Lista todos los seguimientos"),
    create=extend_schema(description="Crea un nuevo seguimiento"),
    retrieve=extend_schema(description="Obtiene un seguimiento específico"),
    update=extend_schema(description="Actualiza un seguimiento"),
    partial_update=extend_schema(description="Actualiza parcialmente un seguimiento"),
    destroy=extend_schema(description="Elimina un seguimiento")
)
class SeguimientoContactoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar seguimientos de contacto.
    """
    queryset = SeguimientoContacto.objects.select_related('legajo', 'profesional')
    serializer_class = SeguimientoContactoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'adherencia', 'legajo']
    ordering = ['-creado']


@extend_schema_view(
    list=extend_schema(description="Lista todas las derivaciones"),
    create=extend_schema(description="Crea una nueva derivación"),
    retrieve=extend_schema(description="Obtiene una derivación específica"),
    update=extend_schema(description="Actualiza una derivación"),
    partial_update=extend_schema(description="Actualiza parcialmente una derivación"),
    destroy=extend_schema(description="Elimina una derivación")
)
class DerivacionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar derivaciones entre dispositivos.
    """
    queryset = Derivacion.objects.select_related('legajo', 'origen', 'destino')
    serializer_class = DerivacionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['estado', 'urgencia', 'origen', 'destino']
    ordering = ['-creado']


@extend_schema_view(
    list=extend_schema(description="Lista todos los eventos críticos"),
    create=extend_schema(description="Crea un nuevo evento crítico"),
    retrieve=extend_schema(description="Obtiene un evento específico"),
    update=extend_schema(description="Actualiza un evento"),
    partial_update=extend_schema(description="Actualiza parcialmente un evento"),
    destroy=extend_schema(description="Elimina un evento")
)
class EventoCriticoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar eventos críticos.
    """
    queryset = EventoCritico.objects.select_related('legajo')
    serializer_class = EventoCriticoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'legajo']
    ordering = ['-creado']