from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Factura
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/factura",
    tags=["Factura"],
    # dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: Factura, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return ResponseDTO(status="success", message="factura agregada correctamente", date=item)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Factura)).all())

@router.get("/consultar/{id}")
def get(id: str, session: Session = Depends(get_session)):
    item = session.get(Factura, id)
    if not item:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return ResponseDTO(status="success", message="", data=item)

# NOTE: ¿es necesario actualizar las facturas?
# @router.put("/actualizar/{id}")
# def update(id: str, updated: Factura, session: Session = Depends(get_session)):
#     item = session.get(Factura, id)
#     if not item:
#         raise HTTPException(status_code=404, detail="Registro no encontrado")
#     for key, value in updated.dict(exclude_unset=True).items():
#         setattr(item, key, value)
#     session.add(item)
#     session.commit()
#     return ResponseDTO(status="success", message="Registro actualizado", data=item) 

@router.delete("/eliminar/{id}")
def delete(id: str, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    session.delete(factura)
    session.commit()
    return ResponseDTO(status="success", message="", data=True) 
