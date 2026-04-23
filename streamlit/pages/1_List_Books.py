import streamlit as st
import pandas as pd
import requests
import os

st.set_page_config(page_title="Catálogo de Libros", page_icon="📖")

st.markdown("# Catálogo de Libros")
st.write("Listado de libros disponibles en la biblioteca.")

# Configuration from environment variable or default
API_URL = os.getenv("API_URL", "http://fastapi:8000")

try:
    response = requests.get(f"{API_URL}/books")
    if response.status_code == 200:
        libros = response.json()
        
        if libros:
            df = pd.DataFrame(libros)
            # Reorder columns for better display
            cols = ["id", "title", "author", "is_available"]
            df = df[cols]
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No hay libros disponibles.")
    else:
        st.error(f"Error al obtener libros: {response.status_code}")
except Exception as e:
    st.error(f"Error de conexión con el servidor: {e}")
    st.info(f"Intentando conectar a: {API_URL}")
