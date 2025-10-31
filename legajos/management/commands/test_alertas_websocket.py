from django.core.management.base import BaseCommand
from django.utils import timezone
from legajos.models import Ciudadano, LegajoAtencion, AlertaCiudadano
from legajos.services_alertas import AlertasService
import time


class Command(BaseCommand):
    help = 'Comando para probar el sistema de alertas WebSocket'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ciudadano-id',
            type=int,
            help='ID del ciudadano para generar alertas de prueba'
        )
        parser.add_argument(
            '--crear-alerta-critica',
            action='store_true',
            help='Crear una alerta crítica de prueba'
        )
        parser.add_argument(
            '--test-conversaciones',
            action='store_true',
            help='Probar alertas de conversaciones'
        )
        parser.add_argument(
            '--test-seguimientos',
            action='store_true',
            help='Probar alertas de seguimientos'
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚨 Iniciando prueba del sistema de alertas WebSocket')
        )

        if options['crear_alerta_critica']:
            self.crear_alerta_critica()
        
        if options['test_conversaciones']:
            self.test_alertas_conversaciones()
        
        if options['test_seguimientos']:
            self.test_alertas_seguimientos()
        
        if options['ciudadano_id']:
            self.generar_alertas_ciudadano(options['ciudadano_id'])
        else:
            self.generar_alertas_automaticas()

    def crear_alerta_critica(self):
        """Crea una alerta crítica de prueba"""
        try:
            # Buscar un ciudadano existente
            ciudadano = Ciudadano.objects.first()
            if not ciudadano:
                self.stdout.write(
                    self.style.ERROR('No hay ciudadanos en el sistema')
                )
                return

            # Crear alerta crítica directamente
            alerta = AlertaCiudadano.objects.create(
                ciudadano=ciudadano,
                tipo='RIESGO_SUICIDA',
                prioridad='CRITICA',
                mensaje='ALERTA DE PRUEBA: Riesgo suicida detectado - SIMULACIÓN'
            )

            # Enviar notificación WebSocket
            AlertasService._enviar_notificacion_alerta(alerta)

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Alerta crítica creada para {ciudadano.nombre_completo}'
                )
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creando alerta crítica: {e}')
            )

    def generar_alertas_ciudadano(self, ciudadano_id):
        """Genera alertas para un ciudadano específico"""
        try:
            ciudadano = Ciudadano.objects.get(id=ciudadano_id)
            alertas = AlertasService.generar_alertas_ciudadano(ciudadano_id)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Generadas {len(alertas)} alertas para {ciudadano.nombre_completo}'
                )
            )

            for alerta in alertas:
                self.stdout.write(f'  - {alerta.prioridad}: {alerta.mensaje}')

        except Ciudadano.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Ciudadano con ID {ciudadano_id} no encontrado')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )

    def generar_alertas_automaticas(self):
        """Genera alertas automáticas para todos los ciudadanos con legajos"""
        try:
            ciudadanos_con_legajos = Ciudadano.objects.filter(
                legajos__isnull=False
            ).distinct()[:5]  # Limitar a 5 para prueba

            total_alertas = 0

            for ciudadano in ciudadanos_con_legajos:
                alertas = AlertasService.generar_alertas_ciudadano(ciudadano.id)
                total_alertas += len(alertas)
                
                if alertas:
                    self.stdout.write(
                        f'📋 {ciudadano.nombre_completo}: {len(alertas)} alertas'
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Proceso completado. Total: {total_alertas} alertas generadas'
                )
            )

            # Crear una alerta crítica adicional para demostración
            if ciudadanos_con_legajos.exists():
                time.sleep(2)  # Esperar 2 segundos
                self.crear_alerta_critica()

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error en proceso automático: {e}')
            )

    def mostrar_estadisticas(self):
        """Muestra estadísticas de alertas"""
        total = AlertaCiudadano.objects.filter(activa=True).count()
        criticas = AlertaCiudadano.objects.filter(
            activa=True, 
            prioridad='CRITICA'
        ).count()
        altas = AlertaCiudadano.objects.filter(
            activa=True, 
            prioridad='ALTA'
        ).count()

        self.stdout.write('\n📊 ESTADÍSTICAS DE ALERTAS:')
        self.stdout.write(f'  Total activas: {total}')
        self.stdout.write(f'  Críticas: {criticas}')
        self.stdout.write(f'  Altas: {altas}')
    
    def test_alertas_conversaciones(self):
        """Prueba alertas de conversaciones"""
        try:
            from conversaciones.models import Conversacion, Mensaje
            
            # Crear conversación de prueba
            ciudadano = Ciudadano.objects.first()
            if not ciudadano:
                self.stdout.write(self.style.ERROR('No hay ciudadanos para probar'))
                return
            
            conversacion = Conversacion.objects.create(
                ciudadano_relacionado=ciudadano,
                estado='ACTIVA'
            )
            
            # Crear mensaje de ciudadano
            Mensaje.objects.create(
                conversacion=conversacion,
                remitente='ciudadano',
                contenido='Mensaje de prueba para alertas'
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Alertas de conversaciones probadas')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error probando conversaciones: {e}')
            )
    
    def test_alertas_seguimientos(self):
        """Prueba alertas de seguimientos"""
        try:
            from legajos.models import SeguimientoContacto
            from datetime import date, timedelta
            
            # Buscar legajo existente
            legajo = LegajoAtencion.objects.first()
            if not legajo:
                self.stdout.write(self.style.ERROR('No hay legajos para probar'))
                return
            
            # Crear seguimiento vencido
            SeguimientoContacto.objects.create(
                legajo=legajo,
                tipo='TELEFONICO',
                fecha_proximo_contacto=date.today() - timedelta(days=5),
                adherencia='BAJA',
                observaciones='Seguimiento de prueba vencido'
            )
            
            self.stdout.write(
                self.style.SUCCESS('✅ Alertas de seguimientos probadas')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error probando seguimientos: {e}')
            )