from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from legajos.models import Ciudadano, LegajoAtencion, AlertaCiudadano
from core.models import Institucion


class Command(BaseCommand):
    help = 'Crea alertas de prueba para verificar el sistema'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Verificando alertas existentes...")
        
        alertas_existentes = AlertaCiudadano.objects.filter(activa=True).count()
        self.stdout.write(f"Alertas activas encontradas: {alertas_existentes}")
        
        if alertas_existentes == 0:
            self.stdout.write("📝 Creando alertas de prueba...")
            
            # Buscar o crear ciudadano de prueba
            ciudadano, created = Ciudadano.objects.get_or_create(
                dni='12345678',
                defaults={
                    'nombre': 'Juan Carlos',
                    'apellido': 'Pérez',
                    'telefono': '1234567890',
                    'email': 'juan.perez@test.com'
                }
            )
            
            if created:
                self.stdout.write(f"✅ Ciudadano creado: {ciudadano}")
            else:
                self.stdout.write(f"✅ Ciudadano encontrado: {ciudadano}")
            
            # Buscar institución
            institucion = Institucion.objects.first()
            if not institucion:
                self.stdout.write(self.style.ERROR("❌ No hay instituciones disponibles"))
                return
            
            # Buscar un usuario para asignar como responsable
            usuario_responsable = User.objects.filter(is_active=True).first()
            
            # Buscar o crear legajo
            legajo, created = LegajoAtencion.objects.get_or_create(
                ciudadano=ciudadano,
                dispositivo=institucion,
                defaults={
                    'via_ingreso': 'ESPONTANEA',
                    'nivel_riesgo': 'ALTO',
                    'responsable': usuario_responsable
                }
            )
            
            if created:
                self.stdout.write(f"✅ Legajo creado: {legajo}")
            else:
                self.stdout.write(f"✅ Legajo encontrado: {legajo}")
            
            # Crear alertas de prueba
            alertas_prueba = [
                {
                    'tipo': 'RIESGO_ALTO',
                    'prioridad': 'CRITICA',
                    'mensaje': 'Ciudadano con nivel de riesgo crítico - Requiere atención inmediata'
                },
                {
                    'tipo': 'SIN_CONTACTO',
                    'prioridad': 'ALTA',
                    'mensaje': 'Sin contacto hace más de 30 días - Verificar estado'
                },
                {
                    'tipo': 'SIN_EVALUACION',
                    'prioridad': 'MEDIA',
                    'mensaje': 'Legajo sin evaluación inicial hace 20 días'
                }
            ]
            
            for alerta_data in alertas_prueba:
                alerta = AlertaCiudadano.objects.create(
                    ciudadano=ciudadano,
                    legajo=legajo,
                    **alerta_data
                )
                self.stdout.write(f"✅ Alerta creada: {alerta.get_tipo_display()} - {alerta.prioridad}")
        
        # Mostrar resumen
        self.stdout.write("\n📊 Resumen de alertas:")
        alertas = AlertaCiudadano.objects.filter(activa=True)
        
        for prioridad in ['CRITICA', 'ALTA', 'MEDIA', 'BAJA']:
            count = alertas.filter(prioridad=prioridad).count()
            if count > 0:
                self.stdout.write(f"  {prioridad}: {count} alertas")
        
        total = alertas.count()
        self.stdout.write(f"\n🎯 Total de alertas activas: {total}")
        
        if total > 0:
            self.stdout.write(self.style.SUCCESS("\n✅ Sistema de alertas configurado correctamente"))
            self.stdout.write("\n🚀 Ahora puedes:")
            self.stdout.write("  1. Hacer clic en el icono de campana en el navbar")
            self.stdout.write("  2. Ir a /legajos/alertas/ para ver el dashboard")
            self.stdout.write("  3. Probar los endpoints:")
            self.stdout.write("     - /legajos/alertas/count/")
            self.stdout.write("     - /legajos/alertas/preview/")
        else:
            self.stdout.write(self.style.WARNING("⚠️ No se crearon alertas"))