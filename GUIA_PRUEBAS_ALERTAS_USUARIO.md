# 🚨 GUÍA DE PRUEBAS - SISTEMA DE ALERTAS WEBSOCKET

## 📋 **PREPARACIÓN INICIAL**

**1. Levantar el sistema:**
```bash
docker-compose up
```

**2. Acceder como usuario:**
- URL: http://localhost:9000
- Usuario: `admin` / Contraseña: `admin123`

**3. Abrir herramientas de desarrollador (F12):**
- Ir a pestaña "Console" para ver logs WebSocket
- Ir a pestaña "Network" > "WS" para ver conexiones WebSocket

---

## 🔔 **QUÉ OBSERVAR EN CADA PRUEBA**

### **Indicadores Visuales:**
- ✅ **Contador de alertas** en navbar (campana con número rojo)
- ✅ **Dropdown de alertas** (click en campana - muestra últimas 5 alertas)
- ✅ **Dashboard de alertas** (click "Ver todas" o ir a `/legajos/alertas/`)
- ✅ **Estado WebSocket** (punto verde/rojo junto a la campana)
- ✅ **Toast notifications** (esquina superior derecha)
- ✅ **Modal crítico** para alertas de prioridad CRÍTICA
- ✅ **Sonido** para alertas críticas
- ✅ **Notificación del navegador** (si das permisos)

### **Cómo se ven las alertas:**

#### **1. Icono de Campana (Navbar):**
- 🔴 **Número rojo** sobre la campana = cantidad de alertas activas
- 🟢 **Punto verde** = WebSocket conectado
- 🔴 **Punto rojo** = WebSocket desconectado
- **Click en campana** = abre dropdown con últimas alertas

#### **2. Toast Notifications (Esquina superior derecha):**
- **Rojo** = Alertas CRÍTICAS (con sonido)
- **Naranja** = Alertas ALTAS
- **Amarillo** = Alertas MEDIAS
- **Azul** = Alertas BAJAS
- **Duración**: 5 segundos (se cierran solas)

#### **3. Modal Crítico (Centro de pantalla):**
- Solo para alertas **CRÍTICAS**
- **Fondo oscuro** con modal rojo
- **Botón "Ver Legajo"** para ir directo al caso
- **Sonido de alerta**
- **Parpadeo en título** del navegador

#### **4. Dashboard de Alertas (`/legajos/alertas/`):**
- **Estadísticas** por prioridad
- **Tarjetas grandes** para alertas críticas
- **Lista compacta** para alertas altas/medias
- **Botón cerrar** en cada alerta
- **Enlaces** a legajos relacionados

---

## 🧪 **PRUEBAS POR CATEGORÍA**

### **1. ALERTAS DE LEGAJOS**

#### **🔴 ALERTA: Riesgo Alto**
**Cómo llegar:**
1. Ir a `/admin/legajos/legajoatencion/`
2. Seleccionar un legajo existente
3. Cambiar `nivel_riesgo` de "BAJO" o "MEDIO" a "ALTO"
4. Guardar

**Qué deberías ver:**
- ✅ Toast notification inmediata: "CAMBIO_RIESGO"
- ✅ Contador de alertas aumenta
- ✅ En consola: mensaje WebSocket recibido

#### **🟡 ALERTA: Sin Evaluación Inicial**
**Cómo llegar:**
1. Ir a `/admin/legajos/legajoatencion/`
2. Crear nuevo legajo
3. Cambiar `fecha_apertura` a hace 20 días
4. NO crear evaluación inicial
5. Ejecutar: `docker compose exec django python manage.py test_alertas_websocket --ciudadano-id X`

**Qué deberías ver:**
- ✅ Toast notification: "SIN_EVALUACION"
- ✅ Mensaje: "Sin evaluación inicial hace X días"

#### **🔴 ALERTA: Riesgo Suicida**
**Cómo llegar:**
1. Ir a `/admin/legajos/evaluacioninicial/`
2. Crear evaluación para un legajo
3. Marcar `riesgo_suicida = True`
4. Guardar

**Qué deberías ver:**
- ✅ Modal crítico rojo con sonido
- ✅ Toast notification: "RIESGO_SUICIDA"
- ✅ Notificación del navegador

---

### **2. ALERTAS DE SEGUIMIENTOS**

#### **🔴 ALERTA: Seguimiento Vencido**
**Cómo llegar:**
1. Ir a `/admin/legajos/seguimientocontacto/`
2. Crear nuevo seguimiento
3. Poner `fecha_proximo_contacto` hace 10 días
4. Guardar

**Qué deberías ver:**
- ✅ Toast notification: "SEGUIMIENTO_VENCIDO"
- ✅ Prioridad CRÍTICA (>7 días vencido)

#### **🟡 ALERTA: Adherencia Baja**
**Cómo llegar:**
1. Crear 2 seguimientos para el mismo legajo
2. Poner `adherencia = "BAJA"` en ambos
3. Ejecutar comando de alertas

**Qué deberías ver:**
- ✅ Toast notification: "ADHERENCIA_BAJA"
- ✅ Mensaje: "Adherencia baja en X seguimientos"

---

### **3. ALERTAS DE CONVERSACIONES**

#### **🟡 ALERTA: Nueva Conversación**
**Cómo llegar:**
1. Ir a `/admin/conversaciones/conversacion/`
2. Crear nueva conversación
3. Asignar `ciudadano_relacionado`
4. Guardar

**Qué deberías ver:**
- ✅ Toast notification: "NUEVA_CONVERSACION"
- ✅ Mensaje con nombre del ciudadano

