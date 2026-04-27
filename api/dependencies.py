from .data.database import SessionLocal
from .logger import get_logger

logger = get_logger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error crítico en la conexión con la base de datos: {e}")
        raise
    finally:
        db.close()
