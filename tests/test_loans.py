import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os
from datetime import datetime

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.append(root)

from api.data.database import Base
from api.data.models import Book, User, Loan

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
    book = Book(title="1984", author="George Orwell")
    user = User(name="Alice", email="alice@example.com")
    db_session.add(book)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(book)
    db_session.refresh(user)

    loan = Loan(book_id=book.id, user_id=user.id, loan_date=datetime.utcnow())
    db_session.add(loan)
    db_session.commit()
    db_session.refresh(loan)

    assert loan.id is not None
    assert loan.book_id == book.id
