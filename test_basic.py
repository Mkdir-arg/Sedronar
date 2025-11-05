#!/usr/bin/env python3
"""
Prueba básica de conectividad
"""
import requests
import time

def test_basic_connection():
    """Prueba básica de conexión"""
    print("🔍 Verificando conectividad básica...")
    
    urls_to_test = [
        "http://localhost:9000/",
        "http://localhost:9000/health/",
        "http://127.0.0.1:9000/",
    ]
    
    for url in urls_to_test:
        try:
            print(f"Probando: {url}")
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            
            print(f"✅ Status: {response.status_code}")
            print(f"⏱️  Tiempo: {response_time*1000:.0f}ms")
            
            # Ver headers de performance
            if 'X-Response-Time' in response.headers:
                print(f"🚀 X-Response-Time: {response.headers['X-Response-Time']}")
            if 'X-Active-Requests' in response.headers:
                print(f"👥 X-Active-Requests: {response.headers['X-Active-Requests']}")
            
            return True
            
        except requests.exceptions.ConnectionError:
            print(f"❌ No se puede conectar a {url}")
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout en {url}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    if test_basic_connection():
        print("\n✅ Servidor funcionando - Listo para pruebas de carga")
    else:
        print("\n❌ Servidor no responde - Revisar configuración")