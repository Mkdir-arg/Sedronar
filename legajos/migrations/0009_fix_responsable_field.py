# Generated manually

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('legajos', '0008_remove_alertaeventocritico_legajos_alertaeventocritico_evento_id_responsable_id_uniq_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='legajoatencion',
            name='responsable',
            field=models.ForeignKey(blank=True, help_text='Usuario con rol de Responsable asignado al legajo', limit_choices_to={'groups__name': 'Responsable'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='legajos_atencion_responsable', to=settings.AUTH_USER_MODEL, verbose_name='Responsable'),
        ),
    ]