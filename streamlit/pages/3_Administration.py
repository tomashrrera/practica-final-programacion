import streamlit as st
from utils.api_client import create_book, create_user

st.set_page_config(page_title="Administración", page_icon="⚙️")

st.markdown("# Administración del Sistema")

tab1, tab2 = st.tabs(["🆕 Registrar Libro", "👥 Registrar Usuario"])

with tab1:
    st.header("Añadir nuevo libro al catálogo")
    with st.form("add_book_form"):
        title = st.text_input("Título")
        author = st.text_input("Autor")
        submit_book = st.form_submit_button("Guardar Libro")
        
        if submit_book:
            if title and author:
                res = create_book(title, author)
                if res.status_code == 200:
                    st.success(f"Libro '{title}' añadido con éxito.")
                    st.cache_data.clear() # Clear cache to show the new book in lists
                else:
                    st.error(f"Error: {res.status_code}")
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
                res = create_user(name, email)
                if res.status_code == 200:
                    st.success(f"Usuario '{name}' registrado con éxito.")
                    st.cache_data.clear() # Clear cache to show the new user in lists
                else:
                    error_detail = res.json().get('detail', 'Error desconocido')
                    st.error(f"❌ Error: {error_detail}")
            else:
                st.warning("Por favor, rellena todos los campos.")
