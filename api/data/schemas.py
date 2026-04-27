from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime

class BookBase(BaseModel):
    title: str
    author: str
    is_available: bool = True

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    status: str
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class LoanBase(BaseModel):
    book_id: int
    user_id: int
    loan_date: datetime = datetime.utcnow()
    return_date: Optional[datetime] = None

class LoanCreate(LoanBase):
    pass

class Loan(LoanBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
ue)
ig = ConfigDict(from_attributes=True)
