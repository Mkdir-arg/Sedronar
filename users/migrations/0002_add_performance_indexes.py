# Generated manually for performance optimization
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            "CREATE INDEX idx_user_is_active_last_login ON auth_user(is_active, last_login);",
            reverse_sql="DROP INDEX idx_user_is_active_last_login ON auth_user;"
        ),
        migrations.RunSQL(
            "CREATE INDEX idx_user_groups_user_group ON auth_user_groups(user_id, group_id);",
            reverse_sql="DROP INDEX idx_user_groups_user_group ON auth_user_groups;"
        ),
    ]