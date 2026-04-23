import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Ensure the fastapi directory is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.data.database import Base
from fastapi.data.models import Book, User

# In-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture that creates a fresh in-memory database for each test.
    Following the Dependency Inversion Principle by using an abstracted session.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create the tables in the in-memory database
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_book(db_session):
    """
    Test creating a Book model.
    Verifies SRP: The model strictly handles Book data persistence.
    Attributes: id, title, author, is_available
    """
    new_book = Book(title="The Pragmatic Programmer", author="Andrew Hunt", is_available=True)
    db_session.add(new_book)
    db_session.commit()
    db_session.refresh(new_book)
    
    assert new_book.id is not None
    assert new_book.title == "The Pragmatic Programmer"
    assert new_book.author == "Andrew Hunt"
    assert new_book.is_available is True

def test_create_user(db_session):
    """
    Test creating a User model.
    Verifies SRP: The model strictly handles User data persistence.
    Attributes: id, name, email
    """
    new_user = User(name="John Doe", email="john@example.com")
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    
    assert new_user.id is not None
    assert new_user.name == "John Doe"
    assert new_user.email == "john@example.com"
