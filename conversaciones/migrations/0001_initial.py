# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('anonima', 'Anónima'), ('personal', 'Personal')], max_length=10)),
                ('estado', models.CharField(choices=[('activa', 'Activa'), ('cerrada', 'Cerrada')], default='activa', max_length=10)),
                ('dni_ciudadano', models.CharField(blank=True, max_length=8, null=True)),
                ('fecha_inicio', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('operador_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_inicio'],
            },
        ),
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remitente', models.CharField(choices=[('ciudadano', 'Ciudadano'), ('operador', 'Operador')], max_length=10)),
                ('contenido', models.TextField()),
                ('fecha_envio', models.DateTimeField(default=django.utils.timezone.now)),
                ('leido', models.BooleanField(default=False)),
                ('conversacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mensajes', to='conversaciones.conversacion')),
            ],
            options={
                'ordering': ['fecha_envio'],
            },
        ),
    ]