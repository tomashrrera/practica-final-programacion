from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importaciones internas del proyecto
from .data.database import SessionLocal, engine
from .data import models, schemas

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


# --- BOOKS ENDPOINTS ---

@app.get("/books", response_model=List[schemas.Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated: schemas.BookCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    for key, value in updated.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    db.delete(book)
    db.commit()
    return {"message": "Libro eliminado correctamente"}


# --- USERS ENDPOINTS ---

@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- LOANS ENDPOINTS ---

@app.get("/loans", response_model=List[schemas.Loan])
def get_loans(db: Session = Depends(get_db)):
    return db.query(models.Loan).all()


@app.post("/loans", response_model=schemas.Loan)
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # Basic validation: check if book and user exist
    book = db.query(models.Book).filter(models.Book.id == loan.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    user = db.query(models.User).filter(models.User.id == loan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db_loan = models.Loan(**loan.model_dump())
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan
