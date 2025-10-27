from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from conversaciones.models import Conversacion, Mensaje


class Command(BaseCommand):
    help = 'Configura los grupos de conversaciones con los permisos necesarios'

    def handle(self, *args, **options):
        # Crear grupo Conversaciones
        grupo_conv, created = Group.objects.get_or_create(name='Conversaciones')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "Conversaciones" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('El grupo "Conversaciones" ya existe')
            )
            
        # Crear grupo OperadorCharla
        grupo_op, created = Group.objects.get_or_create(name='OperadorCharla')
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Grupo "OperadorCharla" creado exitosamente')
            )
        else:
            self.stdout.write(
                self.style.WARNING('El grupo "OperadorCharla" ya existe')
            )

        # Obtener content types
        conversacion_ct = ContentType.objects.get_for_model(Conversacion)
        mensaje_ct = ContentType.objects.get_for_model(Mensaje)

        # Permisos necesarios
        permisos_necesarios = [
            # Conversaciones
            f'{conversacion_ct.app_label}.view_conversacion',
            f'{conversacion_ct.app_label}.change_conversacion',
            # Mensajes
            f'{mensaje_ct.app_label}.view_mensaje',
            f'{mensaje_ct.app_label}.add_mensaje',
        ]

        # Asignar permisos a ambos grupos
        for grupo in [grupo_conv, grupo_op]:
            permisos_asignados = 0
            for permiso_codename in permisos_necesarios:
                try:
                    app_label, codename = permiso_codename.split('.')
                    permiso = Permission.objects.get(
                        content_type__app_label=app_label,
                        codename=codename
                    )
                    grupo.permissions.add(permiso)
                    permisos_asignados += 1
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING(f'Permiso no encontrado: {permiso_codename}')
                    )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Se asignaron {permisos_asignados} permisos al grupo "{grupo.name}"'
                )
            )