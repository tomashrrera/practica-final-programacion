import pytest
import sys
import os

# Now that the folder is renamed to 'api', we can simply add the project root
# and import things normally without shadowing conflicts.
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.append(root)

from fastapi.testclient import TestClient
from api import server, dependencies
from api.data import models, database, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Test Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

server.app.dependency_overrides[dependencies.get_db] = override_get_db

client = TestClient(server.app)

@pytest.fixture(autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=test_engine)
    yield
    models.Base.metadata.drop_all(bind=test_engine)

# --- Book Tests ---

def test_delete_book():
    response = client.post("/books/", json={"title": "Delete Me", "author": "Unknown"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404

def test_book_not_found():
    """Test that custom exception handler works."""
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Libro con ID 999 no encontrado"

# --- User Tests ---

def test_create_user():
    response = client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data

def test_get_users():
    client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1

# --- Loan Tests ---

def test_register_loan():
    res_book = client.post("/books/", json={"title": "1984", "author": "George Orwell"})
    res_user = client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})
    
    assert res_book.status_code == 200
    assert res_user.status_code == 200
    
    book_id = res_book.json()["id"]
    user_id = res_user.json()["id"]
    
    response = client.post("/loans/", json={"book_id": book_id, "user_id": user_id})
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["user_id"] == user_id
    assert data["return_date"] is None
    
    # Verify book is now unavailable
    res_get_book = client.get(f"/books/{book_id}")
    assert res_get_book.json()["is_available"] is False

def test_loan_unavailable_book():
    # Setup: Create book, user, and initial loan
    res_book = client.post("/books/", json={"title": "1984", "author": "George Orwell"})
    res_user1 = client.post("/users/", json={"name": "Alice", "email": "alice@example.com"})
    res_user2 = client.post("/users/", json={"name": "Bob", "email": "bob@example.com"})
    
    book_id = res_book.json()["id"]
    user1_id = res_user1.json()["id"]
    user2_id = res_user2.json()["id"]
    
    # First loan
    client.post("/loans/", json={"book_id": book_id, "user_id": user1_id})
    
    # Second loan attempt (same book)
    response = client.post("/loans/", json={"book_id": book_id, "user_id": user2_id})
    assert response.status_code == 400
    assert response.json()["detail"] == f"El libro con ID {book_id} ya se encuentra prestado"
