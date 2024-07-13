from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Router.Transaction.endpoint import endpoint
from Router.Category.endpoint import category
from Router.funtion.endpoint import funtion


app = FastAPI(title="Control de finanzas", version="1.0")
app.include_router(endpoint, tags=["Crud"])
app.include_router(category, tags=["Manejo de categorias"])
app.include_router(funtion, tags=["Funciones contables"])


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados en las solicitudes
)

@app.get("/Home")
async def root_principal():
    return ("corriendo")