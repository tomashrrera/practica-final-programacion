from pydantic import BaseModel, EmailStr
from typing import Optional

class BookBase(BaseModel):
    title: str
    author: str
    is_available: bool = True

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
