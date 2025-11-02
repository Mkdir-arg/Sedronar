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
    path('instituciones/<int:pk>/', login_required(views.InstitucionDetailView.as_view()), name='institucion_detalle'),
    
    # Gestión de legajo institucional
    path('instituciones/<int:institucion_pk>/personal/crear/', login_required(views.PersonalInstitucionCreateView.as_view()), name='personal_crear'),
    path('instituciones/<int:institucion_pk>/evaluaciones/crear/', login_required(views.EvaluacionInstitucionCreateView.as_view()), name='evaluacion_crear'),
    path('instituciones/<int:institucion_pk>/planes/crear/', login_required(views.PlanFortalecimientoCreateView.as_view()), name='plan_crear'),
    path('instituciones/<int:institucion_pk>/indicadores/crear/', login_required(views.IndicadorInstitucionCreateView.as_view()), name='indicador_crear'),
    
    # Dispositivos (compatibilidad)
    path('dispositivos/', login_required(views.InstitucionListView.as_view()), name='dispositivos'),
    path('dispositivos/crear/', login_required(views.InstitucionCreateView.as_view()), name='dispositivo_crear'),
    path('dispositivos/<int:pk>/editar/', login_required(views.InstitucionUpdateView.as_view()), name='dispositivo_editar'),
    path('dispositivos/<int:pk>/eliminar/', login_required(views.InstitucionDeleteView.as_view()), name='dispositivo_eliminar'),
]