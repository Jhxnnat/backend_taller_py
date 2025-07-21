from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Body, Query
from sqlmodel import Session, select
from models.models import BlackListToken, Usuario, RefreshToken
from settings.ResponseDTO import ResponseDTO
from settings.auth import ALGORITHM, SECRET_KEY, create_token, decode_token
from settings.database import get_session
# from settings.password_utils import PasswordUtils
from settings.password_utils import get_password_hash, verify_password
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
        usuario = session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

        if not usuario or not verify_password(password, usuario.password):
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
        # if not usuario or usuario.password != password:
        #     raise HTTPException(status_code=401, detail="Credenciales inválidas")

        access_token = create_token({
            "sub": username,
            "nombres":usuario.nombres,
            "apellidos":usuario.apellidos
            }, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        refresh_token = create_token({"sub": username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

        refresh_token_model = RefreshToken(token=refresh_token, expiryDate=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), usuario_id_usuario=usuario.idUsuario)
        session.add(refresh_token_model)  
        session.commit()

        return ResponseDTO(status="success", message="Usuario Autenticado", data={
            "accessToken": access_token,
            "refreshToken": refresh_token
        })
    except Exception as e:
        # TODO: cuando hay un error el status da 200, no debería ser así
        print("Error:", e)
        return ResponseDTO(status="error", message="Tiene una sesión abierta", data=False)

@router.post("/register", summary="Registrar un nuevo usuario")
async def register(
    username: str = Query(..., description="Nombre de usuario"),
    password: str = Query(..., description="Contraseña"),
    nombres: str = Query(..., description="Nombres del usuario"),
    apellidos: str = Query(..., description="Apellidos del usuario"),
    email: str = Query(..., description="Correo electronico del usuario"),
    direccion: str = Query(..., description="Direccion del usuario"),
    telefono: str = Query(..., description="Número de telefono del usuario"),
    session: Session = Depends(get_session)):
    
    try:
        # Check if the username already exists
        existing_user = session.exec(
            select(Usuario).where(Usuario.username == username)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")

        # Hash the password
        hashed_password = get_password_hash(password)

        # Create a new user instance
        new_user = Usuario(
            username=username,
            password=hashed_password,
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            direccion=direccion,
            telefono=telefono
        )

        # Add the new user to the session and commit
        session.add(new_user)
        session.commit()

        return ResponseDTO(status="success", message="Usuario registrado exitosamente", data={
            "username": new_user.username,
            "nombres": new_user.nombres,
            "apellidos": new_user.apellidos
        })

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")

@router.post("/logout", summary="Cierre de Sesion")
async def logout(username: str = Query(..., description="username"), session: Session = Depends(get_session)):

    try:
        # TODO: username debería ser único en la base de datos, usar "name" para otros casos
        usuario = session.exec(select(Usuario).where(Usuario.username == username)).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        refresh_token = session.exec(
            select(RefreshToken).where(RefreshToken.usuario_id_usuario == usuario.idUsuario)
        ).first()

        if refresh_token:
            session.delete(refresh_token)
            session.commit()

        return ResponseDTO(status="success", message="Sesión cerrada correctamente", data=True)

    except Exception as e:
        print("Error: ", e)
        raise HTTPException(status_code=404, detail="Error cerrando sesión")

@router.post("/refresh-token", summary="Obtener nuevo access token")
async def refresh_token(
    refresh_token: str = Query(..., description="Refresh token"),
    session: Session = Depends(get_session)):
    
    try:
        # Validate the refresh token
        token_data = decode_token(refresh_token)  # Implement this function to decode and validate the token
        if not token_data:
            raise HTTPException(status_code=401, detail="Refresh token inválido")

        # Check if the refresh token exists in the database
        stored_token = session.exec(
            select(RefreshToken).where(RefreshToken.token == refresh_token)
        ).first()

        if not stored_token or stored_token.expiryDate < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Refresh token expirado")

        # Generate a new access token
        usuario = session.exec(
            select(Usuario).where(Usuario.idUsuario == stored_token.usuario_id_usuario)
        ).first()

        new_access_token = create_token({
            "sub": usuario.username,
            "nombres": usuario.nombres,
            "apellidos": usuario.apellidos
        }, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

        return ResponseDTO(status="success", message="Nuevo access token generado", data={
            "accessToken": new_access_token
        })

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al refrescar el token")

