from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models.models import Cliente

router = APIRouter(
    prefix="/mecanico",
    tags=["Mecanico"];
    dependencies=[Depends(get_current_user)]
)

# @router.post("/agregar")
#
# @router.get("/listar")
#
# @router.get("/consultar/{id}")
#
# @router.put("/actualizar/{id}")
#
# @router.delete("/eliminar/{id}")
