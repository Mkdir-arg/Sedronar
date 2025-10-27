from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("", include("django.contrib.auth.urls")),
    path("", include("users.urls")),
    path("", include("core.urls")),
    path("", include("dashboard.urls")),
    path("legajos/", include("legajos.urls")),
    path("configuracion/", include("configuracion.urls")),
    path("chatbot/", include("chatbot.urls")),
    path("conversaciones/", include("conversaciones.urls")),

    path("", include("healthcheck.urls")),
]

# URLs de desarrollo se pueden agregar aquí si es necesario

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler500 = "config.views.server_error"
