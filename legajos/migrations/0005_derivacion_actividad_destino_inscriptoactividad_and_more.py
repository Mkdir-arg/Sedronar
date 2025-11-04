from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def check_column_exists(apps, schema_editor):
    """Verifica si la columna actividad_destino_id ya existe"""
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name='legajos_derivacion' 
            AND column_name='actividad_destino_id'
            AND table_schema=DATABASE()
        """)
        return cursor.fetchone()[0] > 0


def add_field_if_not_exists(apps, schema_editor):
    """Agrega el campo solo si no existe"""
    if not check_column_exists(apps, schema_editor):
        Derivacion = apps.get_model('legajos', 'Derivacion')
        schema_editor.add_field(
            Derivacion,
            models.ForeignKey(
                blank=True, 
                null=True, 
                on_delete=django.db.models.deletion.SET_NULL, 
                related_name='derivaciones', 
                to='legajos.planfortalecimiento', 
                verbose_name='Actividad Específica'
            )
        )


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('legajos', '0004_alter_planfortalecimiento_options_and_more'),
    ]

    operations = [
        migrations.RunPython(add_field_if_not_exists, migrations.RunPython.noop),
        migrations.CreateModel(
            name='InscriptoActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(choices=[('INSCRITO', 'Inscrito'), ('ACTIVO', 'Activo'), ('FINALIZADO', 'Finalizado'), ('ABANDONADO', 'Abandonado')], default='INSCRITO', max_length=20)),
                ('fecha_inscripcion', models.DateField(auto_now_add=True)),
                ('fecha_finalizacion', models.DateField(blank=True, null=True)),
                ('observaciones', models.TextField(blank=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptos', to='legajos.planfortalecimiento')),
                ('ciudadano', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actividades_inscrito', to='legajos.ciudadano')),
            ],
            options={
                'verbose_name': 'Inscripto en Actividad',
                'verbose_name_plural': 'Inscriptos en Actividades',
                'ordering': ['-fecha_inscripcion'],
                'unique_together': {('actividad', 'ciudadano')},
            },
        ),
        migrations.CreateModel(
            name='HistorialStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('accion', models.CharField(choices=[('ASIGNACION', 'Asignación'), ('DESASIGNACION', 'Desasignación'), ('CAMBIO_ROL', 'Cambio de Rol')], max_length=20)),
                ('descripcion', models.TextField()),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='legajos.staffactividad')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historial de Staff',
                'verbose_name_plural': 'Historiales de Staff',
                'ordering': ['-creado'],
            },
        ),
        migrations.CreateModel(
            name='HistorialInscripto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('accion', models.CharField(choices=[('INSCRIPCION', 'Inscripción'), ('ACTIVACION', 'Activación'), ('FINALIZACION', 'Finalización'), ('ABANDONO', 'Abandono')], max_length=20)),
                ('descripcion', models.TextField()),
                ('estado_anterior', models.CharField(blank=True, max_length=20)),
                ('inscripto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='legajos.inscriptoactividad')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historial de Inscripto',
                'verbose_name_plural': 'Historiales de Inscriptos',
                'ordering': ['-creado'],
            },
        ),
        migrations.CreateModel(
            name='HistorialDerivacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('accion', models.CharField(choices=[('CREACION', 'Creación'), ('ACEPTACION', 'Aceptación'), ('RECHAZO', 'Rechazo')], max_length=20)),
                ('descripcion', models.TextField()),
                ('estado_anterior', models.CharField(blank=True, max_length=20)),
                ('derivacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='legajos.derivacion')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historial de Derivación',
                'verbose_name_plural': 'Historiales de Derivaciones',
                'ordering': ['-creado'],
            },
        ),
        migrations.CreateModel(
            name='HistorialActividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('modificado', models.DateTimeField(auto_now=True)),
                ('accion', models.CharField(choices=[('CREACION', 'Creación'), ('MODIFICACION', 'Modificación'), ('SUSPENSION', 'Suspensión'), ('FINALIZACION', 'Finalización'), ('REACTIVACION', 'Reactivación')], max_length=20)),
                ('descripcion', models.TextField()),
                ('datos_anteriores', models.JSONField(blank=True, null=True)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historial', to='legajos.planfortalecimiento')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Historial de Actividad',
                'verbose_name_plural': 'Historiales de Actividades',
                'ordering': ['-creado'],
            },
        ),
    ]