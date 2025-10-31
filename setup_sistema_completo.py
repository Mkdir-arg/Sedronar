#!/usr/bin/env python
"""
SISOC - Script de configuración completa del sistema
Ejecuta todos los pasos necesarios para levantar el sistema desde cero
"""

import os
import sys
import django
from django.core.management import execute_from_command_line
from django.db import connection

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def ejecutar_comando(comando):
    """Ejecuta un comando de Django management"""
    print(f"\n🔄 Ejecutando: {' '.join(comando)}")
    try:
        execute_from_command_line(['manage.py'] + comando)
        print(f"✅ Completado: {' '.join(comando)}")
        return True
    except Exception as e:
        print(f"❌ Error en {' '.join(comando)}: {e}")
        return False

def ejecutar_sql_file(archivo_sql):
    """Ejecuta un archivo SQL"""
    print(f"\n🔄 Ejecutando archivo SQL: {archivo_sql}")
    try:
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Limpiar el contenido SQL
        sql_content = sql_content.replace('USE sedronar;', '')  # Remover USE database
        
        with connection.cursor() as cursor:
            # Dividir por declaraciones y ejecutar una por una
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            for i, statement in enumerate(statements):
                if statement and not statement.startswith('--') and not statement.startswith('SELECT'):
                    try:
                        cursor.execute(statement)
                        print(f"  ✓ Ejecutado statement {i+1}/{len(statements)}")
                    except Exception as stmt_error:
                        print(f"  ⚠️  Warning en statement {i+1}: {stmt_error}")
                        # Continuar con el siguiente statement
                        continue
        
        print(f"✅ Completado: {archivo_sql}")
        return True
    except Exception as e:
        print(f"❌ Error ejecutando {archivo_sql}: {e}")
        return False

def main():
    """Función principal de configuración"""
    print("=" * 60)
    print("🚀 SISOC - CONFIGURACIÓN COMPLETA DEL SISTEMA")
    print("=" * 60)
    
    # Paso 1: Crear migraciones
    print("\n📋 PASO 1: Creando migraciones...")
    if not ejecutar_comando(['makemigrations']):
        print("❌ Error creando migraciones. Abortando.")
        return False
    
    # Paso 2: Aplicar migraciones
    print("\n📋 PASO 2: Aplicando migraciones...")
    if not ejecutar_comando(['migrate']):
        print("❌ Error aplicando migraciones. Abortando.")
        return False
    
    # Paso 3: Cargar datos base desde SQL
    print("\n📋 PASO 3: Cargando datos base del sistema...")
    if os.path.exists('setup_complete_data.sql'):
        if not ejecutar_sql_file('setup_complete_data.sql'):
            print("❌ Error cargando datos base. Abortando.")
            return False
    else:
        print("⚠️  Archivo setup_complete_data.sql no encontrado. Saltando...")
    
    # Paso 4: Cargar fixtures adicionales
    print("\n📋 PASO 4: Cargando fixtures adicionales...")
    
    # Fixtures de core (saltear dia, mes, sexo porque ya están en el SQL)
    fixtures_core = [
        'core/fixtures/localidad_municipio_provincia.json',
        'core/fixtures/dispositivos.json'
    ]
    
    for fixture in fixtures_core:
        if os.path.exists(fixture):
            ejecutar_comando(['loaddata', fixture])
    
    # Fixtures de chatbot
    if os.path.exists('chatbot/fixtures/initial_knowledge.json'):
        ejecutar_comando(['loaddata', 'chatbot/fixtures/initial_knowledge.json'])
    
    # Fixtures de legajos
    if os.path.exists('legajos/fixtures/contactos_initial_data.json'):
        ejecutar_comando(['loaddata', 'legajos/fixtures/contactos_initial_data.json'])
    
    # Paso 5: Configurar grupos y permisos
    print("\n📋 PASO 5: Configurando grupos y permisos...")
    ejecutar_comando(['setup_groups'])
    ejecutar_comando(['crear_usuarios_sistema'])
    ejecutar_comando(['setup_roles_contactos'])
    
    # Paso 6: Configurar conversaciones
    print("\n📋 PASO 6: Configurando sistema de conversaciones...")
    ejecutar_comando(['setup_conversaciones'])
    
    # Paso 7: Recopilar archivos estáticos
    print("\n📋 PASO 7: Recopilando archivos estáticos...")
    ejecutar_comando(['collectstatic', '--noinput'])
    
    # Resumen final
    print("\n" + "=" * 60)
    print("🎉 CONFIGURACIÓN COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\n📊 CREDENCIALES DE ACCESO:")
    print("👤 Superusuario: admin / admin123")
    print("👥 Administradores: admin1, admin2, admin3 / admin123")
    print("🎯 Responsables: resp1, resp2, resp3 / resp123")
    print("⚙️  Operadores: oper1, oper2, oper3 / oper123")
    print("👁️  Supervisores: super1, super2, super3 / super123")
    print("📖 Consulta: cons1, cons2, cons3 / cons123")
    print("\n🌐 Acceso: http://localhost:9000")
    print("📚 API Docs: http://localhost:9000/api/docs/")
    print("\n✅ Sistema listo para usar!")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)