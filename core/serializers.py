from rest_framework import serializers
from .models import (
    Provincia, Municipio, Localidad, DispositivoRed, Sexo, Mes, Dia, Turno
)


class ProvinciaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Provincia"""
    
    class Meta:
        model = Provincia
        fields = ['id', 'nombre']


class MunicipioSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Municipio"""
    provincia = ProvinciaSerializer(read_only=True)
    provincia_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Municipio
        fields = ['id', 'nombre', 'provincia', 'provincia_id']


class LocalidadSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Localidad"""
    municipio = MunicipioSerializer(read_only=True)
    municipio_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Localidad
        fields = ['id', 'nombre', 'municipio', 'municipio_id']


class DispositivoRedSerializer(serializers.ModelSerializer):
    """Serializer para el modelo DispositivoRed"""
    provincia = ProvinciaSerializer(read_only=True)
    municipio = MunicipioSerializer(read_only=True)
    localidad = LocalidadSerializer(read_only=True)
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = DispositivoRed
        fields = [
            'id', 'tipo', 'tipo_display', 'nombre', 'provincia', 'municipio', 
            'localidad', 'direccion', 'telefono', 'email', 'activo',
            'nro_registro', 'resolucion', 'fecha_alta', 'descripcion',
            'creado', 'modificado'
        ]
        read_only_fields = ['id', 'fecha_alta', 'creado', 'modificado']


class SexoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Sexo"""
    
    class Meta:
        model = Sexo
        fields = ['id', 'sexo']


class MesSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Mes"""
    
    class Meta:
        model = Mes
        fields = ['id', 'nombre']


class DiaSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Dia"""
    
    class Meta:
        model = Dia
        fields = ['id', 'nombre']


class TurnoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Turno"""
    
    class Meta:
        model = Turno
        fields = ['id', 'nombre']