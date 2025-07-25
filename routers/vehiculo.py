from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Vehiculo, VehiculoCrear
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/vehiculo",
    tags=["Vehiculo"],
    # dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: VehiculoCrear, session: Session = Depends(get_session)):
    _vehiculo = Vehiculo(**item.dict())
    session.add(_vehiculo)
    session.commit()
    session.refresh(_vehiculo)
    return ResponseDTO(status="success", message="vehiculo agregado correctamente", data=_vehiculo)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Vehiculo)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(Vehiculo, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.put("/actualizar/{id}")
def update(id: str, updated: Vehiculo, session: Session = Depends(get_session)):
    item = session.get(Vehiculo, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    return ResponseDTO(status="success", message="Registro actualizado", data=item) 

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    vehiculo = session.get(Vehiculo, id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(vehiculo)
    session.commit()
    return ResponseDTO(status="success", message="", data=True) 
