#!/usr/bin/env python
"""
Script to fix migration conflicts by marking migrations as applied
"""
import os
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    from django.db import connection
    
    # Check if actividad_destino_id column exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.columns 
            WHERE table_name='legajos_derivacion' 
            AND column_name='actividad_destino_id'
            AND table_schema=DATABASE()
        """)
        column_exists = cursor.fetchone()[0] > 0
    
    if column_exists:
        print("✅ Column actividad_destino_id already exists")
        print("Marking migration 0006 as applied...")
        
        # Mark migration as applied without running it
        execute_from_command_line(['manage.py', 'migrate', 'legajos', '0006', '--fake'])
        print("✅ Migration conflict resolved")
    else:
        print("❌ Column doesn't exist, running normal migration...")
        execute_from_command_line(['manage.py', 'migrate'])