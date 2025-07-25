from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Usuario
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuario"]
)

@router.post("/agregar")
def create(item: Usuario, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return ResponseDTO(status="success", message="nuevo usuario agregado correctamente", data=item)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Usuario)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(Usuario, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.put("/actualizar/{id}")
def update(id: str, updated: Usuario, session: Session = Depends(get_session)):
    item = session.get(Usuario, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    return ResponseDTO(status="success", message="Registro actualizado", data=item)

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    usuario = session.get(Usuario, id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(usuario)
    session.commit()
    return ResponseDTO(status="success", message="", data=True)
