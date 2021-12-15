###############
#           
#      Proyecto Final 
#    
#      UAM - Cuajimalpa
#
#      Alan Martínez Ruiz 
#   
##############
from fastapi import Depends,FastAPI
from typing import Optional
from pydantic import BaseModel
import shutil
import os
import uuid
from orm.config import obten_sesion
import orm.repo as repo 
from sqlalchemy.orm import Session



app = FastAPI()

@app.get("/usuarios/{id}")
def usuarios(*,sesion:Session=Depends(obten_sesion), id:int):
    print("Buscando con id:", id)
    
    user = repo.usuario_por_id(obten_sesion, id)
    return user