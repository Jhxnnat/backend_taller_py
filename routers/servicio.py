from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Servicio, ServicioCrear, Vehiculo
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/servicio",
    tags=["Servicio"],
    # dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: ServicioCrear, session: Session = Depends(get_session)):
    _servicio = Servicio(**item.dict())
    session.add(_servicio)
    session.commit()
    session.refresh(_servicio)
    return ResponseDTO(status="success", message="servicio agregado correctamente", data=_servicio)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Servicio)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(Servicio, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.get("/consultar_vehiculo/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.exec(select(Servicio).where(Servicio.idVehiculo == id))
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.put("/actualizar/{id}")
def update(id: str, updated: Servicio, session: Session = Depends(get_session)):
    item = session.get(Servicio, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    return ResponseDTO(status="success", message="Registro actualizado", data=item) 

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    servicio = session.get(Servicio, id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(servicio)
    session.commit()
    return ResponseDTO(status="success", message="", data=True) 


