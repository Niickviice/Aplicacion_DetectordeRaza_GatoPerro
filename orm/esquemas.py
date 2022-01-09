from pydantic import BaseModel

class UsersBD(BaseModel):
    nombre:str
    email:str
    password:str 
    foto:int
    telefono:int

class PrediccionRaza(BaseModel):
    porcentaje_primaria:float
    raza_primaria:str
    porcentaje_secundario:float
    raza_secundaria:str
    porcentaje_terciario:float
    raza_terciaria:str    

    
    
        