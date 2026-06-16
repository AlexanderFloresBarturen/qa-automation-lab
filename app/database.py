from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:postgres@192.168.56.2:5432/users"

# Crea conexión PostgreSQL
engine = create_engine(DATABASE_URL)

# Crea sesiones para consultas
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Define una clase base para modelos
Base = declarative_base()

