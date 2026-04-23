import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.append(root)

from api.data.database import Base
from api.data.models import Book, User

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

def test_create_book(db_session):
    new_book = Book(title="The Pragmatic Programmer", author="Andrew Hunt", is_available=True)
    db_session.add(new_book)
    db_session.commit()
    db_session.refresh(new_book)
    
    assert new_book.id is not None
    assert new_book.title == "The Pragmatic Programmer"

def test_create_user(db_session):
    new_user = User(name="John Doe", email="john@example.com")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    
    assert new_user.id is not None
    assert new_user.email == "john@example.com"
