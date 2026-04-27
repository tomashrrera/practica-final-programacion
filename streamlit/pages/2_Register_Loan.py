import streamlit as st
from utils.api_client import fetch_books, fetch_users, create_loan

st.set_page_config(page_title="Préstamo de Libros", page_icon="✍️")

st.markdown("# Gestionar Préstamo")
st.write("Selecciona un libro y un usuario para registrar un préstamo.")

# Fetch data for selectboxes (cached)
available_books = [b for b in fetch_books() if b['is_available']]
users = fetch_users()

if not available_books:
    st.warning("⚠️ No hay libros disponibles para préstamo.")
if not users:
    st.info("💡 No hay usuarios registrados en el sistema.")

with st.form("loan_form"):
    # Format options for the selectbox
    book_options = {f"{b['title']} (ID: {b['id']})": b['id'] for b in available_books}
    user_options = {f"{u['name']} (ID: {u['id']})": u['id'] for u in users}

    selected_book_label = st.selectbox("Seleccionar Libro", options=list(book_options.keys()))
    selected_user_label = st.selectbox("Seleccionar Usuario", options=list(user_options.keys()))
    
    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        if not selected_book_label or not selected_user_label:
            st.error("Por favor, selecciona un libro y un usuario.")
        else:
            book_id = book_options[selected_book_label]
            user_id = user_options[selected_user_label]
            
            response = create_loan(book_id, user_id)
            
            if response.status_code == 200:
                st.success("✅ Préstamo registrado correctamente.")
                # Clear cache so the book list updates its availability status
                st.cache_data.clear()
            else:
                error_detail = response.json().get('detail', 'Error desconocido')
                st.error(f"❌ Error: {error_detail}")

st.markdown("---")
if st.button("🔄 Refrescar datos"):
    st.cache_data.clear()
    st.rerun()
