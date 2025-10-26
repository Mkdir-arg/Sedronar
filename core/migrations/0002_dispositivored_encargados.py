# Generated manually

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispositivored',
            name='encargados',
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={'groups__name': 'EncargadoDispositivo'},
                related_name='dispositivos_encargados',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Encargados del Dispositivo'
            ),
        ),
    ]