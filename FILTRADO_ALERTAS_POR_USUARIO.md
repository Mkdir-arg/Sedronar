# 🔒 Filtrado de Alertas por Usuario - SEDRONAR

## Implementación del Sistema de Permisos

Las alertas ahora se filtran automáticamente según el usuario que las consulta, garantizando que cada usuario vea únicamente las alertas que le corresponden según su rol y asignaciones.

## 🎯 Criterios de Filtrado

### 1. **Superusuarios**
- ✅ Ven **TODAS** las alertas del sistema
- Sin restricciones

### 2. **Administradores** (Grupo: 'Administrador')
- ✅ Ven **TODAS** las alertas del sistema
- Sin restricciones

### 3. **Supervisores** (Grupo: 'Supervisor')
- ✅ Ven alertas de **su provincia**
- Basado en `usuario.profile.provincia`

### 4. **Usuarios Provinciales**
- ✅ Ven alertas de **legajos de su provincia**
- Basado en `usuario.profile.es_usuario_provincial = True`
- Filtro: `legajo.dispositivo.provincia = usuario.profile.provincia`

### 5. **Responsables de Legajos**
- ✅ Ven alertas de **legajos donde son responsables**
- Filtro: `legajo.responsable = usuario`

### 6. **Usuarios de Dispositivo**
- ✅ Ven alertas de **legajos de su dispositivo**
- Se detecta automáticamente el dispositivo del usuario
- Filtro: `legajo.dispositivo = dispositivo_del_usuario`

### 7. **Usuarios Sin Asignaciones Específicas**
- ✅ Ven solo **alertas críticas generales**
- Filtro: `prioridad = 'CRITICA'`

## 🔧 Implementación Técnica

### Servicio Principal
```python
# legajos/services_filtros_usuario.py
FiltrosUsuarioService.obtener_alertas_usuario(usuario)
```

### Métodos Disponibles
- `obtener_alertas_usuario(usuario)` - Obtiene alertas filtradas
- `puede_ver_alerta(usuario, alerta)` - Verifica permisos específicos
- `obtener_estadisticas_usuario(usuario)` - Estadísticas filtradas

## 📊 Endpoints Actualizados

Todos los endpoints ahora respetan el filtrado por usuario:

| Endpoint | Descripción | Filtrado |
|----------|-------------|----------|
| `/legajos/alertas/count/` | Contador de alertas | ✅ Por usuario |
| `/legajos/alertas/preview/` | Preview navbar | ✅ Por usuario |
| `/legajos/alertas/` | Dashboard | ✅ Por usuario |
| `/api/legajos/alertas/` | API REST | ✅ Por usuario |
| `/legajos/alertas/debug/` | Debug info | ✅ Muestra filtros aplicados |

## 🔍 Detección Automática de Dispositivo

El sistema detecta automáticamente el dispositivo del usuario mediante:

1. **Legajos como responsable**: Si es responsable de algún legajo
2. **Seguimientos como profesional**: Si ha realizado seguimientos
3. **Configuraciones adicionales**: Extensible para más relaciones

## 📋 Información de Debug

Visita `/legajos/alertas/debug/` para ver:

- ✅ **Usuario actual** y sus grupos
- ✅ **Tipo de usuario** (provincial, superuser, etc.)
- ✅ **Provincia asignada**
- ✅ **Total de alertas del sistema** vs **alertas visibles para el usuario**
- ✅ **Últimas alertas filtradas**

## 🚀 Cómo Probar

### 1. Crear Alertas de Prueba
```bash
python manage.py crear_alertas_prueba
```

### 2. Verificar Filtrado
1. Inicia sesión con diferentes usuarios
2. Visita `/legajos/alertas/debug/`
3. Compara las alertas visibles vs totales del sistema
4. Verifica el icono de campana en el navbar

### 3. Casos de Prueba

#### Usuario Superadmin
- Debe ver **todas** las alertas
- Contador muestra total del sistema

#### Usuario Provincial
- Debe ver solo alertas de su provincia
- Contador filtrado por provincia

#### Responsable de Legajo
- Debe ver alertas de sus legajos asignados
- Contador específico de sus responsabilidades

#### Usuario Sin Asignaciones
- Debe ver solo alertas críticas
- Contador mínimo de alertas críticas

## 🔧 Configuración de Usuarios

### Asignar Provincia a Usuario
```python
from users.models import Profile
from core.models import Provincia

profile = user.profile
profile.es_usuario_provincial = True
profile.provincia = Provincia.objects.get(nombre='Buenos Aires')
profile.save()
```

### Asignar Responsable a Legajo
```python
from legajos.models import LegajoAtencion

legajo = LegajoAtencion.objects.get(id=legajo_id)
legajo.responsable = usuario
legajo.save()
```

### Asignar Grupos
```python
from django.contrib.auth.models import Group

grupo_supervisor = Group.objects.get(name='Supervisor')
usuario.groups.add(grupo_supervisor)
```

## 🎯 Beneficios del Sistema

### Seguridad
- ✅ **Aislamiento de datos** por usuario
- ✅ **Control granular** de permisos
- ✅ **Auditoría** de accesos

### Usabilidad
- ✅ **Información relevante** para cada usuario
- ✅ **Reducción de ruido** en alertas
- ✅ **Mejor rendimiento** con menos datos

### Escalabilidad
- ✅ **Filtrado a nivel de base de datos**
- ✅ **Consultas optimizadas**
- ✅ **Extensible** para nuevos roles

## 🔄 Flujo de Filtrado

```
Usuario hace petición
       ↓
FiltrosUsuarioService.obtener_alertas_usuario()
       ↓
Detecta rol y permisos del usuario
       ↓
Construye filtros Q() apropiados
       ↓
Retorna QuerySet filtrado
       ↓
Vista/API usa el QuerySet filtrado
       ↓
Usuario ve solo sus alertas
```

## ✅ Verificación Final

Para confirmar que el filtrado funciona:

1. **Crea usuarios con diferentes roles**
2. **Asigna provincias y responsabilidades**
3. **Ejecuta**: `python manage.py crear_alertas_prueba`
4. **Inicia sesión con cada usuario**
5. **Verifica**: Que cada uno ve diferentes alertas
6. **Comprueba**: `/legajos/alertas/debug/` para cada usuario

El sistema ahora garantiza que cada usuario vea únicamente las alertas que le corresponden según su rol y asignaciones en el sistema. 🔒✅