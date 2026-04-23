import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime

# To avoid shadowing the 'fastapi' library with our local 'fastapi' directory
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root in sys.path:
    sys.path.remove(root)
backend_path = os.path.join(root, "fastapi")
if backend_path not in sys.path:
    sys.path.append(backend_path)
sys.path.append(root)

from data.database import Base
from data.models import Book, User, Loan

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_loan(db_session):
    """
    Test creating a Loan model.
    Should link a Book and a User.
    """
    # Setup: Create a book and a user first
    book = Book(title="1984", author="George Orwell")
    user = User(name="Alice", email="alice@example.com")
    db_session.add(book)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(book)
    db_session.refresh(user)

    # Action: Create a loan
    loan = Loan(book_id=book.id, user_id=user.id, loan_date=datetime.utcnow())
    db_session.add(loan)
    db_session.commit()
    db_session.refresh(loan)

    # Assertions
    assert loan.id is not None
    assert loan.book_id == book.id
    assert loan.user_id == user.id
    assert loan.return_date is None
