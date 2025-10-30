from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.PortalHomeView.as_view(), name='home'),
    path('crear-usuario/', views.crear_usuario_institucion, name='crear_usuario'),
    path('registro-institucion/', views.registro_institucion, name='registro_institucion'),
    path('consultar-tramite/', views.consultar_tramite, name='consultar_tramite'),
    path('api/municipios/', views.get_municipios, name='get_municipios'),
    path('api/localidades/', views.get_localidades, name='get_localidades'),
]