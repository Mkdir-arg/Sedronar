from django.urls import path
from . import views

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
    path('<uuid:legajo_id>/evaluacion/', views.EvaluacionInicialView.as_view(), name='evaluacion'),
    path('<uuid:legajo_id>/plan/', views.PlanIntervencionView.as_view(), name='plan'),
    path('<uuid:legajo_id>/seguimiento/', views.SeguimientoCreateView.as_view(), name='seguimiento_nuevo'),
    path('<uuid:legajo_id>/seguimientos/', views.SeguimientoListView.as_view(), name='seguimientos'),
    path('<uuid:legajo_id>/derivacion/', views.DerivacionCreateView.as_view(), name='derivacion_nueva'),
    path('<uuid:legajo_id>/derivaciones/', views.DerivacionListView.as_view(), name='derivaciones'),
    path('<uuid:legajo_id>/evento/', views.EventoCriticoCreateView.as_view(), name='evento_nuevo'),
    path('<uuid:pk>/', views.LegajoDetailView.as_view(), name='detalle'),
    path('<uuid:pk>/cerrar/', views.LegajoCerrarView.as_view(), name='cerrar'),
    path('<uuid:pk>/reabrir/', views.LegajoReabrirView.as_view(), name='reabrir'),
    path('reportes/', views.ReportesView.as_view(), name='reportes'),
    path('exportar-csv/', views.ExportarCSVView.as_view(), name='exportar_csv'),
]