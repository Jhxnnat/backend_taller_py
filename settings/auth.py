from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from models.models import BlackListToken
from settings.database import get_session

# Configuración
SECRET_KEY = "secret-jwt-key"
ALGORITHM = "HS256"

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
security = HTTPBearer()

# Crear token con iat y exp
def create_token(data: dict, expires_delta: timedelta):
    now_utc = datetime.now(timezone.utc)
    to_encode = data.copy()
    to_encode["iat"] = int(now_utc.timestamp())
    to_encode["exp"] = int((now_utc + expires_delta).timestamp())
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verificar token y obtener usuario
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),
                     session: Session = Depends(get_session)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token sin usuario")
        # Consulta DB si lo necesitas
        backlist = session.exec(select(BlackListToken).where(BlackListToken.token == token)).first()
        if backlist:
            raise HTTPException(status_code=401, detail="Token en lista negra")
        
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

