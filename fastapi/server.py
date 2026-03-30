from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

# Importaciones internas del proyecto
from data.database import SessionLocal, engine
from data import models, schemas

# Crear tablas si no existen
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library API",
    description="API para gestionar el catálogo y préstamos de la biblioteca",
    version="1.0.0"
)


# Dependencia: obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ RUTA PRINCIPAL
@app.get("/")
def home():
    return {"message": "Bienvenido a la API de Biblioteca"}


# ✅ OBTENER TODOS LOS LIBROS
@app.get("/books", response_model=list[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books


# ✅ OBTENER LIBRO POR ID
@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return book


# ✅ CREAR LIBRO
@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# ✅ ACTUALIZAR LIBRO
@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated: schemas.BookCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if not book:
