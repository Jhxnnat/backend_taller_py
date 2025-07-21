from sqlmodel import SQLModel, Column, Field, Relationship
from sqlalchemy import ForeignKey, String, Integer
from typing import Optional, List
from datetime import datetime

# TODO: algunos id deberian ser 'autoincrement'
# para que no se tengan que manejar en la API

class Cliente(SQLModel, table=True):
    idCliente: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, nullable=False)
    apellido: str = Field(max_length=50, nullable=False)
    telefono: str = Field(max_length=15, nullable=False)
    email: Optional[str] = Field(max_length=50)

    vehiculos: List["Vehiculo"] = Relationship(back_populates="cliente")


class Vehiculo(SQLModel, table=True):
    idVehiculo: int = Field(default=None, primary_key=True)
    marca: str = Field(max_length=50, nullable=False)
    modelo: str = Field(max_length=50, nullable=False)
    anio: int = Field(ge=1886, le=datetime.now().year)  # Validación de año
    placa: str = Field(max_length=10, nullable=False)
    idCliente: int = Field(foreign_key="cliente.idCliente", nullable=False)

    cliente: Cliente = Relationship(back_populates="vehiculos")
    servicios: List["Servicio"] = Relationship(back_populates="vehiculo")


class Servicio(SQLModel, table=True):
    idServicio: int = Field(default=None, primary_key=True)
    descripcion: str = Field(max_length=250, nullable=False)
    fecharegistro: datetime = Field(nullable=False)
    estado: Optional[str] = Field(max_length=50)
    idVehiculo: int = Field(foreign_key="vehiculo.idVehiculo", nullable=False)

    vehiculo: Vehiculo = Relationship(back_populates="servicios")
    mecanicos: List["ServicioMecanico"] = Relationship(back_populates="servicio")


class Mecanico(SQLModel, table=True):
    idMecanico: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, nullable=False)
    apellido: str = Field(max_length=50, nullable=False)
    especialidad: str = Field(max_length=50, nullable=False)

    servicios: List["ServicioMecanico"] = Relationship(back_populates="mecanico")


class ServicioMecanico(SQLModel, table=True):
    idServicioMecanico: int = Field(default=None, primary_key=True)
    idServicio: int = Field(foreign_key="servicio.idServicio", nullable=False)
    idMecanico: int = Field(foreign_key="mecanico.idMecanico", nullable=False)

    servicio: Servicio = Relationship(back_populates="mecanicos")
    mecanico: Mecanico = Relationship(back_populates="servicios")


class Factura(SQLModel, table=True):
    idFactura: int = Field(default=None, primary_key=True)
    idServicio: int = Field(foreign_key="servicio.idServicio", nullable=False)
    fechaFactura: datetime = Field(nullable=False)
    montoDescripcion: str = Field(max_length=500, nullable=False)
    montoTotal: float = Field(nullable=False)

    # servicio: Servicio = Relationship(back_populates="factura")
    servicio: Servicio = Relationship()

class Usuario(SQLModel, table=True):
    idUsuario: int = Field(default=None, sa_column=Column(Integer, primary_key=True, autoincrement=True))
    # idUsuario: str = Field(sa_column=Column(String(50), primary_key=True))
    username: str
    password: str
    email: str
    nombres: str
    apellidos: str
    direccion: str
    telefono: str

    # relación uno a uno con RefreshToken
    refresh_token: Optional["RefreshToken"] = Relationship(back_populates="usuario")

class RefreshToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str
    expiryDate: datetime

    usuario_id_usuario: int = Field(sa_column=Column(Integer, ForeignKey("usuario.idUsuario"), unique=True))

    # Relación uno a uno con Usuario
    usuario: "Usuario" = Relationship(back_populates="refresh_token")

class BlackListToken(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    token: str
    expiryDate: datetime
