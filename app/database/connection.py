from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.settings import settings

# Crea conexión PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Crea sesiones para consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define una clase base para modelos
Base = declarative_base()
