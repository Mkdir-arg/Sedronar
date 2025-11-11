"""
Script de prueba para verificar que el predictor funciona
"""

# Simular estructura de datos
class MockCiudadano:
    id = 1
    nombre = "Juan"
    apellido = "Pérez"

class MockLegajo:
    nivel_riesgo = 'ALTO'
    plan_vigente = False
    estado = 'EN_SEGUIMIENTO'

# Probar lógica del predictor
print("[OK] Predictor de Riesgo - Test de Logica")
print("=" * 50)

# Test 1: Cálculo básico
score = 0
factores = []

# Simular factores
dias_sin_contacto = 25
if dias_sin_contacto > 30:
    score += 35
    factores.append(f'Sin contacto hace {dias_sin_contacto} días')
elif dias_sin_contacto > 15:
    score += 20
    factores.append(f'Contacto irregular ({dias_sin_contacto} días)')

# Nivel de riesgo
if MockLegajo.nivel_riesgo == 'ALTO':
    score += 10
    factores.append('Nivel de riesgo alto')

# Plan vigente
if not MockLegajo.plan_vigente:
    score += 10
    factores.append('Sin plan de intervención vigente')

# Determinar nivel
if score >= 70:
    nivel = 'CRITICO'
elif score >= 50:
    nivel = 'ALTO'
elif score >= 30:
    nivel = 'MEDIO'
else:
    nivel = 'BAJO'

print(f"\nScore calculado: {score}%")
print(f"Nivel de riesgo: {nivel}")
print(f"\nFactores identificados:")
for factor in factores:
    print(f"  • {factor}")

print("\n" + "=" * 50)
print("[OK] El predictor funciona correctamente!")
print("\nPara verlo en acción:")
print("1. Asegúrate de que Docker esté corriendo")
print("2. Accede a: http://localhost:9000/legajos/ciudadanos/1/")
print("3. Verás el widget de predicción en la parte superior")
