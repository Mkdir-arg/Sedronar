# SISOC - Versión Básica

Sistema de gestión básico basado en **Django** y **MySQL**, desplegable mediante **Docker** y **Docker Compose**.  
Esta versión incluye únicamente los módulos esenciales: Login, Ciudadanos y configuración de usuarios.

---

## Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)  
2. [Requisitos Previos](#requisitos-previos)  
3. [Despliegue Local](#despliegue-local)  
4. [Estructura de Carpetas](#estructura-de-carpetas)  
5. [Formateo y Estilo de Código](#formateo-y-estilo-de-código)  
6. [Variables de Entorno](#variables-de-entorno)  
7. [Tests Automáticos](#tests-automáticos)  
8. [Módulos Incluidos](#módulos-incluidos)  
9. [Tecnologías Utilizadas](#tecnologías-utilizadas)  
10. [Contribución](#contribución)

---

## Arquitectura General

- **Backend**: Django  
- **Base de datos**: MySQL  
- **Contenedores**: Docker + Docker Compose  
- **Front-end**: HTML, CSS, JS, Tailwind CSS, Alpine.js  
- **Tests**: pytest  

---

## Requisitos Previos

- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados.  
- Python 3.11+ (solo si se ejecuta fuera de contenedores).  
- VSCode recomendado con extensión **Python** y **Docker**.  

---

## Despliegue Local

1. Clonar el repositorio:
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd Sedronar
   ```
2. Levantar servicios:
   ```bash
   docker-compose up
   ```
3. Acceder a la app en [http://localhost:9000](http://localhost:9000).
4. Credenciales por defecto:
   - Usuario: `admin`
   - Contraseña: `admin123`

## Reiniciar base de datos
```bash
docker-compose down
docker volume rm sedronar_sedronar_mysql_data
docker-compose up
```

## Debug con VSCode
- Iniciar servicios con `docker-compose up`.  
- Seleccionar la configuración `Django in Docker` en el panel de debugging.  

---

## Estructura de Carpetas

- **`config/`** → configuración global de Django  
- **`docker/`** → archivos de contenedores  
- **`users/`** → gestión de usuarios y autenticación  
- **`core/`** → funcionalidades básicas del sistema  
- **`dashboard/`** → página de inicio  
- **`ciudadanos/`** → módulo de gestión de ciudadanos  
- **`healthcheck/`** → verificación de salud del sistema  
- **`templates/`** → plantillas HTML  
- **`static/`** → archivos estáticos (CSS, JS, imágenes)  

---

## Formateo y Estilo de Código

Antes de un **Pull Request**, ejecutar:

```bash
# Linter
pylint **/*.py --rcfile=.pylintrc

# Formateo Python
black .

# Formateo Django Templates
djlint . --configuration=.djlintrc --reformat
```

---

## Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
# Django
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=tu-clave-secreta
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Base de datos
DATABASE_HOST=sedronar-mysql
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=sedronar123
DATABASE_NAME=sedronar
```

---

## Tests Automáticos

Ejecutar:
```bash
docker compose exec django pytest -n auto
```

---

## Módulos Incluidos

### 1. **Autenticación y Usuarios**
- Login/Logout
- Gestión de usuarios
- Grupos y permisos
- Perfiles de usuario

### 2. **Ciudadanos**
- Registro de ciudadanos
- Búsqueda y filtrado
- Gestión de información personal

### 3. **Dashboard**
- Página de inicio
- Estadísticas básicas

### 4. **Core**
- Funcionalidades compartidas
- Modelos base (Provincia, Localidad, etc.)
- Utilidades comunes

---

## Tecnologías Utilizadas

- **Django 4.2**: Framework web
- **MySQL 8.0**: Base de datos
- **Docker & Docker Compose**: Contenedores
- **Tailwind CSS**: Framework CSS utilitario
- **Alpine.js**: Framework JS ligero para interactividad
- **pytest**: Testing
- **Black**: Formateo de código
- **Pylint**: Análisis de código

---

## Contribución

1. Crear una branch desde `main`.  
2. Commit siguiendo el estándar definido.  
3. Abrir **Pull Request** a `main`.  
4. Pasar linters y tests antes del PR.  
5. Revisión de al menos otro dev antes del merge.  

---

## Credenciales por Defecto

- **Usuario**: admin
- **Contraseña**: admin123
- **Email**: admin@sisoc.gov.ar

**¡IMPORTANTE!** Cambiar estas credenciales en producción.