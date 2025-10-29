from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Ciudadano, LegajoAtencion
from .models_contactos import HistorialContacto, VinculoFamiliar, ContactoEmergencia
from core.models import DispositivoRed, Provincia, Municipio


class ContactosAPITestCase(APITestCase):
    def setUp(self):
        # Crear usuario de prueba
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Crear datos base
        self.provincia = Provincia.objects.create(nombre='Buenos Aires')
        self.municipio = Municipio.objects.create(nombre='La Plata', provincia=self.provincia)
        
        self.dispositivo = DispositivoRed.objects.create(
            tipo='DTC',
            nombre='Dispositivo Test',
            provincia=self.provincia,
            municipio=self.municipio
        )
        
        self.ciudadano = Ciudadano.objects.create(
            dni='12345678',
            nombre='Juan',
            apellido='Pérez'
        )
        
        self.legajo = LegajoAtencion.objects.create(
            ciudadano=self.ciudadano,
            dispositivo=self.dispositivo,
            responsable=self.user
        )
        
        # Autenticar usuario
        self.client.force_authenticate(user=self.user)
    
    def test_crear_historial_contacto(self):
        """Test crear historial de contacto"""
        url = reverse('historialcontacto-list')
        data = {
            'legajo': self.legajo.id,
            'tipo_contacto': 'LLAMADA',
            'fecha_contacto': '2024-01-15T10:00:00Z',
            'profesional': self.user.id,
            'motivo': 'Seguimiento rutinario',
            'resumen': 'Contacto exitoso',
            'estado': 'EXITOSO'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HistorialContacto.objects.count(), 1)
    
    def test_listar_contactos_por_legajo(self):
        """Test filtrar contactos por legajo"""
        # Crear contacto
        HistorialContacto.objects.create(
            legajo=self.legajo,
            tipo_contacto='LLAMADA',
            fecha_contacto='2024-01-15T10:00:00Z',
            profesional=self.user,
            motivo='Test',
            resumen='Test'
        )
        
        url = reverse('historialcontacto-list')
        response = self.client.get(url, {'legajo': self.legajo.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_crear_vinculo_familiar(self):
        """Test crear vínculo familiar"""
        ciudadano2 = Ciudadano.objects.create(
            dni='87654321',
            nombre='María',
            apellido='González'
        )
        
        url = reverse('vinculofamiliar-list')
        data = {
            'ciudadano_principal': self.ciudadano.id,
            'ciudadano_vinculado': ciudadano2.id,
            'tipo_vinculo': 'MADRE',
            'es_contacto_emergencia': True
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VinculoFamiliar.objects.count(), 1)
    
    def test_validacion_vinculo_mismo_ciudadano(self):
        """Test validación de vínculo consigo mismo"""
        url = reverse('vinculofamiliar-list')
        data = {
            'ciudadano_principal': self.ciudadano.id,
            'ciudadano_vinculado': self.ciudadano.id,
            'tipo_vinculo': 'PADRE'
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_crear_contacto_emergencia(self):
        """Test crear contacto de emergencia"""
        url = reverse('contactoemergencia-list')
        data = {
            'legajo': self.legajo.id,
            'nombre': 'María González',
            'relacion': 'Madre',
            'telefono_principal': '1234567890',
            'prioridad': 1
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactoEmergencia.objects.count(), 1)
    
    def test_estadisticas_contactos(self):
        """Test endpoint de estadísticas"""
        # Crear algunos contactos
        HistorialContacto.objects.create(
            legajo=self.legajo,
            tipo_contacto='LLAMADA',
            fecha_contacto='2024-01-15T10:00:00Z',
            profesional=self.user,
            motivo='Test 1',
            resumen='Test 1'
        )
        
        HistorialContacto.objects.create(
            legajo=self.legajo,
            tipo_contacto='EMAIL',
            fecha_contacto='2024-01-16T10:00:00Z',
            profesional=self.user,
            motivo='Test 2',
            resumen='Test 2'
        )
        
        url = reverse('historialcontacto-estadisticas')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_contactos'], 2)
        self.assertIn('por_tipo', response.data)
        self.assertIn('por_estado', response.data)