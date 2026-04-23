import pytest
import sys
import os

# To avoid shadowing the 'fastapi' library with our local 'fastapi' directory,
# we ensure the library path takes precedence by moving the root to the end of sys.path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root in sys.path:
    sys.path.remove(root)
# Add backend code to path but NOT at the beginning
backend_path = os.path.join(root, "fastapi")
if backend_path not in sys.path:
    sys.path.append(backend_path)
# Add root at the end just in case
sys.path.append(root)

from fastapi.testclient import TestClient
import server
from data import models, database, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Test Database setup - Using StaticPool for in-memory SQLite to persist data across connections
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

server.app.dependency_overrides[server.get_db] = override_get_db

client = TestClient(server.app)

@pytest.fixture(autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=test_engine)
    yield
    models.Base.metadata.drop_all(bind=test_engine)

# --- Book Tests ---

def test_delete_book():
    # Create a book first
    response = client.post("/books", json={"title": "Delete Me", "author": "Unknown"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    
    # Delete it
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404

# --- User Tests ---

def test_create_user():
    response = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert "id" in data

def test_get_users():
    client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 1

# --- Loan Tests ---

def test_register_loan():
    # Setup: Create book and user
    res_book = client.post("/books", json={"title": "1984", "author": "George Orwell"})
    res_user = client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    
    assert res_book.status_code == 200
    assert res_user.status_code == 200
    
    book_id = res_book.json()["id"]
    user_id = res_user.json()["id"]
    
    # Action: Register loan
    response = client.post("/loans", json={"book_id": book_id, "user_id": user_id})
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["user_id"] == user_id
    assert data["return_date"] is None
