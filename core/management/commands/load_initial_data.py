from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.db import transaction

class Command(BaseCommand):
    help = 'Carga datos iniciales del sistema'
    
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('📦 Cargando datos iniciales...')
        
        # Cargar fixtures
        fixtures = [
            'core/fixtures/dia.json',
            'core/fixtures/mes.json',
            'core/fixtures/sexo.json',
            'core/fixtures/localidad_municipio_provincia.json',
            'chatbot/fixtures/initial_knowledge.json',
            'legajos/fixtures/contactos_initial_data.json',
        ]
        
        for fixture in fixtures:
            try:
                call_command('loaddata', fixture, verbosity=0)
                self.stdout.write(f'✅ {fixture}')
            except Exception as e:
                self.stdout.write(f'⚠️  {fixture}: {str(e)}')
        
        # Crear grupos
        grupos = ['Administrador', 'Responsable', 'Operador', 'Supervisor', 'Consulta']
        for nombre in grupos:
            Group.objects.get_or_create(name=nombre)
        
        # Crear superusuario
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@sisoc.gov.ar', 'admin123')
            self.stdout.write('✅ Superusuario admin creado')
        
        # Crear usuarios por grupo
        usuarios = [
            ('admin1', 'Juan', 'Pérez', 'admin123', 'Administrador', True),
            ('admin2', 'María', 'González', 'admin123', 'Administrador', True),
            ('resp1', 'Ana', 'Martínez', 'resp123', 'Responsable', False),
            ('resp2', 'Luis', 'Rodríguez', 'resp123', 'Responsable', False),
            ('oper1', 'Diego', 'Fernández', 'oper123', 'Operador', False),
            ('oper2', 'Laura', 'Morales', 'oper123', 'Operador', False),
        ]
        
        for username, first, last, pwd, grupo, is_staff in usuarios:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username, f'{username}@sisoc.gov.ar', pwd)
                user.first_name = first
                user.last_name = last
                user.is_staff = is_staff
                user.save()
                user.groups.add(Group.objects.get(name=grupo))
                self.stdout.write(f'✅ Usuario {username} creado')
        
        self.stdout.write(self.style.SUCCESS('✅ Datos cargados'))
