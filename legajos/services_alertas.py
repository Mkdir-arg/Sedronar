from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q, Count
from .models import (
    AlertaCiudadano, LegajoAtencion, Ciudadano, EvaluacionInicial,
    PlanIntervencion, EventoCritico, Derivacion, Consentimiento
)
from .models_contactos import HistorialContacto, VinculoFamiliar


class AlertasService:
    """Servicio para generar y gestionar alertas automáticas"""
    
    @staticmethod
    def generar_alertas_ciudadano(ciudadano_id):
        """Genera todas las alertas para un ciudadano específico"""
        try:
            ciudadano = Ciudadano.objects.get(id=ciudadano_id)
            legajos = LegajoAtencion.objects.filter(ciudadano=ciudadano)
            
            # Limpiar alertas existentes no críticas
            AlertaCiudadano.objects.filter(
                ciudadano=ciudadano,
                activa=True,
                prioridad__in=['MEDIA', 'BAJA']
            ).update(activa=False)
            
            alertas_generadas = []
            
            for legajo in legajos:
                alertas_generadas.extend(AlertasService._generar_alertas_legajo(legajo))
            
            # Alertas generales del ciudadano
            alertas_generadas.extend(AlertasService._generar_alertas_generales(ciudadano))
            
            return alertas_generadas
            
        except Exception as e:
            print(f"Error generando alertas: {e}")
            return []
    
    @staticmethod
    def _generar_alertas_legajo(legajo):
        """Genera alertas específicas de un legajo"""
        alertas = []
        
        # 1. Riesgo Alto
        if legajo.nivel_riesgo == 'ALTO':
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'RIESGO_ALTO', 'ALTA',
                f'Legajo con nivel de riesgo alto'
            ))
        
        # 2. Sin Evaluación Inicial
        if not hasattr(legajo, 'evaluacion'):
            dias_sin_eval = (timezone.now().date() - legajo.fecha_apertura).days
            if dias_sin_eval > 15:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'SIN_EVALUACION', 'MEDIA',
                    f'Sin evaluación inicial hace {dias_sin_eval} días'
                ))
        
        # 3. Evaluación con riesgos
        try:
            evaluacion = legajo.evaluacion
            if evaluacion.riesgo_suicida:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'RIESGO_SUICIDA', 'CRITICA',
                    'Riesgo suicida identificado en evaluación'
                ))
            if evaluacion.violencia:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'VIOLENCIA', 'CRITICA',
                    'Situación de violencia identificada'
                ))
        except:
            pass
        
        # 4. Sin Plan de Intervención
        if legajo.estado in ['ABIERTO', 'EN_SEGUIMIENTO'] and not legajo.plan_vigente:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'SIN_PLAN', 'MEDIA',
                'Legajo activo sin plan de intervención'
            ))
        
        # 5. Sin Contacto Prolongado
        ultimo_contacto = HistorialContacto.objects.filter(
            legajo=legajo
        ).order_by('-fecha_contacto').first()
        
        if ultimo_contacto:
            dias_sin_contacto = (timezone.now().date() - ultimo_contacto.fecha_contacto.date()).days
            if dias_sin_contacto > 30:
                alertas.append(AlertasService._crear_alerta(
                    legajo.ciudadano, legajo, 'SIN_CONTACTO', 'ALTA',
                    f'Sin contacto hace {dias_sin_contacto} días'
                ))
        
        # 6. Contactos Fallidos
        contactos_fallidos = HistorialContacto.objects.filter(
            legajo=legajo,
            estado='NO_CONTESTA',
            fecha_contacto__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        if contactos_fallidos >= 3:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'CONTACTOS_FALLIDOS', 'MEDIA',
                f'{contactos_fallidos} contactos fallidos en el último mes'
            ))
        
        # 7. Eventos Críticos Recientes
        eventos_recientes = EventoCritico.objects.filter(
            legajo=legajo,
            creado__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        if eventos_recientes > 0:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'EVENTO_CRITICO', 'CRITICA',
                f'{eventos_recientes} evento(s) crítico(s) en la última semana'
            ))
        
        # 8. Derivaciones Pendientes
        derivaciones_pendientes = Derivacion.objects.filter(
            legajo=legajo,
            estado='PENDIENTE',
            creado__lte=timezone.now() - timedelta(days=7)
        ).count()
        
        if derivaciones_pendientes > 0:
            alertas.append(AlertasService._crear_alerta(
                legajo.ciudadano, legajo, 'DERIVACION_PENDIENTE', 'MEDIA',
                f'{derivaciones_pendientes} derivación(es) pendiente(s)'
            ))
        
        return alertas
    
    @staticmethod
    def _generar_alertas_generales(ciudadano):
        """Genera alertas generales del ciudadano"""
        alertas = []
        
        # 1. Sin Red Familiar
        vinculos = VinculoFamiliar.objects.filter(
            ciudadano_principal=ciudadano,
            activo=True
        ).count()
        
        if vinculos == 0:
            alertas.append(AlertasService._crear_alerta(
                ciudadano, None, 'SIN_RED_FAMILIAR', 'BAJA',
                'Sin vínculos familiares registrados'
            ))
        
        # 2. Sin Consentimiento
        consentimiento_vigente = Consentimiento.objects.filter(
            ciudadano=ciudadano,
            vigente=True
        ).exists()
        
        if not consentimiento_vigente:
            alertas.append(AlertasService._crear_alerta(
                ciudadano, None, 'SIN_CONSENTIMIENTO', 'MEDIA',
                'Sin consentimiento informado vigente'
            ))
        
        return alertas
    
    @staticmethod
    def _crear_alerta(ciudadano, legajo, tipo, prioridad, mensaje):
        """Crea una alerta si no existe una similar activa"""
        alerta_existente = AlertaCiudadano.objects.filter(
            ciudadano=ciudadano,
            legajo=legajo,
            tipo=tipo,
            activa=True
        ).first()
        
        if not alerta_existente:
            return AlertaCiudadano.objects.create(
                ciudadano=ciudadano,
                legajo=legajo,
                tipo=tipo,
                prioridad=prioridad,
                mensaje=mensaje
            )
        
        return alerta_existente
    
    @staticmethod
    def obtener_alertas_ciudadano(ciudadano_id):
        """Obtiene todas las alertas activas de un ciudadano"""
        return AlertaCiudadano.objects.filter(
            ciudadano_id=ciudadano_id,
            activa=True
        ).order_by('prioridad', '-creado')
    
    @staticmethod
    def cerrar_alerta(alerta_id, usuario=None):
        """Cierra una alerta específica"""
        try:
            alerta = AlertaCiudadano.objects.get(id=alerta_id, activa=True)
            alerta.cerrar(usuario)
            return True
        except AlertaCiudadano.DoesNotExist:
            return False