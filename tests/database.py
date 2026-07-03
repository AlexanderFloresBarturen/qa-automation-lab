from psycopg import connect, sql
from psycopg.errors import DuplicateDatabase
from sqlalchemy.engine.url import make_url

from app.core.settings import settings

"""
Crea la base de datos de prueba en caso de que no exista
"""


def ensure_test_database_exists():
    url = make_url(settings.TEST_DATABASE_URL)

    if url.database is None:
        raise ValueError("TEST_DATABASE_URL must include a database name.")

    database_name = url.database

    with connect(host=url.host, port=url.port, user=url.username, password=url.password, dbname="postgres", autocommit=True) as connection:

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1 FROM pg_database
                WHERE datname = %s
                """,
                (database_name,),
            )

            database_exists = cursor.fetchone() is not None

            if not database_exists:
                print(f"Creating database '{database_name}'...")

                try:
                    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))

                    print(f"Database {database_name} created successfully!")
                except DuplicateDatabase:
                    print(f"Database '{database_name}' already exists.")
            else:
                print(f"Database '{database_name}' already exists.")
