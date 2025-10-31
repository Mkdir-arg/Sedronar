# Sistema de Alertas para Conversaciones

## Descripción

Sistema de alertas en tiempo real para operadores con rol "Conversaciones". Cuando un ciudadano envía un mensaje a una conversación asignada, el operador recibe una alerta inmediata en el icono de campana del navbar.

## Funcionalidades Implementadas

### 1. Alertas en Tiempo Real
- ✅ Alerta automática cuando ciudadano envía mensaje
- ✅ Solo para conversaciones asignadas al operador
- ✅ Notificación WebSocket en tiempo real
- ✅ Contador visual en icono de campana
- ✅ Sonido de notificación

### 2. Interfaz de Usuario
- ✅ Icono de campana con contador de alertas
- ✅ Dropdown con preview de alertas
- ✅ Toast notifications
- ✅ Notificaciones del navegador (si están permitidas)
- ✅ Indicador de estado de conexión WebSocket

### 3. Permisos y Seguridad
- ✅ Solo usuarios con rol "Conversaciones" o "OperadorCharla"
- ✅ Alertas específicas por operador
- ✅ Conexión WebSocket autenticada

## Archivos Modificados/Creados

### Backend
- `conversaciones/signals_alertas.py` - Señales para generar alertas
- `conversaciones/consumers.py` - Consumer WebSocket para alertas
- `conversaciones/routing.py` - Rutas WebSocket
- `conversaciones/context_processors.py` - Context processor para grupos

### Frontend
- `static/custom/js/alertas_conversaciones.js` - Lógica principal de alertas
- `static/custom/js/notification_sound.js` - Generador de sonidos
- `templates/includes/base.html` - Inclusión de scripts

### Configuración
- `config/settings.py` - Context processor agregado

### Pruebas
- `test_alertas_conversaciones.py` - Script de prueba
- `ALERTAS_CONVERSACIONES.md` - Esta documentación

## Cómo Funciona

### 1. Flujo de Alertas

```
Ciudadano envía mensaje
         ↓
Signal post_save en Mensaje
         ↓
_generar_alerta_mensaje_ciudadano()
         ↓
WebSocket a grupo específico del operador
         ↓
JavaScript recibe alerta
         ↓
Actualiza UI + sonido + notificación
```

### 2. Estructura de Datos de Alerta

```javascript
{
    id: 'conv_123_456',
    conversacion_id: 123,
    tipo: 'NUEVO_MENSAJE_CIUDADANO',
    prioridad: 'MEDIA',
    mensaje: 'Nuevo mensaje en conversación #123',
    fecha: '31/10/2024 14:30',
    operador_id: 5,
    contenido_mensaje: 'Hola, necesito ayuda...'
}
```

## Instalación y Configuración

### 1. Verificar Configuración

El context processor debe estar en `settings.py`:

```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ... otros processors
            'conversaciones.context_processors.user_groups',
        ],
    },
}]
```

### 2. Ejecutar Pruebas

```bash
python test_alertas_conversaciones.py
```

### 3. Verificar en el Navegador

1. Iniciar servidor: `python manage.py runserver`
2. Iniciar sesión con usuario que tenga rol "Conversaciones"
3. Verificar que aparezca el icono de campana en el navbar
4. Ejecutar script de prueba para generar alertas
5. Verificar que aparezcan las notificaciones

## Personalización

### Cambiar Sonido de Notificación

Modificar `notification_sound.js`:

```javascript
// Cambiar frecuencia del tono
oscillator.frequency.setValueAtTime(1000, this.audioContext.currentTime);

// Cambiar duración
oscillator.stop(this.audioContext.currentTime + 0.5);
```

### Cambiar Estilo de Alertas

Modificar `alertas_conversaciones.js` en la función `mostrarToast()`:

```javascript
toast.className = 'fixed top-4 right-4 bg-green-600 text-white px-4 py-3 rounded-lg shadow-lg z-50 max-w-sm';
```

### Agregar Más Tipos de Alertas

1. Modificar `_generar_alerta_mensaje_ciudadano()` en `signals_alertas.py`
2. Agregar nuevos tipos en `alertas_conversaciones.js`
3. Actualizar el consumer si es necesario

## Troubleshooting

### Las alertas no aparecen

1. Verificar que el usuario tenga rol "Conversaciones"
2. Verificar conexión WebSocket en DevTools
3. Verificar que el context processor esté configurado
4. Verificar que los archivos JavaScript se carguen correctamente

### El sonido no funciona

1. Verificar que el navegador permita audio
2. Verificar que no esté en modo silencioso
3. Verificar consola del navegador por errores

### WebSocket no conecta

1. Verificar que el servidor esté corriendo
2. Verificar rutas en `routing.py`
3. Verificar permisos del usuario
4. Verificar configuración ASGI (si está habilitada)

## Próximas Mejoras

- [ ] Persistir alertas en base de datos
- [ ] Panel de configuración de notificaciones
- [ ] Diferentes tipos de sonidos por prioridad
- [ ] Integración con sistema de alertas general
- [ ] Métricas de tiempo de respuesta
- [ ] Alertas por email/SMS para casos críticos

## Notas Técnicas

- Las alertas son temporales (solo en memoria)
- Requiere WebSocket habilitado
- Compatible con navegadores modernos
- Usa Web Audio API para sonidos
- Responsive design incluido