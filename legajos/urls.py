from django.urls import path
from . import views
from . import views_dashboard_simple as views_simple
from . import views_simple_contactos as views_contactos_simple

app_name = 'legajos'

urlpatterns = [
    path('', views.LegajoListView.as_view(), name='lista'),
    path('nuevo/', views.LegajoCreateView.as_view(), name='nuevo'),
    path('ciudadanos/', views.CiudadanoListView.as_view(), name='ciudadanos'),
    path('ciudadanos/nuevo/', views.CiudadanoCreateView.as_view(), name='ciudadano_nuevo'),
    path('ciudadanos/confirmar/', views.CiudadanoConfirmarView.as_view(), name='ciudadano_confirmar'),
    path('ciudadanos/manual/', views.CiudadanoManualView.as_view(), name='ciudadano_manual'),
    path('ciudadanos/<int:pk>/', views.CiudadanoDetailView.as_view(), name='ciudadano_detalle'),
    path('ciudadanos/<int:pk>/editar/', views.CiudadanoUpdateView.as_view(), name='ciudadano_editar'),
    path('admision/paso1/', views.AdmisionPaso1View.as_view(), name='admision_paso1'),
    path('admision/paso2/', views.AdmisionPaso2View.as_view(), name='admision_paso2'),
    path('admision/paso3/', views.AdmisionPaso3View.as_view(), name='admision_paso3'),
    # Evaluaciones
    path('<uuid:legajo_id>/evaluaciones/', views.EvaluacionListView.as_view(), name='evaluaciones'),
    path('<uuid:legajo_id>/evaluacion/', views.EvaluacionInicialView.as_view(), name='evaluacion'),
    
    # Planes de Intervención
    path('<uuid:legajo_id>/planes/', views.PlanListView.as_view(), name='planes'),
    path('<uuid:legajo_id>/plan/', views.PlanIntervencionView.as_view(), name='plan'),
    path('plan/<int:pk>/editar/', views.PlanUpdateView.as_view(), name='plan_editar'),
    
    # Seguimientos
    path('<uuid:legajo_id>/seguimientos/', views.SeguimientoListView.as_view(), name='seguimientos'),
    path('<uuid:legajo_id>/seguimiento/', views.SeguimientoCreateView.as_view(), name='seguimiento_nuevo'),
    path('seguimiento/<int:pk>/editar/', views.SeguimientoUpdateView.as_view(), name='seguimiento_editar'),
    
    # Derivaciones
    path('<uuid:legajo_id>/derivaciones/', views.DerivacionListView.as_view(), name='derivaciones'),
    path('<uuid:legajo_id>/derivacion/', views.DerivacionCreateView.as_view(), name='derivacion_nueva'),
    path('derivacion/<int:pk>/editar/', views.DerivacionUpdateView.as_view(), name='derivacion_editar'),
    
    # Eventos Críticos
    path('<uuid:legajo_id>/eventos/', views.EventoListView.as_view(), name='eventos'),
    path('<uuid:legajo_id>/evento/', views.EventoCriticoCreateView.as_view(), name='evento_nuevo'),
    path('evento/<int:pk>/editar/', views.EventoUpdateView.as_view(), name='evento_editar'),
    path('<uuid:pk>/', views.LegajoDetailView.as_view(), name='detalle'),
    path('<uuid:pk>/cerrar/', views.LegajoCerrarView.as_view(), name='cerrar'),
    path('<uuid:pk>/reabrir/', views.LegajoReabrirView.as_view(), name='reabrir'),
    path('<uuid:pk>/cambiar-responsable/', views.CambiarResponsableView.as_view(), name='cambiar_responsable'),
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
    path('exportar-csv/', views.ExportarCSVView.as_view(), name='exportar_csv'),
    path('dispositivo/<int:dispositivo_id>/derivaciones/', views.DispositivoDerivacionesView.as_view(), name='dispositivo_derivaciones'),
    path('cerrar-alerta/', views.CerrarAlertaEventoView.as_view(), name='cerrar_alerta'),
    
    # Dashboard Contactos
    path('dashboard-contactos/', views_contactos_simple.dashboard_contactos_simple, name='dashboard_contactos'),
    path('test-contactos/', views_simple.dashboard_contactos_simple, name='test_contactos'),
    path('test-api/', views_simple.test_api, name='test_api'),
    
    # Historial de Contactos
    path('<uuid:legajo_id>/historial-contactos/', views_contactos_simple.historial_contactos_simple, name='historial_contactos'),
    
    # Red de Contactos
    path('<uuid:legajo_id>/red-contactos/', views_contactos_simple.red_contactos_simple, name='red_contactos'),
    
    # API Actividades
    path('ciudadanos/<int:ciudadano_id>/actividades/', views_contactos_simple.actividades_ciudadano_api, name='actividades_ciudadano'),
    
    # Subir archivos
    path('<uuid:legajo_id>/subir-archivos/', views_contactos_simple.subir_archivos_legajo, name='subir_archivos'),
    
    # API Archivos
    path('ciudadanos/<int:ciudadano_id>/archivos/', views_contactos_simple.archivos_ciudadano_api, name='archivos_ciudadano'),
    path('archivos/<int:archivo_id>/eliminar/', views_contactos_simple.eliminar_archivo, name='eliminar_archivo'),
    
    # API Alertas
    path('ciudadanos/<int:ciudadano_id>/alertas/', views_contactos_simple.alertas_ciudadano_api, name='alertas_ciudadano'),
    path('alertas/<int:alerta_id>/cerrar/', views_contactos_simple.cerrar_alerta_api, name='cerrar_alerta'),
    
    # Instituciones
    path('instituciones/', views.InstitucionListView.as_view(), name='instituciones'),
    path('instituciones/crear/', views.InstitucionCreateView.as_view(), name='institucion_crear'),
    path('instituciones/<int:pk>/editar/', views.InstitucionUpdateView.as_view(), name='institucion_editar'),
    path('instituciones/<int:pk>/eliminar/', views.InstitucionDeleteView.as_view(), name='institucion_eliminar'),
]