# create_db.py
import MySQLdb
import django
from django.db import connections
from django.conf import settings
import os
# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GestionEvenement.settings')
django.setup()

from django.conf import settings
def create_database_if_not_exists():
    db_settings = settings.DATABASES['default']
    conn = MySQLdb.connect(
        host=db_settings['HOST'],
        user=db_settings['USER'],
        passwd=db_settings['PASSWORD']
    )
    cursor = conn.cursor()
    database_name = db_settings['NAME']
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;")
    conn.close()

if __name__ == '__main__':
    create_database_if_not_exists()
