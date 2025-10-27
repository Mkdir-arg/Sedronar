# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversaciones', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversacion',
            name='sexo_ciudadano',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
    ]