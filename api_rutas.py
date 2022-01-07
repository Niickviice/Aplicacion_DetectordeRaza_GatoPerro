#################################
#                               #           
#      Proyecto Final           #
#                               #
#      UAM - Cuajimalpa         #
#                               #
#      Alan Martínez Ruiz       #
#                               #
#################################

from fastapi import Depends, FastAPI, UploadFile, File, Form 
from typing import Optional
from fastapi.param_functions import Form
from pydantic import BaseModel
import shutil
import os
import uuid
from orm.config import obten_sesion
from orm.esquemas import UsersBD
import orm.repo as repo
from sqlalchemy.orm import Session, session
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#Ruta Get para obtener la tabla de usuarios por id 
@app.get("/usuarios/{id}")
def usuarios(*,sesion:Session=Depends(obten_sesion), id:int):
    print("Buscando con id:", id)
    
    user = repo.usuario_por_id(sesion, id)
    return user

#Ruta post, para registrar nuevo usuario.
@app.post("/registro")
def registro(*,sesion:Session=Depends(obten_sesion), usuario:UsersBD):
    print("Usuario registrado:", usuario)
    
    
    return repo.guardar_usuario(sesion, usuario)

#Ruta Put, para actualizar información del usuario 
@app.put("usuario/{id}")
def actualizar_usuario(*,sesion:Session=Depends(obten_sesion), id:int,  usuario:UsersBD):
    
    return repo.actualizar_usuario(sesion, id, usuario)

#Ruta Get para obtener la tabla de razas por id 
@app.get("/razas/{id}")
def usuarios(*,sesion:Session=Depends(obten_sesion), id:int):
    print("Buscando con id:", id)
    
    user = repo.raza_id(sesion, id)
    return user

#Ruta Get para obtener la tabla de usuarios completa
@app.get("/usuariosCompletos ")
def usuarios_lista(*,sesion:Session=Depends(obten_sesion), lote:int=10, pag:int, orden:Optional[str]=None):
    print("lote", lote, "pag:", pag, "orden:", orden)
    
    return repo.usuarios(sesion, lote, pag)

#Ruta Get para obtener la tabla de razas completa
@app.get("/razasCompletas")
def usuarios_lista(*,sesion:Session=Depends(obten_sesion), lote:int=10, pag:int, orden:Optional[str]=None):
    print("lote", lote, "pag:", pag, "orden:", orden)
    
    return repo.razas(sesion, lote, pag)

#Ruta POST para subir la imagen de usuario
@app.post("/fotos")
async def guardar_usuario_fotos(foto:UploadFile=File(...)):
    
    
    home_user = os.path.expanduser("~")
    nombre_archivo = uuid.uuid4().hex #Se genera noombre en formato hexadecimal 
    extension = os.path.splitext(foto.filename)[1]
    ruta_image = f'{home_user}/usuario/fotos/{nombre_archivo}{extension}'
    print("Imagen guardada en ruta:", ruta_image)   
    
    with open(ruta_image, "wb") as imagen:
        contenido = await foto.read()
        imagen.write(contenido)
    
    return {"foto": foto.filename}