from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Mecanico, MecanicoCrear
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/mecanico",
    tags=["Mecanico"],
    # dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: MecanicoCrear, session: Session = Depends(get_session)):
    _mecanico = Mecanico(**item.dict())
    session.add(_mecanico)
    session.commit()
    session.refresh(_mecanico)
    return ResponseDTO(status="success", message="mecanico agregado correctamente", data=_mecanico)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Mecanico)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(Mecanico, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.put("/actualizar/{id}")
def update(id: str, updated: Mecanico, session: Session = Depends(get_session)):
    item = session.get(Mecanico, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    return ResponseDTO(status="success", message="Registro actualizado", data=item) 

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    mecanico = session.get(Mecanico, id)
    if not mecanico:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(mecanico)
    session.commit()
    return ResponseDTO(status="success", message="", data=True) 


