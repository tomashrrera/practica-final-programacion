import streamlit as st
import requests

# Dirección del servicio FastAPI (en Docker usar "fastapi")
API_URL = "http://fastapi:8000"

st.set_page_config(page_title="Biblioteca", page_icon="📚")

st.title("📚 Biblioteca – Gestión de Libros")



# Helpers


def get_books():
    response = requests.get(f"{API_URL}/books")
    if response.status_code == 200:
        return response.json()
    return []


def create_book(title, author, year):
    payload = {"title": title, "author": author, "year": year}
    return requests.post(f"{API_URL}/books", json=payload)


def update_book(book_id, title, author, year):
    payload = {"title": title, "author": author, "year": year}
    return requests.put(f"{API_URL}/books/{book_id}", json=payload)


def delete_book(book_id):
    return requests.delete(f"{API_URL}/books/{book_id}")



# Sección: Mostrar todos los libros


st.header("📖 Catálogo de libros")

books = get_books()

if not books:
    st.info("No hay libros en la base de datos todavía.")
else:
    for book in books:
        with st.expander(f"{book['title']} – {book['author']} ({book['year']})"):
            st.write(f"**Título:** {book['title']}")
            st.write(f"**Autor:** {book['author']}")
            st.write(f"**Año:** {book['year']}")

            col1, col2 = st.columns(2)

            # Botón eliminar
            if col1.button("🗑️ Eliminar", key=f"del_{book['id']}"):
                delete_book(book["id"])
                st.experimental_rerun()

            # Botón editar
            if col2.button("✏️ Editar", key=f"edit_{book['id']}"):
                st.session_state["edit_book"] = book
                st.experimental_rerun()



# Sección: Crear un libro nuevo


st.header("➕ Añadir un nuevo libro")

with st.form("create_form"):
    title = st.text_input("Título")
    author = st.text_input("Autor")
    year = st.number_input("Año de publicación", min_value=0, max_value=2100, value=2020)

    submitted = st.form_submit_button("Añadir libro")

    if submitted:
        if title.strip() and author.strip():
            response = create_book(title, author, year)
            if response.status_code == 200:
                st.success("✅ Libro añadido correctamente")
                st.experimental_rerun()
            else:
                st.error("❌ Error al añadir el libro")
        else:
            st.warning("⚠️ Todos los campos son obligatorios.")



# Sección: Editar libro existente


if "edit_book" in st.session_state:

    book = st.session_state["edit_book"]

    st.header("✏️ Editar libro")

    with st.form("edit_form"):
        title_edit = st.text_input("Título", value=book["title"])
        author_edit = st.text_input("Autor", value=book["author"])
        year_edit = st.number_input("Año", min_value=0, max_value=2100, value=book["year"])

        submitted_edit = st.form_submit_button("Guardar cambios")

        if submitted_edit:
            update_book(book["id"], title_edit, author_edit, year_edit)
            st.success("✅ Cambios guardados correctamente")
            del st.session_state["edit_book"]
            st.experimental_rerun()

    if st.button("Cancelar edición"):
        del st.session_state["edit_book"]
        st.experimental_rerun()