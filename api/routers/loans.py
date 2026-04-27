from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..data import models, schemas
from ..dependencies import get_db
from ..exceptions import BookNotFoundError, UserNotFoundError, BookAlreadyBorrowedError
from ..logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/loans",
    tags=["loans"]
)

@router.get("/", response_model=List[schemas.Loan])
def get_loans(db: Session = Depends(get_db)):
    return db.query(models.Loan).all()

@router.post("/", response_model=schemas.Loan)
@log_execution_time
def create_loan(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    # Basic validation
    book = db.query(models.Book).filter(models.Book.id == loan.book_id).first()
    if not book:
        logger.error(f"Intento de préstamo de libro inexistente: ID {loan.book_id}")
        raise BookNotFoundError(loan.book_id)
    
    # Check if book is available
    if not book.is_available:
        logger.warning(f"Intento de préstamo de libro no disponible: ID {book.id} ({book.title})")
        raise BookAlreadyBorrowedError(book.id)
    
    user = db.query(models.User).filter(models.User.id == loan.user_id).first()
    if not user:
        logger.error(f"Intento de préstamo para usuario inexistente: ID {loan.user_id}")
        raise UserNotFoundError(loan.user_id)

    # Process loan
    db_loan = models.Loan(**loan.model_dump())
    
    # Mark book as unavailable
    book.is_available = False
    
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    
    logger.info(f"Préstamo registrado: Libro ID {book.id} a Usuario ID {user.id}")
    return db_loan