#### **🟠 ALERTA: Mensaje Sin Operador**
**Cómo llegar:**
1. Crear conversación sin `operador_asignado`
2. Ir a `/admin/conversaciones/mensaje/`
3. Crear mensaje con `remitente = "ciudadano"`
4. Guardar

**Qué deberías ver:**
- ✅ Toast notification: "MENSAJE_SIN_OPERADOR"
- ✅ Prioridad ALTA

#### **🔵 ALERTA: Conversación Cerrada**
**Cómo llegar:**
1. Tomar conversación existente
2. Cambiar `estado` de "ACTIVA" a "CERRADA"
3. Guardar

**Qué deberías ver:**
- ✅ Toast notification: "CONVERSACION_CERRADA"
- ✅ Duración de la conversación

---

### **4. ALERTAS DE EVENTOS CRÍTICOS**

#### **🔴 ALERTA: Evento Crítico**
**Cómo llegar:**
1. Ir a `/admin/legajos/eventocritico/`
2. Crear nuevo evento crítico
3. Seleccionar cualquier `tipo`
4. Guardar

**Qué deberías ver:**
- ✅ Modal crítico inmediato
- ✅ Toast notification: "EVENTO_CRITICO_INMEDIATO"
- ✅ Sonido de alerta

---

### **5. ALERTAS GENERALES**

#### **🟡 ALERTA: Sin Red Familiar**
**Cómo llegar:**
1. Tener ciudadano sin vínculos familiares
2. Ejecutar: `docker compose exec django python manage.py test_alertas_websocket --ciudadano-id X`

**Qué deberías ver:**
- ✅ Toast notification: "SIN_RED_FAMILIAR"

#### **🟡 ALERTA: Datos Incompletos**
**Cómo llegar:**
1. Ir a `/admin/legajos/ciudadano/`
2. Editar ciudadano
3. Dejar vacíos: `telefono`, `email`, `domicilio`
4. Ejecutar comando de alertas

**Qué deberías ver:**
- ✅ Toast notification: "DATOS_INCOMPLETOS"
- ✅ Lista de campos faltantes

---

## 🎯 **PRUEBAS RÁPIDAS**

### **Prueba Completa en 5 Minutos:**

1. **Abrir F12 > Console**
2. **Ejecutar:** `docker compose exec django python manage.py test_alertas_websocket --crear-alerta-critica`
3. **Crear evento crítico** en admin
4. **Cambiar riesgo de legajo** a ALTO
5. **Crear seguimiento vencido** con fecha pasada

### **Verificar Funcionamiento:**
- ✅ **Contador de alertas cambia** (número en campana)
- ✅ **Dropdown se actualiza** (click en campana)
- ✅ **Toast notifications aparecen** (esquina superior derecha)
- ✅ **Dashboard se actualiza** (ir a `/legajos/alertas/`)
- ✅ **Console muestra mensajes WebSocket** (F12 > Console)
- ✅ **Estado WebSocket verde** (punto junto a campana)
- ✅ **Modal crítico** para alertas importantes
- ✅ **Sonido** para alertas críticas

### **Navegación de Alertas:**
1. **Campana en navbar** → Dropdown con últimas 5 alertas
2. **"Ver todas"** en dropdown → Dashboard completo
3. **Dashboard** → `/legajos/alertas/` - Vista completa
4. **"Ver Legajo"** → Va al legajo relacionado
5. **Botón "Cerrar"** → Cierra la alerta (desaparece)

---

## 🔧 **SOLUCIÓN DE PROBLEMAS**

### **Si no ves notificaciones:**
1. **Verificar WebSocket:** Estado debe estar verde
2. **Revisar Console:** Buscar errores de conexión
3. **Permisos navegador:** Permitir notificaciones
4. **Recargar página:** F5 para reconectar

### **Si WebSocket no conecta:**
1. **Verificar servicios:** `docker-compose ps`
2. **Logs del contenedor:** `docker-compose logs django`
3. **Redis funcionando:** Necesario para WebSocket

### **URLs de Verificación:**
- **Dashboard Principal:** http://localhost:9000
- **Dashboard de Alertas:** http://localhost:9000/legajos/alertas/
- **Admin Alertas:** http://localhost:9000/admin/legajos/alertaciudadano/
- **API Contador:** http://localhost:9000/legajos/alertas/count/
- **API Alertas:** http://localhost:9000/api/legajos/alertas/
- **WebSocket:** ws://localhost:9000/ws/alertas/

---

## 📊 **TIPOS DE ALERTAS Y PRIORIDADES**

| Tipo | Prioridad | Color | Sonido | Modal |
|------|-----------|-------|--------|-------|
| RIESGO_SUICIDA | CRÍTICA | Rojo | ✅ | ✅ |
| VIOLENCIA | CRÍTICA | Rojo | ✅ | ✅ |
| EVENTO_CRITICO | CRÍTICA | Rojo | ✅ | ✅ |
| SEGUIMIENTO_VENCIDO (>7d) | CRÍTICA | Rojo | ✅ | ✅ |
| RIESGO_ALTO | ALTA | Naranja | ❌ | ❌ |
| SIN_CONTACTO | ALTA | Naranja | ❌ | ❌ |
| MENSAJE_SIN_OPERADOR | ALTA | Naranja | ❌ | ❌ |
| SIN_EVALUACION | MEDIA | Amarillo | ❌ | ❌ |
| DERIVACION_PENDIENTE | MEDIA | Amarillo | ❌ | ❌ |
| SIN_RED_FAMILIAR | BAJA | Azul | ❌ | ❌ |

¡Con esta guía puedes probar todas las alertas del sistema como usuario final!