from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Body, Query
from sqlmodel import Session, select
from models.models import BlackListToken, Usuario, RefreshToken
from settings.ResponseDTO import ResponseDTO
from settings.auth import ALGORITHM, SECRET_KEY, create_token
from settings.database import get_session
from settings.password_utils import PasswordUtils
from settings.database import engine
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"]
)

REFRESH_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_MINUTES = 60

@router.post("/login", summary="Autenticación")
async def login(
    username: str = Query(..., description="username"),
    password: str = Query(..., description="password"),
    session: Session = Depends(get_session)):
    
    try:
        # Aquí deberías implementar la lógica de autenticación real
        usuario = session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

        # if not usuario or usuario.password != PasswordUtils.hash_password(password):
        #     raise HTTPException(status_code=401, detail="Credenciales inválidas")

        if not usuario or usuario.password != password:
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

        access_token = create_token({
            "sub": username,
            "nombres":usuario.nombres,
            "apellidos":usuario.apellidos
            }, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_token({"sub": username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        # Aquí podrías guardar el refresh token en la base de datos si es necesario
        refresh_token_model = RefreshToken(token=refresh_token, expiryDate=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), usuario_id_usuario=usuario.idUsuario)
        session.add(refresh_token_model)  
        session.commit()

        return ResponseDTO(status="success", message="Usuario Autenticado", data={
            "accessToken": access_token,
            "refreshToken": refresh_token
        })
    except Exception as e:
        # TODO: cuando hay un error el status da 200, no debería
        return ResponseDTO(status="error", message="Tiene una sesión abierta", data=False)

# @router.post("/register", summary="Registro de nuevo usuario")
# async def register(
#         username: str = Query(..., description="username"),
#         password: str = Query(..., description="password"),
#         session: Session = Depends(get_session)):
#     pass


@router.post("/logout", summary="Cierre de Sesion")
async def logout(data: dict = Body(...),
                 session: Session = Depends(get_session),
                 usuario: Usuario = Depends(get_session)):
    username = data.get("username")
    token = data.get("token")

    usuario = session.exec(select(Usuario).where(Usuario.username == username)).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    refresh_token = session.exec(select(RefreshToken).where(RefreshToken.usuario == usuario.idUsuario)).first()
    if not refresh_token:
        raise HTTPException(status_code=404, detail="Refresh token no encontrado")

    # Eliminar el refresh token de la base de datos
    session.delete(refresh_token)
    session.commit()

    # Seleccion del campo expiryDate del token
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp_timestamp = payload.get("exp")
    expiry_date = datetime.fromtimestamp(exp_timestamp).replace(tzinfo=None)

    # Agregar el token a la lista negra
    black = BlackListToken(token=token, expiryDate=expiry_date)
    session.add(black)
    session.commit()  

    return ResponseDTO(
            status="success",
            message="Sesión cerrada correctamente",
            data=True
        )

@router.post("/refresh", summary="Refrescar Token")
async def refresh_token(data: dict = Body(...)):
    refresh = data.get("refresh")

    if not refresh:
        raise HTTPException(status_code=400, detail="Falta el token de refresco")

    with Session(engine) as session:
        try:
            payload = jwt.decode(refresh, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido")

        usuario = session.exec(select(Usuario).where(Usuario.username == username)).first()
        refreshToken = session.exec(select(RefreshToken).where(RefreshToken.token == refresh)).first()

        if not usuario or not refreshToken or refreshToken.token != refresh:
            raise HTTPException(status_code=401, detail="Refresh token no válido")

        new_access_token = create_token(
            {"sub": usuario.username, "name": usuario.nombres, "lastname": usuario.apellidos},
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return ResponseDTO(
            status="success",
            message="Usuario autenticado",
            data={"accessToken": new_access_token}
        )
