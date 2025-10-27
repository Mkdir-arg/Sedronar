from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import (
    Provincia, Municipio, Localidad, DispositivoRed, Sexo, Mes, Dia, Turno
)
from .serializers import (
    ProvinciaSerializer, MunicipioSerializer, LocalidadSerializer,
    DispositivoRedSerializer, SexoSerializer, MesSerializer, 
    DiaSerializer, TurnoSerializer
)


@extend_schema_view(
    list=extend_schema(description="Lista todas las provincias"),
    create=extend_schema(description="Crea una nueva provincia"),
    retrieve=extend_schema(description="Obtiene una provincia específica"),
    update=extend_schema(description="Actualiza una provincia"),
    partial_update=extend_schema(description="Actualiza parcialmente una provincia"),
    destroy=extend_schema(description="Elimina una provincia")
)
class ProvinciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar provincias.
    
    Permite realizar operaciones CRUD sobre las provincias del sistema.
    """
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['nombre']
    ordering = ['nombre']

    @extend_schema(description="Obtiene los municipios de una provincia")
    @action(detail=True, methods=['get'])
    def municipios(self, request, pk=None):
        """Obtiene los municipios de una provincia específica"""
        provincia = self.get_object()
        municipios = provincia.municipio_set.all()
        serializer = MunicipioSerializer(municipios, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description="Lista todos los municipios"),
    create=extend_schema(description="Crea un nuevo municipio"),
    retrieve=extend_schema(description="Obtiene un municipio específico"),
    update=extend_schema(description="Actualiza un municipio"),
    partial_update=extend_schema(description="Actualiza parcialmente un municipio"),
    destroy=extend_schema(description="Elimina un municipio")
)
class MunicipioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar municipios.
    """
    queryset = Municipio.objects.select_related('provincia')
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['provincia']
    search_fields = ['nombre']
    ordering = ['nombre']

    @extend_schema(description="Obtiene las localidades de un municipio")
    @action(detail=True, methods=['get'])
    def localidades(self, request, pk=None):
        """Obtiene las localidades de un municipio específico"""
        municipio = self.get_object()
        localidades = municipio.localidad_set.all()
        serializer = LocalidadSerializer(localidades, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description="Lista todas las localidades"),
    create=extend_schema(description="Crea una nueva localidad"),
    retrieve=extend_schema(description="Obtiene una localidad específica"),
    update=extend_schema(description="Actualiza una localidad"),
    partial_update=extend_schema(description="Actualiza parcialmente una localidad"),
    destroy=extend_schema(description="Elimina una localidad")
)
class LocalidadViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar localidades.
    """
    queryset = Localidad.objects.select_related('municipio__provincia')
    serializer_class = LocalidadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['municipio']
    search_fields = ['nombre']
    ordering = ['nombre']


@extend_schema_view(
    list=extend_schema(description="Lista todos los dispositivos de red"),
    create=extend_schema(description="Crea un nuevo dispositivo de red"),
    retrieve=extend_schema(description="Obtiene un dispositivo específico"),
    update=extend_schema(description="Actualiza un dispositivo"),
    partial_update=extend_schema(description="Actualiza parcialmente un dispositivo"),
    destroy=extend_schema(description="Elimina un dispositivo")
)
class DispositivoRedViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar dispositivos de red SEDRONAR.
    
    Permite realizar operaciones CRUD sobre los dispositivos de la red territorial.
    """
    queryset = DispositivoRed.objects.select_related('provincia', 'municipio', 'localidad')
    serializer_class = DispositivoRedSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tipo', 'activo', 'provincia', 'municipio']
    search_fields = ['nombre', 'nro_registro']
    ordering_fields = ['nombre', 'fecha_alta', 'tipo']
    ordering = ['nombre']

    @extend_schema(description="Activa un dispositivo de red")
    @action(detail=True, methods=['post'])
    def activar(self, request, pk=None):
        """Activa un dispositivo de red"""
        dispositivo = self.get_object()
        dispositivo.activo = True
        dispositivo.save()
        return Response({'status': 'Dispositivo activado'})

    @extend_schema(description="Desactiva un dispositivo de red")
    @action(detail=True, methods=['post'])
    def desactivar(self, request, pk=None):
        """Desactiva un dispositivo de red"""
        dispositivo = self.get_object()
        dispositivo.activo = False
        dispositivo.save()
        return Response({'status': 'Dispositivo desactivado'})


@extend_schema_view(
    list=extend_schema(description="Lista todos los sexos"),
    retrieve=extend_schema(description="Obtiene un sexo específico")
)
class SexoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para sexos.
    """
    queryset = Sexo.objects.all()
    serializer_class = SexoSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(description="Lista todos los meses"),
    retrieve=extend_schema(description="Obtiene un mes específico")
)
class MesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para meses.
    """
    queryset = Mes.objects.all()
    serializer_class = MesSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(description="Lista todos los días"),
    retrieve=extend_schema(description="Obtiene un día específico")
)
class DiaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para días.
    """
    queryset = Dia.objects.all()
    serializer_class = DiaSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(description="Lista todos los turnos"),
    retrieve=extend_schema(description="Obtiene un turno específico")
)
class TurnoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para turnos.
    """
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    permission_classes = [IsAuthenticated]