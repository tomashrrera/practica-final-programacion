from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Book(Base):
    """
    Book model representing a library resource.
    Adheres to SRP by only handling book-related data.
    """
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, index=True, nullable=False)
    is_available = Column(Boolean, default=True)

class User(Base):
    """
    User model representing a library member.
    Adheres to SRP by only handling user-related data.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
