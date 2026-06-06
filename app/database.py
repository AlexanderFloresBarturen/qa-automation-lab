from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./users.db"

# Crea conexión SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Crea sesiones para consultas
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Define una clase base para modelos
Base = declarative_base()

# Esto crea y cierra sesiones automáticamente por cada request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
