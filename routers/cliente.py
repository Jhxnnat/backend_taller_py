from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Cliente, ClienteCrear
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/clientes",
    tags=["Cliente"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: ClienteCrear, session: Session = Depends(get_session)):
    _cliente = Cliente(**item.dict())
    session.add(_cliente)
    session.commit()
    session.refresh(_cliente)
    return ResponseDTO(status="success", message="cliente agregado correctamente", data=_cliente)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Cliente)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(Cliente, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

@router.put("/actualizar/{id}")
def update(id: str, updated: Cliente, session: Session = Depends(get_session)):
    item = session.get(Cliente, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(item, key, value)
    session.add(item)
    session.commit()
    return ResponseDTO(status="success", message="Registro actualizado", data=item) 

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(cliente)
    session.commit()
    return ResponseDTO(status="success", message="", data=True) 


