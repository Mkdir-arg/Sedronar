#!/usr/bin/env python3
"""
Sistema de pruebas de carga para verificar performance
"""
import asyncio
import aiohttp
import time
import statistics
from concurrent.futures import ThreadPoolExecutor
import json

class LoadTester:
    def __init__(self, base_url="http://localhost:9000"):
        self.base_url = base_url
        self.results = []
        
    async def single_request(self, session, endpoint="/"):
        """Ejecuta una request individual"""
        start_time = time.time()
        try:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                await response.text()
                response_time = time.time() - start_time
                return {
                    'status': response.status,
                    'response_time': response_time,
                    'success': response.status == 200
                }
        except Exception as e:
            return {
                'status': 0,
                'response_time': time.time() - start_time,
                'success': False,
                'error': str(e)
            }
    
    async def concurrent_test(self, concurrent_users=100, requests_per_user=10):
        """Prueba con usuarios concurrentes"""
        print(f"🚀 Iniciando prueba: {concurrent_users} usuarios, {requests_per_user} requests c/u")
        
        connector = aiohttp.TCPConnector(limit=1000, limit_per_host=500)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = []
            
            # Crear tasks para todos los requests
            for user in range(concurrent_users):
                for req in range(requests_per_user):
                    task = self.single_request(session, "/")
                    tasks.append(task)
            
            # Ejecutar todos los requests concurrentemente
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time
            
            # Procesar resultados
            successful_requests = [r for r in results if isinstance(r, dict) and r.get('success')]
            failed_requests = [r for r in results if not (isinstance(r, dict) and r.get('success'))]
            
            if successful_requests:
                response_times = [r['response_time'] for r in successful_requests]
                
                stats = {
                    'total_requests': len(results),
                    'successful_requests': len(successful_requests),
                    'failed_requests': len(failed_requests),
                    'success_rate': len(successful_requests) / len(results) * 100,
                    'total_time': total_time,
                    'requests_per_second': len(results) / total_time,
                    'avg_response_time': statistics.mean(response_times),
                    'min_response_time': min(response_times),
                    'max_response_time': max(response_times),
                    'p95_response_time': statistics.quantiles(response_times, n=20)[18] if len(response_times) > 20 else max(response_times),
                    'concurrent_users': concurrent_users
                }
            else:
                stats = {
                    'total_requests': len(results),
                    'successful_requests': 0,
                    'failed_requests': len(failed_requests),
                    'success_rate': 0,
                    'error': 'No successful requests'
                }
            
            return stats
    
    def print_results(self, stats):
        """Imprime resultados formateados"""
        print("\n" + "="*60)
        print("📊 RESULTADOS DE PRUEBA DE CARGA")
        print("="*60)
        
        if stats.get('success_rate', 0) > 0:
            print(f"✅ Requests exitosos: {stats['successful_requests']}/{stats['total_requests']}")
            print(f"📈 Tasa de éxito: {stats['success_rate']:.1f}%")
            print(f"⚡ Requests/segundo: {stats['requests_per_second']:.1f}")
            print(f"👥 Usuarios concurrentes: {stats['concurrent_users']}")
            print(f"⏱️  Tiempo promedio: {stats['avg_response_time']*1000:.0f}ms")
            print(f"🚀 Tiempo mínimo: {stats['min_response_time']*1000:.0f}ms")
            print(f"🐌 Tiempo máximo: {stats['max_response_time']*1000:.0f}ms")
            print(f"📊 P95: {stats['p95_response_time']*1000:.0f}ms")
            
            # Evaluación de performance
            if stats['avg_response_time'] < 0.5:
                print("🏆 EXCELENTE: Tiempo de respuesta < 500ms")
            elif stats['avg_response_time'] < 1.0:
                print("✅ BUENO: Tiempo de respuesta < 1s")
            elif stats['avg_response_time'] < 2.0:
                print("⚠️  ACEPTABLE: Tiempo de respuesta < 2s")
            else:
                print("❌ LENTO: Tiempo de respuesta > 2s")
                
        else:
            print("❌ FALLO: No se pudieron completar requests exitosos")
            print(f"Requests fallidos: {stats['failed_requests']}")
        
        print("="*60)

async def run_progressive_test():
    """Ejecuta pruebas progresivas de carga"""
    tester = LoadTester()
    
    test_scenarios = [
        (50, 5),    # 50 usuarios, 5 requests c/u = 250 total
        (100, 5),   # 100 usuarios, 5 requests c/u = 500 total
        (200, 5),   # 200 usuarios, 5 requests c/u = 1000 total
        (300, 5),   # 300 usuarios, 5 requests c/u = 1500 total
        (500, 3),   # 500 usuarios, 3 requests c/u = 1500 total
    ]
    
    print("🔥 INICIANDO PRUEBAS PROGRESIVAS DE CARGA")
    print("Verificando capacidad del sistema optimizado...")
    
    all_results = []
    
    for users, requests in test_scenarios:
        print(f"\n⏳ Preparando prueba: {users} usuarios concurrentes...")
        await asyncio.sleep(2)  # Pausa entre pruebas
        
        try:
            stats = await tester.concurrent_test(users, requests)
            tester.print_results(stats)
            all_results.append(stats)
            
            # Si la tasa de éxito baja mucho, parar
            if stats.get('success_rate', 0) < 80:
                print("⚠️  Tasa de éxito baja, deteniendo pruebas progresivas")
                break
                
        except Exception as e:
            print(f"❌ Error en prueba: {e}")
            break
    
    # Resumen final
    if all_results:
        print("\n🎯 RESUMEN FINAL")
        print("-" * 40)
        for i, result in enumerate(all_results):
            users = test_scenarios[i][0]
            if result.get('success_rate', 0) > 0:
                print(f"{users} usuarios: {result['success_rate']:.1f}% éxito, {result['avg_response_time']*1000:.0f}ms promedio")
            else:
                print(f"{users} usuarios: FALLO")

if __name__ == "__main__":
    print("🚀 SISTEMA DE PRUEBAS DE CARGA - SEDRONAR")
    print("Verificando optimizaciones de Gunicorn + Workers asíncronos")
    
    try:
        asyncio.run(run_progressive_test())
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")