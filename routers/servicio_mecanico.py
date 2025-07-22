from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import ServicioMecanico, ServicioMecanicoCrear
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/servicio_mecanico",
    tags=["ServicioMecanico"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: ServicioMecanicoCrear, session: Session = Depends(get_session)):
    _servicio_mecanico = ServicioMecanico(**item.dict())
    session.add(item)
    session.commit()
    session.refresh(item)
    return ResponseDTO(status="success", message="servicio mecanico agregado correctamente", date=item)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(ServicioMecanico)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(ServicioMecanico, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.put("/actualizar/{id}")
def update(id: str, updated: ServicioMecanico, session: Session = Depends(get_session)):
    item = session.get(ServicioMecanico, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    return ResponseDTO(status="success", message="Registro actualizado", data=item) 

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    servicio_mecanico = session.get(ServicioMecanico, id)
    if not servicio_mecanico:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(servicio_mecanico)
    session.commit()
    return ResponseDTO(status="success", message="", data=True) 


