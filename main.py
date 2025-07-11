from fastapi import FastAPI
from models.models import SQLModel
from settings.database import engine

# from routers.usuario import router as usuario_router
from routers.cliente import router as cliente_router
from routers.auth import router as auth_router

tags_metadata = [
    { "name": "Cliente", "description": "Permite gestionar los clientes" },
    { "name": "Autenticación", "description": "Permite gestión de usuarios y sesiones" }
]

app = FastAPI(
    title="API Gestión de Taller Mecánico",
    description="Documentación de la API para administracion de vehiculos y usuarios",
    version="1.0.1",
    openapi_tags=tags_metadata,
)

# crea las tablas en la base de datos
SQLModel.metadata.create_all(engine)

# incluir cada router por separado
# app.include_router(usuario_router)
app.include_router(cliente_router)
app.include_router(auth_router)
