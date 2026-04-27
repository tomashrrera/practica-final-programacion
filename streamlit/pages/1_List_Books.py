import streamlit as st
import pandas as pd
from utils.api_client import fetch_books

st.set_page_config(page_title="Catálogo de Libros", page_icon="📖")

st.markdown("# Catálogo de Libros")
st.write("Listado de libros disponibles en la biblioteca.")

# Use the cached function from our utility module
libros = fetch_books()

if libros:
    df = pd.DataFrame(libros)
    # Reorder columns for better display
    cols = ["id", "title", "author", "is_available"]
    df = df[cols]
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No hay libros disponibles en este momento.")

if st.button("🔄 Refrescar catálogo"):
    # This clears the cache for this specific function
    st.cache_data.clear()
    st.rerun()
