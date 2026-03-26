import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class BaseModelo(BaseModel):
    class Config:
        arbitrary_types_allowed = True

class Libro(BaseModelo):
    id: int
    titulo: str
    autor: str
    genero: str
    disponible: bool

class ListadoLibros(BaseModelo):
    libros: List[Libro] = []

app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="1.0.0"
)

@app.get("/libros/")
def retrieve_data():
    # EDUCATIONAL WARNING: Esto es ineficiente. Cada request vuelve a leer CSV.
    # Deberíais migrarlo a BD más adelante.

    try:
        todosmisdatos = pd.read_csv('./books.csv', sep=';')
        todosmisdatos = todosmisdatos.fillna(0)
        todosmisdatosdict = todosmisdatos.to_dict(orient='records')

        listado = ListadoLibros()
        listado.libros = todosmisdatosdict

        return listado

    except Exception as e:
        return {"error": str(e)}

@app.post("/prestamos/")
async def create_loan(libro_id: int):
    # Mock de un préstamo real
    return {"message": "Préstamo creado (no realmente)", "libro_id": libro_id}