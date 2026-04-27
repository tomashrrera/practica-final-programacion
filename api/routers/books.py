from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..data import models, schemas
from ..dependencies import get_db
from ..exceptions import BookNotFoundError
from ..logger import log_execution_time

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=List[schemas.Book])
@log_execution_time
def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)
    return book

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, updated: schemas.BookCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)
    
    for key, value in updated.model_dump().items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise BookNotFoundError(book_id)
    
    db.delete(book)
    db.commit()
    return {"message": "Libro eliminado correctamente"}
