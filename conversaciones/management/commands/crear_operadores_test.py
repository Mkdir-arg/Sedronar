from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from conversaciones.services import AsignadorAutomatico


class Command(BaseCommand):
    help = 'Crea operadores de prueba para el sistema de conversaciones'

    def handle(self, *args, **options):
        # Crear grupo de operadores si no existe
        grupo_operadores, created = Group.objects.get_or_create(name='OperadorCharla')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo OperadorCharla creado'))

        # Crear operadores de prueba
        operadores_data = [
            {'username': 'operador1', 'first_name': 'Juan', 'last_name': 'Pérez', 'email': 'operador1@sedronar.gov.ar'},
            {'username': 'operador2', 'first_name': 'María', 'last_name': 'González', 'email': 'operador2@sedronar.gov.ar'},
            {'username': 'operador3', 'first_name': 'Carlos', 'last_name': 'López', 'email': 'operador3@sedronar.gov.ar'},
        ]

        for data in operadores_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                    'email': data['email'],
                    'is_active': True,
                    'is_staff': True
                }
            )
            
            if created:
                user.set_password('operador123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario {user.username} creado'))
            
            # Agregar al grupo
            user.groups.add(grupo_operadores)
            
            # Configurar en el sistema de cola
            cola = AsignadorAutomatico.configurar_operador(user, max_conversaciones=3, activo=True)
            self.stdout.write(self.style.SUCCESS(f'Operador {user.get_full_name()} configurado en cola'))

        self.stdout.write(self.style.SUCCESS('Operadores de prueba creados exitosamente'))
        self.stdout.write(self.style.WARNING('Contraseña para todos: operador123'))