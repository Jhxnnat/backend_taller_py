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

security = HTTPBearer()

# Crear token con iat y exp
def create_token(data: dict, expires_delta: timedelta):
    now_utc = datetime.now(timezone.utc)
    to_encode = data.copy()
    to_encode["iat"] = int(now_utc.timestamp())
    to_encode["exp"] = int((now_utc + expires_delta).timestamp())
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if the token is expired
        if 'exp' in payload and datetime.utcfromtimestamp(payload['exp']) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expirado")

        return payload  # Return the decoded payload if valid

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

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
