from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import time
from sqlalchemy.exc import OperationalError
from .data.database import engine
from .data import models
from .routers import books, users, loans
from .exceptions import LibraryException, BookNotFoundError, UserNotFoundError

# Crear tablas si no existen (con resiliencia al inicio)
max_retries = 5
for i in range(max_retries):
    try:
        models.Base.metadata.create_all(bind=engine)
        print("Tablas verificadas/creadas con éxito en la base de datos.")
        break
    except OperationalError as e:
        if i == max_retries - 1:
            print("No se pudo conectar a la base de datos tras múltiples intentos.")
            raise e
        print(f"Base de datos no lista, reintentando en 5 segundos... ({i+1}/{max_retries})")
        time.sleep(5)

app = FastAPI(
    title="Library API",
    description="API para gestionar el catálogo y préstamos de la biblioteca",
    version="2.1.0"
)

# --- GLOBAL EXCEPTION HANDLERS ---

@app.exception_handler(LibraryException)
async def library_exception_handler(request: Request, exc: LibraryException):
    status_code = 400
    if isinstance(exc, (BookNotFoundError, UserNotFoundError)):
        status_code = 404
    
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message}
    )

# Incluir routers modularizados
app.include_router(books.router)
app.include_router(users.router)
app.include_router(loans.router)

@app.get("/")
def home():
    return {"message": "Bienvenido a la API de Biblioteca (Versión Modular con Excepciones)"}
