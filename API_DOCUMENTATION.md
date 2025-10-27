# SISOC API Documentation

## Introducción

El sistema SISOC ahora cuenta con una API REST completamente documentada usando **Swagger/OpenAPI 3.0**. Esta documentación proporciona acceso programático a todas las funcionalidades del sistema.

## Acceso a la Documentación

Una vez que el sistema esté ejecutándose, puedes acceder a la documentación interactiva en:

- **Swagger UI**: `http://localhost:9000/api/docs/`
- **ReDoc**: `http://localhost:9000/api/redoc/`
- **Schema JSON**: `http://localhost:9000/api/schema/`

## Autenticación

Todas las APIs requieren autenticación. El sistema utiliza autenticación basada en sesiones de Django.

### Para usar las APIs:

1. Primero inicia sesión en el sistema web
2. Usa las mismas credenciales de sesión para las APIs
3. O implementa autenticación por token si es necesario

## Endpoints Disponibles

### 1. Módulo Core (`/api/core/`)

- **Provincias**: `/api/core/provincias/`
- **Municipios**: `/api/core/municipios/`
- **Localidades**: `/api/core/localidades/`
- **Dispositivos de Red**: `/api/core/dispositivos/`
- **Datos de referencia**: sexos, meses, días, turnos

#### Ejemplos:
```bash
# Listar todas las provincias
GET /api/core/provincias/

# Obtener municipios de una provincia
GET /api/core/provincias/1/municipios/

# Crear un nuevo dispositivo
POST /api/core/dispositivos/
```

### 2. Módulo Legajos (`/api/legajos/`)

- **Ciudadanos**: `/api/legajos/ciudadanos/`
- **Legajos de Atención**: `/api/legajos/legajos/`
- **Evaluaciones Iniciales**: `/api/legajos/evaluaciones/`
- **Planes de Intervención**: `/api/legajos/planes/`
- **Seguimientos**: `/api/legajos/seguimientos/`
- **Derivaciones**: `/api/legajos/derivaciones/`
- **Eventos Críticos**: `/api/legajos/eventos/`

#### Ejemplos:
```bash
# Listar ciudadanos
GET /api/legajos/ciudadanos/

# Crear un nuevo ciudadano
POST /api/legajos/ciudadanos/
{
  "dni": "12345678",
  "nombre": "Juan",
  "apellido": "Pérez",
  "genero": "M"
}

# Cerrar un legajo
POST /api/legajos/legajos/123/cerrar/
{
  "motivo_cierre": "Tratamiento completado exitosamente"
}
```

### 3. Módulo Chatbot (`/api/chatbot/`)

- **Conversaciones**: `/api/chatbot/conversations/`
- **Mensajes**: `/api/chatbot/messages/`
- **Base de Conocimiento**: `/api/chatbot/knowledge/`
- **Feedback**: `/api/chatbot/feedback/`

#### Ejemplos:
```bash
# Crear nueva conversación
POST /api/chatbot/conversations/
{
  "title": "Consulta sobre tratamiento"
}

# Enviar mensaje al chatbot
POST /api/chatbot/conversations/1/send_message/
{
  "message": "¿Cuáles son los pasos para iniciar un tratamiento?"
}
```

### 4. Módulo Users (`/api/users/`)

- **Usuarios**: `/api/users/users/`
- **Grupos**: `/api/users/groups/`
- **Perfiles**: `/api/users/profiles/`

#### Ejemplos:
```bash
# Obtener perfil actual
GET /api/users/users/me/

# Cambiar contraseña
POST /api/users/users/change_password/
{
  "old_password": "contraseña_actual",
  "new_password": "nueva_contraseña",
  "new_password_confirm": "nueva_contraseña"
}
```

## Filtros y Búsqueda

La mayoría de los endpoints soportan:

- **Filtrado**: `?campo=valor`
- **Búsqueda**: `?search=término`
- **Ordenamiento**: `?ordering=campo` o `?ordering=-campo`
- **Paginación**: `?page=2&page_size=20`

### Ejemplos:
```bash
# Filtrar legajos por estado
GET /api/legajos/legajos/?estado=ABIERTO

# Buscar ciudadanos por nombre
GET /api/legajos/ciudadanos/?search=Juan

# Ordenar por fecha de creación
GET /api/legajos/legajos/?ordering=-fecha_admision
```

## Códigos de Respuesta

- `200 OK`: Operación exitosa
- `201 Created`: Recurso creado exitosamente
- `400 Bad Request`: Error en los datos enviados
- `401 Unauthorized`: No autenticado
- `403 Forbidden`: Sin permisos
- `404 Not Found`: Recurso no encontrado
- `500 Internal Server Error`: Error del servidor

## Formato de Respuesta

Todas las respuestas están en formato JSON:

```json
{
  "count": 25,
  "next": "http://localhost:9000/api/legajos/ciudadanos/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "dni": "12345678",
      "nombre": "Juan",
      "apellido": "Pérez",
      "creado": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Instalación y Configuración

### 1. Instalar dependencias:
```bash
pip install drf-spectacular==0.27.0
```

### 2. La configuración ya está incluida en `settings.py`:
- `drf_spectacular` en `INSTALLED_APPS`
- Configuración de `SPECTACULAR_SETTINGS`
- Schema class en `REST_FRAMEWORK`

### 3. Las URLs están configuradas en `config/urls.py`

## Desarrollo y Personalización

### Agregar nuevos endpoints:

1. Crear serializers en `app/serializers.py`
2. Crear viewsets en `app/api_views.py`
3. Registrar en `app/api_urls.py`
4. Incluir en `config/urls.py`

### Documentar endpoints:

```python
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description="Lista todos los elementos"),
    create=extend_schema(description="Crea un nuevo elemento")
)
class MiViewSet(viewsets.ModelViewSet):
    # ...
```

## Seguridad

- Todas las APIs requieren autenticación
- Los permisos se validan por endpoint
- Los datos sensibles están protegidos
- Se respetan los permisos de usuario y grupos

## Soporte

Para más información sobre el uso de las APIs, consulta:
- La documentación interactiva en `/api/docs/`
- Los ejemplos en cada endpoint
- El código fuente en los archivos `api_views.py` de cada módulo