from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from orm import repo
from sqlalchemy.orm import Session
import constantes


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

#funcion para verificar que un password coincide con el password hash
def verificar_password(password_plano, password_hash):
    return pwd_context.verify(password_plano, password_hash)

#función para obtener el hash de un password
def obtener_password_hash(password):
    return pwd_context.hash(password)

#función para autentificar a un usuario
def autentificar_usuario(sesion:Session, email: str, password: str):
    usuario = repo.usuario_por_email(sesion,email)
    if not usuario: 
        #el usuario no existe, no es válido
        print("No existe usuario con email:", email)        
        return False
    if not verificar_password(password, usuario.password_hash):
        #el password no es correcto
        print("password incorrecto para usuario con email:", email)
        return False
    return usuario

def crear_token_acceso(email:str):    
    intervalo_expiracion = timedelta(minutes=constantes.JWT_TOKEN_TIEMPO_EXPIRACION_MINUTOS)
    fecha_expiracion = datetime.utcnow() + intervalo_expiracion    
    datos_a_codificar = {"sub": email,"exp": fecha_expiracion}    
    token_jwt = jwt.encode(datos_a_codificar, constantes.JWT_SECRET_KEY, algorithm=constantes.HASH_ALGORITMO)
    return token_jwt

#dado un token valida si es correcto, si lo es, regresa el email del usuario que generó el token
async def validar_token_usuario(token: str = Depends(oauth2_scheme)):    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, constantes.JWT_SECRET_KEY, algorithms=[constantes.HASH_ALGORITMO])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception        
    except JWTError:
        raise credentials_exception
    
    return email
