#!/usr/bin/env python
"""
Script para probar el sistema de alertas
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from legajos.models import Ciudadano, LegajoAtencion, AlertaCiudadano
from legajos.services_alertas import AlertasService
from django.contrib.auth.models import User
from core.models import Institucion

def crear_alertas_prueba():
    """Crea alertas de prueba para verificar el sistema"""
    
    print("🔍 Verificando alertas existentes...")
    alertas_existentes = AlertaCiudadano.objects.filter(activa=True).count()
    print(f"Alertas activas encontradas: {alertas_existentes}")
    
    if alertas_existentes == 0:
        print("📝 Creando alertas de prueba...")
        
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
            print(f"✅ Ciudadano creado: {ciudadano}")
        else:
            print(f"✅ Ciudadano encontrado: {ciudadano}")
        
        # Buscar institución
        institucion = Institucion.objects.first()
        if not institucion:
            print("❌ No hay instituciones disponibles")
            return
        
        # Buscar o crear legajo
        legajo, created = LegajoAtencion.objects.get_or_create(
            ciudadano=ciudadano,
            dispositivo=institucion,
            defaults={
                'via_ingreso': 'ESPONTANEA',
                'nivel_riesgo': 'ALTO'
            }
        )
        
        if created:
            print(f"✅ Legajo creado: {legajo}")
        else:
            print(f"✅ Legajo encontrado: {legajo}")
        
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
            print(f"✅ Alerta creada: {alerta.get_tipo_display()} - {alerta.prioridad}")
    
    # Mostrar resumen
    print("\n📊 Resumen de alertas:")
    alertas = AlertaCiudadano.objects.filter(activa=True)
    
    for prioridad in ['CRITICA', 'ALTA', 'MEDIA', 'BAJA']:
        count = alertas.filter(prioridad=prioridad).count()
        if count > 0:
            print(f"  {prioridad}: {count} alertas")
    
    print(f"\n🎯 Total de alertas activas: {alertas.count()}")
    
    # Probar API
    print("\n🔗 Probando endpoints:")
    print("  - GET /api/legajos/alertas/ (lista de alertas)")
    print("  - GET /api/legajos/alertas/count/ (contador)")
    print("  - GET /legajos/alertas/count/ (contador AJAX)")
    
    return alertas.count()

if __name__ == '__main__':
    try:
        count = crear_alertas_prueba()
        print(f"\n✅ Sistema de alertas configurado correctamente con {count} alertas activas")
        print("\n🚀 Ahora puedes:")
        print("  1. Hacer clic en el icono de campana en el navbar")
        print("  2. Ir a /legajos/alertas/ para ver el dashboard")
        print("  3. Probar la API en /api/legajos/alertas/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()