#!/usr/bin/env python3
"""
Prueba de carga simple usando requests (sin async)
"""
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import statistics

class SimpleLoadTester:
    def __init__(self, base_url="http://localhost:9000"):
        self.base_url = base_url
        self.results = []
        self.lock = threading.Lock()
    
    def single_request(self, endpoint="/"):
        """Ejecuta una request individual"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}{endpoint}", timeout=30)
            response_time = time.time() - start_time
            
            with self.lock:
                self.results.append({
                    'status': response.status_code,
                    'response_time': response_time,
                    'success': response.status_code == 200
                })
            
            return response.status_code == 200
            
        except Exception as e:
            response_time = time.time() - start_time
            with self.lock:
                self.results.append({
                    'status': 0,
                    'response_time': response_time,
                    'success': False,
                    'error': str(e)
                })
            return False
    
    def run_test(self, concurrent_users=100, requests_per_user=5):
        """Ejecuta prueba de carga"""
        print(f"🚀 Iniciando prueba: {concurrent_users} usuarios, {requests_per_user} requests c/u")
        
        self.results = []
        total_requests = concurrent_users * requests_per_user
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []
            
            # Crear todas las tareas
            for user in range(concurrent_users):
                for req in range(requests_per_user):
                    future = executor.submit(self.single_request, "/")
                    futures.append(future)
            
            # Esperar a que terminen todas
            completed = 0
            for future in futures:
                future.result()
                completed += 1
                if completed % 50 == 0:
                    print(f"Completado: {completed}/{total_requests}")
        
        total_time = time.time() - start_time
        
        # Calcular estadísticas
        successful = [r for r in self.results if r['success']]
        failed = [r for r in self.results if not r['success']]
        
        if successful:
            response_times = [r['response_time'] for r in successful]
            
            stats = {
                'total_requests': len(self.results),
                'successful_requests': len(successful),
                'failed_requests': len(failed),
                'success_rate': len(successful) / len(self.results) * 100,
                'total_time': total_time,
                'requests_per_second': len(self.results) / total_time,
                'avg_response_time': statistics.mean(response_times),
                'min_response_time': min(response_times),
                'max_response_time': max(response_times),
                'concurrent_users': concurrent_users
            }
        else:
            stats = {
                'total_requests': len(self.results),
                'successful_requests': 0,
                'failed_requests': len(failed),
                'success_rate': 0,
                'error': 'No successful requests'
            }
        
        return stats
    
    def print_results(self, stats):
        """Imprime resultados"""
        print("\n" + "="*50)
        print("📊 RESULTADOS DE PRUEBA")
        print("="*50)
        
        if stats.get('success_rate', 0) > 0:
            print(f"✅ Exitosos: {stats['successful_requests']}/{stats['total_requests']}")
            print(f"📈 Éxito: {stats['success_rate']:.1f}%")
            print(f"⚡ RPS: {stats['requests_per_second']:.1f}")
            print(f"👥 Usuarios: {stats['concurrent_users']}")
            print(f"⏱️  Promedio: {stats['avg_response_time']*1000:.0f}ms")
            print(f"🚀 Mínimo: {stats['min_response_time']*1000:.0f}ms")
            print(f"🐌 Máximo: {stats['max_response_time']*1000:.0f}ms")
            
            if stats['avg_response_time'] < 0.5:
                print("🏆 EXCELENTE")
            elif stats['avg_response_time'] < 1.0:
                print("✅ BUENO")
            else:
                print("⚠️  MEJORABLE")
        else:
            print("❌ FALLO TOTAL")
        
        print("="*50)

def run_quick_tests():
    """Ejecuta pruebas rápidas"""
    tester = SimpleLoadTester()
    
    tests = [
        (10, 3),   # Prueba básica
        (50, 3),   # Prueba media
        (100, 3),  # Prueba alta
        (200, 2),  # Prueba límite
    ]
    
    print("🔥 PRUEBAS DE CARGA RÁPIDAS")
    
    for users, requests in tests:
        print(f"\n⏳ Probando {users} usuarios...")
        
        try:
            stats = tester.run_test(users, requests)
            tester.print_results(stats)
            
            if stats.get('success_rate', 0) < 80:
                print("⚠️  Límite alcanzado, deteniendo pruebas")
                break
                
        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    print("🚀 PRUEBAS DE CARGA SIMPLES - SEDRONAR")
    
    try:
        run_quick_tests()
    except KeyboardInterrupt:
        print("\n⏹️  Interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")