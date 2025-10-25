# Generated manually

from django.db import migrations


def create_responsable_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.get_or_create(name='Responsable')


def reverse_operations(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Responsable').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('legajos', '0004_objetivo_seguimientocontacto_planintervencion_and_more'),
    ]

    operations = [
        migrations.RunPython(create_responsable_group, reverse_operations),
    ]