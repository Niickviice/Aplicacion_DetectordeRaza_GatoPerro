from typing import Optional
from pydantic import BaseModel

#para hacer posts
class UsersBD(BaseModel):
    nombre:str
    email:str
    password:str     
    telefono:str
    
#para put
class UsersBDUpdate(BaseModel):
    nombre:Optional[str] = None
    email:Optional[str] = None
    password:Optional[str] = None
    telefono:Optional[str] = None

class PrediccionRaza(BaseModel):
    porcentaje_primaria:float
    raza_primaria:str
    porcentaje_secundario:float
    raza_secundaria:str
    porcentaje_terciario:float
    raza_terciaria:str    

    
    
        