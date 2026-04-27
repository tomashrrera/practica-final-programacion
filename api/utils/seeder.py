from sqlalchemy.orm import Session
from ..data import models
from ..data.database import SessionLocal, engine
from typing import Generator, Dict, Any

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

def mock_data_generator() -> Generator[Dict[str, Any], None, None]:
    """
    Advanced Generator that yields mock data for the library.
    Demonstrates efficient memory usage by yielding items one by one.
    """
    # Yield some initial books
    books = [
        {"type": "book", "title": "Cien años de soledad", "author": "Gabriel García Márquez"},
        {"type": "book", "title": "Don Quijote de la Mancha", "author": "Miguel de Cervantes"},
        {"type": "book", "title": "El Aleph", "author": "Jorge Luis Borges"},
        {"type": "book", "title": "Rayuela", "author": "Julio Cortázar"},
        {"type": "book", "title": "Crónica de una muerte anunciada", "author": "Gabriel García Márquez"}
    ]
    
    # Yield some initial users
    users = [
        {"type": "user", "name": "Tomas Herrera", "email": "tomas@example.com"},
        {"type": "user", "name": "Maria Garcia", "email": "maria@example.com"},
        {"type": "user", "name": "Juan Perez", "email": "juan@example.com"}
    ]

    for item in books:
        yield item
    
    for item in users:
        yield item

def seed_database():
    """Uses the generator to populate the database."""
    db = SessionLocal()
    print("Iniciando el sembrado de datos (Seeding)...")
    
    count_books = 0
    count_users = 0
    
    try:
        for data in mock_data_generator():
            if data["type"] == "book":
                # Check if book exists (simple check by title)
                exists = db.query(models.Book).filter(models.Book.title == data["title"]).first()
                if not exists:
                    new_book = models.Book(title=data["title"], author=data["author"])
                    db.add(new_book)
                    count_books += 1
            
            elif data["type"] == "user":
                # Check if user exists by email
                exists = db.query(models.User).filter(models.User.email == data["email"]).first()
                if not exists:
                    new_user = models.User(name=data["name"], email=data["email"])
                    db.add(new_user)
                    count_users += 1
        
        db.commit()
        print(f"Éxito: Se han añadido {count_books} libros y {count_users} usuarios.")
    except Exception as e:
        print(f"Error durante el sembrado: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
