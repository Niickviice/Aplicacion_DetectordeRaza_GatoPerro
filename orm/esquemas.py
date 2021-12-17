from pydantic import BaseModel


class UsersBD(BaseModel):
    nombre:str
    email:str
    password:str 
    foto:int
    telefono:int
    ruta_avatar:str