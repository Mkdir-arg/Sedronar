from django.urls import path
from . import views

app_name = 'legajos'

urlpatterns = [
    path('', views.LegajoListView.as_view(), name='lista'),
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
    path('<uuid:pk>/', views.LegajoDetailView.as_view(), name='detalle'),
]