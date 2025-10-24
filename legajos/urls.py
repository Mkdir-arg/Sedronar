from django.urls import path
from . import views

app_name = 'legajos'

urlpatterns = [
    path('', views.LegajoListView.as_view(), name='lista'),
    path('ciudadanos/', views.CiudadanoListView.as_view(), name='ciudadanos'),
    path('ciudadanos/nuevo/', views.CiudadanoCreateView.as_view(), name='ciudadano_nuevo'),
    path('ciudadanos/<int:pk>/', views.CiudadanoDetailView.as_view(), name='ciudadano_detalle'),
    path('ciudadanos/<int:pk>/editar/', views.CiudadanoUpdateView.as_view(), name='ciudadano_editar'),
    path('nuevo/', views.LegajoCreateView.as_view(), name='nuevo'),
    path('<uuid:pk>/', views.LegajoDetailView.as_view(), name='detalle'),
]