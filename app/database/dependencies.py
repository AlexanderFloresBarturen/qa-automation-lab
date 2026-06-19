from app.database.connection import SessionLocal

# Esto crea y cierra sesiones automáticamente por cada request
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()