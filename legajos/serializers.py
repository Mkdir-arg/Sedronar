from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Ciudadano, LegajoAtencion, EvaluacionInicial, 
    PlanIntervencion, SeguimientoContacto, Derivacion, 
    EventoCritico, Profesional
)
from core.models import DispositivoRed


class CiudadanoSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Ciudadano"""
    
    class Meta:
        model = Ciudadano
        fields = [
            'id', 'dni', 'nombre', 'apellido', 'fecha_nacimiento',
            'genero', 'telefono', 'email', 'domicilio', 'activo',
            'creado', 'modificado'
        ]
        read_only_fields = ['id', 'creado', 'modificado']


class DispositivoRedSerializer(serializers.ModelSerializer):
    """Serializer para DispositivoRed"""
    
    class Meta:
        model = DispositivoRed
        fields = ['id', 'nombre', 'tipo', 'activo']


class UserSerializer(serializers.ModelSerializer):
    """Serializer básico para User"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProfesionalSerializer(serializers.ModelSerializer):
    """Serializer para Profesional"""
    usuario = UserSerializer(read_only=True)
    
    class Meta:
        model = Profesional
        fields = ['id', 'usuario', 'matricula', 'rol']


class LegajoAtencionSerializer(serializers.ModelSerializer):
    """Serializer para LegajoAtencion"""
    ciudadano = CiudadanoSerializer(read_only=True)
    dispositivo = DispositivoRedSerializer(read_only=True)
    responsable = UserSerializer(read_only=True)
    
    class Meta:
        model = LegajoAtencion
        fields = [
            'id', 'codigo', 'ciudadano', 'dispositivo', 'responsable',
            'via_ingreso', 'fecha_admision', 'estado', 'plan_vigente',
            'nivel_riesgo', 'notas', 'fecha_cierre', 'creado', 'modificado'
        ]
        read_only_fields = ['id', 'codigo', 'creado', 'modificado']


class EvaluacionInicialSerializer(serializers.ModelSerializer):
    """Serializer para EvaluacionInicial"""
    
    class Meta:
        model = EvaluacionInicial
        fields = [
            'id', 'legajo', 'situacion_consumo', 'antecedentes',
            'red_apoyo', 'condicion_social', 'tamizajes',
            'riesgo_suicida', 'violencia', 'creado', 'modificado'
        ]
        read_only_fields = ['id', 'creado', 'modificado']


class PlanIntervencionSerializer(serializers.ModelSerializer):
    """Serializer para PlanIntervencion"""
    profesional = ProfesionalSerializer(read_only=True)
    
    class Meta:
        model = PlanIntervencion
        fields = [
            'id', 'legajo', 'profesional', 'vigente', 'actividades',
            'creado', 'modificado'
        ]
        read_only_fields = ['id', 'creado', 'modificado']


class SeguimientoContactoSerializer(serializers.ModelSerializer):
    """Serializer para SeguimientoContacto"""
    profesional = ProfesionalSerializer(read_only=True)
    
    class Meta:
        model = SeguimientoContacto
        fields = [
            'id', 'legajo', 'profesional', 'tipo', 'descripcion',
            'adherencia', 'adjuntos', 'creado', 'modificado'
        ]
        read_only_fields = ['id', 'creado', 'modificado']


class DerivacionSerializer(serializers.ModelSerializer):
    """Serializer para Derivacion"""
    origen = DispositivoRedSerializer(read_only=True)
    destino = DispositivoRedSerializer(read_only=True)
    
    class Meta:
        model = Derivacion
        fields = [
            'id', 'legajo', 'origen', 'destino', 'motivo', 'urgencia',
            'estado', 'respuesta', 'fecha_aceptacion', 'creado', 'modificado'
        ]
        read_only_fields = ['id', 'creado', 'modificado']


class EventoCriticoSerializer(serializers.ModelSerializer):
    """Serializer para EventoCritico"""
    
    class Meta:
        model = EventoCritico
        fields = [
            'id', 'legajo', 'tipo', 'detalle', 'notificado_a',
            'creado', 'modificado'
        ]
        read_only_fields = ['id', 'creado', 'modificado']