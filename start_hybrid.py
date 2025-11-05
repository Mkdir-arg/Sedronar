#!/usr/bin/env python3
"""
Script para iniciar arquitectura híbrida Gunicorn + Daphne
"""
import subprocess
import sys
import os

def start_hybrid():
    """Inicia la arquitectura híbrida"""
    print("🚀 Iniciando SEDRONAR con arquitectura híbrida...")
    print("📡 Gunicorn (HTTP) + Daphne (WebSockets) + Nginx")
    
    try:
        # Detener contenedores existentes
        print("\n🛑 Deteniendo contenedores existentes...")
        subprocess.run(["docker-compose", "down"], check=False)
        
        # Iniciar arquitectura híbrida
        print("\n🔄 Iniciando arquitectura híbrida...")
        result = subprocess.run([
            "docker-compose", 
            "-f", "docker-compose.hybrid.yml", 
            "up", "-d"
        ], check=True)
        
        print("\n✅ Sistema iniciado exitosamente!")
        print("\n📊 Servicios disponibles:")
        print("   🌐 Aplicación: http://localhost:9000")
        print("   🔗 HTTP Backend: http://localhost:8000")
        print("   📡 WebSocket Backend: ws://localhost:8001")
        print("   🗄️  MySQL: localhost:3307")
        print("   🔴 Redis: localhost:6379")
        
        print("\n🔍 Para ver logs:")
        print("   docker-compose -f docker-compose.hybrid.yml logs -f")
        
        print("\n🛠️  Para detener:")
        print("   docker-compose -f docker-compose.hybrid.yml down")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error iniciando sistema: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Operación cancelada por el usuario")
        sys.exit(1)

if __name__ == "__main__":
    start_hybrid()