from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .data.database import engine
from .data import models
from .routers import books, users, loans
from .exceptions import LibraryException, BookNotFoundError, UserNotFoundError

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

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
