import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://fastapi:8000")

@st.cache_data(ttl=60)  # Cache data for 60 seconds
def fetch_books():
    """Fetch all books from the API with caching."""
    try:
        response = requests.get(f"{API_URL}/books/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_users():
    """Fetch all users from the API with caching."""
    try:
        response = requests.get(f"{API_URL}/users/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []

@st.cache_data(ttl=60)
def fetch_loans():
    """Fetch all loans from the API with caching."""
    try:
        response = requests.get(f"{API_URL}/loans/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []

def create_book(title: str, author: str):
    """Send POST request to create a book. (No caching for writes)"""
    return requests.post(f"{API_URL}/books/", json={"title": title, "author": author})

def create_user(name: str, email: str):
    """Send POST request to create a user."""
    return requests.post(f"{API_URL}/users/", json={"name": name, "email": email})

def create_loan(book_id: int, user_id: int):
    """Send POST request to register a loan."""
    payload = {"book_id": book_id, "user_id": user_id}
    return requests.post(f"{API_URL}/loans/", json=payload)
