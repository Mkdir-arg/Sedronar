from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'configuracion'

urlpatterns = [
    # Provincias
    path('provincias/', login_required(views.ProvinciaListView.as_view()), name='provincias'),
    path('provincias/crear/', login_required(views.ProvinciaCreateView.as_view()), name='provincia_crear'),
    path('provincias/<int:pk>/editar/', login_required(views.ProvinciaUpdateView.as_view()), name='provincia_editar'),
    path('provincias/<int:pk>/eliminar/', login_required(views.ProvinciaDeleteView.as_view()), name='provincia_eliminar'),
    
    # Municipios
    path('municipios/', login_required(views.MunicipioListView.as_view()), name='municipios'),
    path('municipios/crear/', login_required(views.MunicipioCreateView.as_view()), name='municipio_crear'),
    path('municipios/<int:pk>/editar/', login_required(views.MunicipioUpdateView.as_view()), name='municipio_editar'),
    path('municipios/<int:pk>/eliminar/', login_required(views.MunicipioDeleteView.as_view()), name='municipio_eliminar'),
    
    # Localidades
    path('localidades/', login_required(views.LocalidadListView.as_view()), name='localidades'),
    path('localidades/crear/', login_required(views.LocalidadCreateView.as_view()), name='localidad_crear'),
    path('localidades/<int:pk>/editar/', login_required(views.LocalidadUpdateView.as_view()), name='localidad_editar'),
    path('localidades/<int:pk>/eliminar/', login_required(views.LocalidadDeleteView.as_view()), name='localidad_eliminar'),
    
    # Instituciones
    path('instituciones/', login_required(views.InstitucionListView.as_view()), name='instituciones'),
    path('instituciones/crear/', login_required(views.InstitucionCreateView.as_view()), name='institucion_crear'),
    path('instituciones/nueva/', login_required(views.InstitucionCreateView.as_view()), name='institucion_nueva'),
    path('instituciones/<int:pk>/editar/', login_required(views.InstitucionUpdateView.as_view()), name='institucion_editar'),
    path('instituciones/<int:pk>/eliminar/', login_required(views.InstitucionDeleteView.as_view()), name='institucion_eliminar'),
    
    # Dispositivos (compatibilidad)
    path('dispositivos/', login_required(views.InstitucionListView.as_view()), name='dispositivos'),
    path('dispositivos/crear/', login_required(views.InstitucionCreateView.as_view()), name='dispositivo_crear'),
    path('dispositivos/<int:pk>/editar/', login_required(views.InstitucionUpdateView.as_view()), name='dispositivo_editar'),
    path('dispositivos/<int:pk>/eliminar/', login_required(views.InstitucionDeleteView.as_view()), name='dispositivo_eliminar'),
]