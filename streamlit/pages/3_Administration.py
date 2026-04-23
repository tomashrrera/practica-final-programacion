import streamlit as st
import requests
import os

st.set_page_config(page_title="Administración", page_icon="⚙️")

st.markdown("# Administración del Sistema")
API_URL = os.getenv("API_URL", "http://fastapi:8000")

tab1, tab2 = st.tabs(["🆕 Registrar Libro", "👥 Registrar Usuario"])

with tab1:
    st.header("Añadir nuevo libro al catálogo")
    with st.form("add_book_form"):
        title = st.text_input("Título")
        author = st.text_input("Autor")
        submit_book = st.form_submit_button("Guardar Libro")
        
        if submit_book:
            if title and author:
                try:
                    res = requests.post(f"{API_URL}/books", json={"title": title, "author": author})
                    if res.status_code == 200:
                        st.success(f"Libro '{title}' añadido con éxito.")
                    else:
                        st.error(f"Error: {res.status_code}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
            else:
                st.warning("Por favor, rellena todos los campos.")

with tab2:
    st.header("Registrar nuevo usuario")
    with st.form("add_user_form"):
        name = st.text_input("Nombre Completo")
        email = st.text_input("Email")
        submit_user = st.form_submit_button("Guardar Usuario")
        
        if submit_user:
            if name and email:
                try:
                    res = requests.post(f"{API_URL}/users", json={"name": name, "email": email})
                    if res.status_code == 200:
                        st.success(f"Usuario '{name}' registrado con éxito.")
                    else:
                        st.error(f"Error: {res.status_code}")
                        st.write(res.text)
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
            else:
                st.warning("Por favor, rellena todos los campos.")
