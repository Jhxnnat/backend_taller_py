from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from models.models import SQLModel
from settings.database import engine

from routers import cliente
from routers import vehiculo
from routers import servicio
from routers import mecanico
from routers import factura
from routers import servicio_mecanico
from routers import usuario
from routers import auth

tags_metadata = [
    { "name": "Cliente", "description": "Permite gestionar los clientes" },
    { "name": "Vehiculo", "description": "Permite gestionar los vehiculos" },
    { "name": "Servicio", "description": "Permite gestionar los servicios" },
    { "name": "Mecanico", "description": "Permite gestión de los mecánicos del taller" },
    { "name": "Factura", "description": "Permite gestión de las facturas del taller" },
    { "name": "ServicioMecanico", "description": "Permite gestión de asignaciones de los mecanicos a los servicios" },
    # { "name": "Usuario", "description": "Permite gestión de los usuarios (administradores) del taller" },
    { "name": "Autenticación", "description": "Permite gestión de usuarios y sesiones" }
]

def get_application():
    _app = FastAPI(
        title="API Gestión de Taller Mecánico",
        description="Documentación de la API para administracion de vehiculos y usuarios",
        version="1.0.1",
        openapi_tags=tags_metadata,
    )
    _app.include_router(cliente.router)
    _app.include_router(vehiculo.router)
    _app.include_router(servicio.router)
    _app.include_router(mecanico.router)
    _app.include_router(factura.router)
    _app.include_router(servicio_mecanico.router)
    # _app.include_router(usuario.router)
    _app.include_router(auth.router)

    origins = [
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app

app = get_application()

@app.get("/")
def test_connection():
    return {"status": "ok"}

def main():
    SQLModel.metadata.create_all(engine)
    uvicorn.run("main:app", reload=True)

if __name__ == "__main__":
    main()

