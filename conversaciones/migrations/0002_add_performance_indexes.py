# Generated manually for performance optimization - MySQL compatible
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('conversaciones', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX idx_conversacion_estado_operador ON conversaciones_conversacion(estado, operador_asignado_id);",
            reverse_sql="DROP INDEX idx_conversacion_estado_operador ON conversaciones_conversacion;"
        ),
        migrations.RunSQL(
            "CREATE INDEX idx_conversacion_fecha_estado ON conversaciones_conversacion(fecha_inicio, estado);",
            reverse_sql="DROP INDEX idx_conversacion_fecha_estado ON conversaciones_conversacion;"
        ),
        migrations.RunSQL(
            "CREATE INDEX idx_mensaje_conversacion_fecha ON conversaciones_mensaje(conversacion_id, fecha_envio);",
            reverse_sql="DROP INDEX idx_mensaje_conversacion_fecha ON conversaciones_mensaje;"
        ),
        migrations.RunSQL(
            "CREATE INDEX idx_mensaje_remitente_leido ON conversaciones_mensaje(remitente, leido);",
            reverse_sql="DROP INDEX idx_mensaje_remitente_leido ON conversaciones_mensaje;"
        ),
    ]