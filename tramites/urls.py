from django.urls import path
from . import views

app_name = 'tramites'

urlpatterns = [
    path('', views.lista_tramites, name='lista_tramites'),
    path('<int:tramite_id>/', views.detalle_tramite, name='detalle_tramite'),
    path('<int:tramite_id>/aprobar/', views.aprobar_tramite, name='aprobar_tramite'),
    path('<int:tramite_id>/rechazar/', views.rechazar_tramite, name='rechazar_tramite'),
]