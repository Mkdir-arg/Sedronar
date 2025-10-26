# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('legajos', '0005_create_responsable_group'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlertaEventoCritico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('modificado', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('fecha_cierre', models.DateTimeField(auto_now_add=True)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alertas_vistas', to='legajos.eventocritico')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alertas_eventos_vistas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Alerta Evento Crítico',
                'verbose_name_plural': 'Alertas Eventos Críticos',
                'indexes': [models.Index(fields=['responsable', 'fecha_cierre'], name='legajos_ale_respons_b8b8b8_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='alertaeventocritico',
            constraint=models.UniqueConstraint(fields=('evento', 'responsable'), name='legajos_alertaeventocritico_evento_id_responsable_id_uniq'),
        ),
    ]