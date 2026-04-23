import streamlit as st
import requests
import os
from datetime import datetime

st.set_page_config(page_title="Préstamo de Libros", page_icon="✍️")

st.markdown("# Gestionar Préstamo")
st.write("Formulario para realizar un préstamo.")

API_URL = os.getenv("API_URL", "http://fastapi:8000")

with st.form("loan_form"):
    libro_id = st.number_input("ID del Libro", min_value=1, step=1)
    usuario_id = st.number_input("ID de Usuario", min_value=1, step=1)
    submitted = st.form_submit_button("Realizar Préstamo")

    if submitted:
        payload = {
            "book_id": int(libro_id),
            "user_id": int(usuario_id),
            "loan_date": datetime.utcnow().isoformat()
        }
        
        try:
            response = requests.post(f"{API_URL}/loans", json=payload)
            
            if response.status_code == 200:
                st.success("✅ Préstamo registrado correctamente.")
                st.json(response.json())
            elif response.status_code == 404:
                st.error(f"❌ Error: {response.json().get('detail')}")
            else:
                st.error(f"❌ Error al registrar préstamo: {response.status_code}")
                st.write(response.text)
        except Exception as e:
            st.error(f"Error de conexión: {e}")

st.markdown("---")
st.info("💡 Asegúrate de que tanto el Libro como el Usuario existan en el sistema antes de registrar el préstamo.")
