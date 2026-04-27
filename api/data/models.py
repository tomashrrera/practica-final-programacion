from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
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

    # Relationships
    loans = relationship("Loan", back_populates="book")

class User(Base):
    """
    User model representing a library member.
    Adheres to SRP by only handling user-related data.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relationships
    loans = relationship("Loan", back_populates="user")

class Loan(Base):
    """
    Loan model representing a book borrowed by a user.
    Adheres to SRP by only handling loan-related data.
    """
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    # Relationships
    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")

    @property
    def is_active(self) -> bool:
        """Check if the loan is currently active."""
        return self.return_date is None
"User", back_populates="loans")
return_date = Column(DateTime, nullable=True)

    # Relationships
    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")
