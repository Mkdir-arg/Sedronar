from django.db.models import Q
from django.contrib.auth.models import User
from .models import AlertaCiudadano, LegajoAtencion
from users.models import Profile


class FiltrosUsuarioService:
    """Servicio para filtrar alertas según el usuario y sus permisos"""
    
    @staticmethod
    def obtener_alertas_usuario(usuario):
        """
        Obtiene las alertas que corresponden a un usuario específico
        basándose en sus permisos y asignaciones
        """
        if not usuario or not usuario.is_authenticated:
            return AlertaCiudadano.objects.none()
        
        # Superusuarios ven todas las alertas
        if usuario.is_superuser:
            return AlertaCiudadano.objects.filter(activa=True)
        
        # Construir filtros según el rol del usuario
        filtros = Q()
        
        # 1. Alertas de legajos donde el usuario es responsable
        legajos_responsable = LegajoAtencion.objects.filter(responsable=usuario).select_related('dispositivo')
        if legajos_responsable.exists():
            filtros |= Q(legajo__in=legajos_responsable)
        
        # 2. Alertas de legajos del mismo dispositivo del usuario
        try:
            profile = usuario.profile
            if profile.es_usuario_provincial:
                # Usuarios provinciales ven alertas de su provincia
                legajos_provincia = LegajoAtencion.objects.filter(
                    dispositivo__provincia=profile.provincia
                ).select_related('dispositivo')
                filtros |= Q(legajo__in=legajos_provincia)
            else:
                # Usuarios de dispositivo ven alertas de su dispositivo
                # Buscar dispositivo del usuario (puede estar en diferentes modelos)
                dispositivo_usuario = FiltrosUsuarioService._obtener_dispositivo_usuario(usuario)
                if dispositivo_usuario:
                    legajos_dispositivo = LegajoAtencion.objects.filter(
                        dispositivo=dispositivo_usuario
                    ).select_related('dispositivo')
                    filtros |= Q(legajo__in=legajos_dispositivo)
        except Profile.DoesNotExist:
            pass
        
        # 3. Verificar grupos del usuario para permisos adicionales
        grupos_usuario = usuario.groups.values_list('name', flat=True)
        
        if 'Administrador' in grupos_usuario:
            # Administradores ven todas las alertas
            return AlertaCiudadano.objects.filter(activa=True)
        
        elif 'Supervisor' in grupos_usuario:
            # Supervisores ven alertas de su provincia o región
            try:
                profile = usuario.profile
                if profile.provincia:
                    legajos_supervision = LegajoAtencion.objects.filter(
                        dispositivo__provincia=profile.provincia
                    ).select_related('dispositivo')
                    filtros |= Q(legajo__in=legajos_supervision)
            except Profile.DoesNotExist:
                pass
        
        # Si no hay filtros específicos, mostrar solo alertas críticas generales
        if not filtros:
            filtros = Q(prioridad='CRITICA')
        
        return AlertaCiudadano.objects.filter(filtros, activa=True)
    
    @staticmethod
    def _obtener_dispositivo_usuario(usuario):
        """
        Intenta obtener el dispositivo asociado al usuario
        """
        # Buscar en diferentes posibles relaciones
        
        # 1. Como responsable de legajos
        legajo_responsable = LegajoAtencion.objects.filter(responsable=usuario).select_related('dispositivo').first()
        if legajo_responsable:
            return legajo_responsable.dispositivo
        
        # 2. Como profesional en seguimientos
        try:
            from .models import Profesional, SeguimientoContacto
            profesional = Profesional.objects.get(usuario=usuario)
            seguimiento = SeguimientoContacto.objects.filter(profesional=profesional).select_related('legajo__dispositivo').first()
            if seguimiento:
                return seguimiento.legajo.dispositivo
        except:
            pass
        
        # 3. Buscar en configuraciones adicionales (si existen)
        # Aquí se pueden agregar más lógicas según la estructura del sistema
        
        return None
    
    @staticmethod
    def puede_ver_alerta(usuario, alerta):
        """
        Verifica si un usuario específico puede ver una alerta específica
        """
        if not usuario or not usuario.is_authenticated:
            return False
        
        if usuario.is_superuser:
            return True
        
        # Verificar si la alerta está en las alertas permitidas para el usuario
        alertas_usuario = FiltrosUsuarioService.obtener_alertas_usuario(usuario)
        return alertas_usuario.filter(id=alerta.id).exists()
    
    @staticmethod
    def obtener_estadisticas_usuario(usuario):
        """
        Obtiene estadísticas de alertas para un usuario específico
        """
        alertas_usuario = FiltrosUsuarioService.obtener_alertas_usuario(usuario)
        
        return {
            'total': alertas_usuario.count(),
            'criticas': alertas_usuario.filter(prioridad='CRITICA').count(),
            'altas': alertas_usuario.filter(prioridad='ALTA').count(),
            'medias': alertas_usuario.filter(prioridad='MEDIA').count(),
            'bajas': alertas_usuario.filter(prioridad='BAJA').count(),
        }