from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


def crear_usuario_con_grupos(username, email, password, grupos=None, is_superuser=False):
    user_model = get_user_model()
    user_qs = user_model.objects.filter(username=username)
    if user_qs.exists():
        user = user_qs.first()
        user.email = email
        user.set_password(password)
        user.save()
        creado = False
    else:
        if is_superuser:
            user = user_model.objects.create_superuser(
                username=username, email=email, password=password
            )
        else:
            user = user_model.objects.create_user(
                username=username, email=email, password=password
            )
        creado = True
    
    # Asignar grupos si es necesario
    if grupos:
        for group_name in grupos:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
    return user, creado


class Command(BaseCommand):
    help = "Crea usuarios básicos de testing solo si DEBUG=True"

    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            self.stdout.write("👥 Creando usuarios para test...")

            usuarios = [
                {
                    "username": "admin",
                    "email": "admin@sedronar.gov.ar",
                    "password": "admin123",
                    "is_superuser": True,
                    "grupos": ["Administrador"],
                },
                {
                    "username": "ciudadanos",
                    "email": "ciudadanos@sedronar.gov.ar",
                    "password": "ciudadanos123",
                    "is_superuser": False,
                    "grupos": ["Ciudadanos"],
                },
            ]

            for conf in usuarios:
                user, creado = crear_usuario_con_grupos(
                    username=conf["username"],
                    email=conf["email"],
                    password=conf["password"],
                    grupos=conf.get("grupos"),
                    is_superuser=conf.get("is_superuser", False),
                )
                tipo = "Superusuario" if conf.get("is_superuser") else "Usuario"
                if creado:
                    self.stdout.write(
                        self.style.SUCCESS(f"{tipo} '{conf['username']}' creado.")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"{tipo} '{conf['username']}' ya existe (actualizado)."
                        )
                    )

            self.stdout.write(self.style.SUCCESS("Proceso completado."))