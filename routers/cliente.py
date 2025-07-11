from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Cliente
from settings.ResponseDTO import ResponseDTO
from settings.auth import get_current_user
from settings.database import get_session

router = APIRouter(
    prefix="/clientes",
    tags=["Cliente"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/agregar")
def create(item: Cliente, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return ResponseDTO(status="success", message="cliente agregado correctamente", date=item)

@router.get("/listar")
def get_all(session: Session = Depends(get_session)):
    return ResponseDTO(status="success", message="", data=session.exec(select(Cliente)).all())

# @router.get("/consultar/{id}")
#
# @router.put("/actualizar/{id}")
#
# @router.delete("/eliminar/{id}")
