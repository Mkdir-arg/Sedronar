# settings.py
import os
import sys
import logging
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# --- Paths y .env (en este orden) ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# --- Entorno ---
DEBUG = os.environ.get("DJANGO_DEBUG", "False") == "True"
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")  # dev|qa|prd

# --- Secret Key ---
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# --- i18n/Timezone ---
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Hosts / CSRF ---
# Tomo del .env si existe; si no, fuerzo dominio de PythonAnywhere para evitar 400.
hosts_env = os.getenv("DJANGO_ALLOWED_HOSTS", "")
hosts = [h.strip() for h in hosts_env.split(",") if h.strip()]
if "mlepera.pythonanywhere.com" not in hosts:
    hosts += ["mlepera.pythonanywhere.com"]
# en desarrollo, también localhost
if DEBUG:
    for h in ("localhost", "127.0.0.1"):
        if h not in hosts:
            hosts.append(h)

ALLOWED_HOSTS = list(dict.fromkeys(hosts))  # sin duplicados

DEFAULT_SCHEME = "https" if ENVIRONMENT == "prd" else "http"

# CSRF_TRUSTED_ORIGINS requiere esquema. Para PA siempre https.
CSRF_TRUSTED_ORIGINS = ["https://mlepera.pythonanywhere.com"]
if DEBUG:
    CSRF_TRUSTED_ORIGINS += ["http://localhost", "http://127.0.0.1"]

# --- Apps ---
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admindocs",
    # Libs
    "django_extensions",
    "rest_framework",
    "channels",
    # Apps propias
    "users",
    "core",
    "dashboard",
    "legajos",
    "configuracion",
    "chatbot",
    "conversaciones",
    "portal",
    "tramites",
    "healthcheck",  # la usás en urls
    # "simple_history",       # si la reactivás, agregala también acá
    "drf_spectacular",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
    "config.middlewares.xss_protection.XSSProtectionMiddleware",
    "config.middlewares.threadlocals.ThreadLocalMiddleware",
    # "simple_history.middleware.HistoryRequestMiddleware",
    "config.middlewares.auditoria.AuditoriaMiddleware",
    "config.middlewares.query_counter.QueryCountMiddleware",
]

# --- URLs / WSGI / ASGI ---
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Templates ---
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "legajos.context_processors.alertas_eventos_criticos",
                "core.context_processors.dispositivos_context",
                "conversaciones.context_processors.user_groups",
            ],
        },
    },
]

# --- Static & Media ---
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # coherente con mapeo en panel Web

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Auth / Redirects ---
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "inicio"
LOGOUT_REDIRECT_URL = "login"
ACCOUNT_FORMS = {"login": "users.forms.UserLoginForm"}

# --- Email ---
if ENVIRONMENT == "prd":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Mensajes ---
MESSAGE_TAGS = {
    messages.DEBUG: "bg-gray-800 text-white",
    messages.INFO: "bg-blue-500 text-white",
    messages.SUCCESS: "bg-green-500 text-white",
    messages.WARNING: "bg-yellow-500 text-white",
    messages.ERROR: "bg-red-500 text-white",
}

# --- DB ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
        "CONN_MAX_AGE": 60,
    }
}

if "pytest" in sys.argv or os.environ.get("PYTEST_RUNNING") == "1":
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# --- Cache ---
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# --- Channels ---
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# --- TTLs ---
DEFAULT_CACHE_TIMEOUT = 300
DASHBOARD_CACHE_TIMEOUT = 300
CIUDADANO_CACHE_TIMEOUT = 300

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# --- Integraciones ---
DOMINIO = os.environ.get("DOMINIO", "localhost:8001")
RENAPER_API_USERNAME = os.getenv("RENAPER_API_USERNAME")
RENAPER_API_PASSWORD = os.getenv("RENAPER_API_PASSWORD")
RENAPER_API_URL = os.getenv("RENAPER_API_URL")
RENAPER_TEST_MODE = os.getenv("RENAPER_TEST_MODE", "False") == "True"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Logging ---
LOG_DIR = BASE_DIR / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "info_only": {"()": "django.utils.log.CallbackFilter", "callback": lambda r: r.levelno == logging.INFO},
        "error_only": {"()": "django.utils.log.CallbackFilter", "callback": lambda r: r.levelno == logging.ERROR},
        "warning_only": {"()": "django.utils.log.CallbackFilter", "callback": lambda r: r.levelno == logging.WARNING},
        "critical_only": {"()": "django.utils.log.CallbackFilter", "callback": lambda r: r.levelno == logging.CRITICAL},
        "data_only": {"()": "django.utils.log.CallbackFilter", "callback": lambda r: hasattr(r, "data")},
    },
    "formatters": {
        "verbose": {"format": "[{asctime}] {module} {levelname} {name}: {message}", "style": "{"},
        "simple": {"format": "[{asctime}] {levelname} {message}", "style": "{"},
        "json_data": {"()": "core.utils.JSONDataFormatter"},
    },
    "handlers": {
        "info_file": {"level": "INFO", "filters": ["info_only"], "class": "core.utils.DailyFileHandler", "filename": str(LOG_DIR / "info.log"), "formatter": "verbose"},
        "error_file": {"level": "ERROR", "filters": ["error_only"], "class": "core.utils.DailyFileHandler", "filename": str(LOG_DIR / "error.log"), "formatter": "verbose"},
        "warning_file": {"level": "WARNING", "filters": ["warning_only"], "class": "core.utils.DailyFileHandler", "filename": str(LOG_DIR / "warning.log"), "formatter": "verbose"},
        "critical_file": {"level": "CRITICAL", "filters": ["critical_only"], "class": "core.utils.DailyFileHandler", "filename": str(LOG_DIR / "critical.log"), "formatter": "verbose"},
        "data_file": {"level": "INFO", "filters": ["data_only"], "class": "core.utils.DailyFileHandler", "filename": str(LOG_DIR / "data.log"), "formatter": "json_data"},
    },
    "root": {"handlers": ["info_file", "error_file", "warning_file", "critical_file", "data_file"], "level": "DEBUG" if DEBUG else "INFO"},
    "loggers": {"django": {"handlers": [], "level": "DEBUG" if DEBUG else "INFO", "propagate": True}, "django.request": {"handlers": ["error_file"], "level": "ERROR", "propagate": False}},
}

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Debug tools ---
if DEBUG:
    INTERNAL_IPS = ["127.0.0.1", "::1"]

# --- Seguridad por entorno ---
if ENVIRONMENT == "prd":
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
# DRF Spectacular Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'SEDRONAR API',
    'DESCRIPTION': 'Sistema de Gestión SEDRONAR - Documentación de APIs',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': '/api/',
}