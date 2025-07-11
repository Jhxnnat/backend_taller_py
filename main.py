from fastapi import FastAPI
from models.models import SQLModel
from settings.database import engine

# from routers.usuario import router as usuario_router
from routers.cliente import router as cliente_router
from routers.vehiculo import router as vehiculo_router
from routers.servicio import router as servicio_router
from routers.mecanico import router as mecanico_router
from routers.factura import router as factura_router
from routers.servicio_mecanico import router as servicio_mecanico_router
from routers.auth import router as auth_router

tags_metadata = [
    { "name": "Cliente", "description": "Permite gestionar los clientes" },
    { "name": "Vehiculo", "description": "Permite gestionar los vehiculos" },
    { "name": "Servicio", "description": "Permite gestionar los servicios" },
    { "name": "Mecanico", "description": "Permite gestión de los mecánicos del taller" },
    { "name": "Factura", "description": "Permite gestión de las facturas del taller" },
    { "name": "ServicioMecanico", "description": "Permite gestión de asignaciones de los mecanicos a los servicios" },
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
app.include_router(vehiculo_router)
app.include_router(servicio_router)
app.include_router(mecanico_router)
app.include_router(factura_router)
app.include_router(servicio_mecanico_router)
app.include_router(auth_router)
