import pytest
import sys
import os

# Now that the folder is renamed to 'api', we can simply add the project root
# and import things normally without shadowing conflicts.
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.append(root)

from fastapi.testclient import TestClient
from api import server
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

server.app.dependency_overrides[server.get_db] = override_get_db

client = TestClient(server.app)

@pytest.fixture(autouse=True)
def setup_db():
    models.Base.metadata.create_all(bind=test_engine)
    yield
    models.Base.metadata.drop_all(bind=test_engine)

# --- Book Tests ---

def test_delete_book():
    response = client.post("/books", json={"title": "Delete Me", "author": "Unknown"})
    assert response.status_code == 200
    book_id = response.json()["id"]
    
    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    
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
    res_book = client.post("/books", json={"title": "1984", "author": "George Orwell"})
    res_user = client.post("/users", json={"name": "Bob", "email": "bob@example.com"})
    
    assert res_book.status_code == 200
    assert res_user.status_code == 200
    
    book_id = res_book.json()["id"]
    user_id = res_user.json()["id"]
    
    response = client.post("/loans", json={"book_id": book_id, "user_id": user_id})
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["user_id"] == user_id
    assert data["return_date"] is None
