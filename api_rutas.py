#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################
#                               #           
#      Proyecto Final           #
#                               #
#      UAM - Cuajimalpa         #
#                               #
#      Alan Martínez Ruiz       #
#                               #
#################################

from fastapi import Body, Depends, FastAPI, UploadFile, File, Form,HTTPException, Response,status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from typing import Optional
from fastapi.param_functions import Form
from pydantic import BaseModel
from datetime import timedelta
import shutil
import os
import uuid
import constantes as constantes
import uvicorn
from orm.config import obten_sesion
from orm.esquemas import UsersBD, UsersBDUpdate
import orm.repo as repo
from sqlalchemy.orm import Session, session
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from vgg16 import clasificador
from seguridad import autenticacion


app = FastAPI()
#indicamos la carpeta de rutas para las fotos
app.mount(constantes.FOTOS_RUTA_VIRTUAL, StaticFiles(directory=constantes.FOTOS_RUTA_REAL), name="static-fotos")
#activamos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ruta para obtener token jwt
@app.post("/token", response_model=autenticacion.Token)
async def login_para_obtener_token(*,sesion:Session=Depends(obten_sesion), form_data: OAuth2PasswordRequestForm = Depends()):
    #autentificamos si el usuario es valido        
    email = form_data.username
    password = form_data.password
    user = autenticacion.autentificar_usuario(sesion,email,password)
    if not user:
        #si no es valido regresamos un error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #si es valido creamos su token de acceso
    access_token = autenticacion.crear_token_acceso(email)
    #regresamos el token y tipo de token (bearer para jwt)
    return {"access_token": access_token, "token_type": "bearer"}

#Ruta Get para obtener la tabla de usuarios por id 
@app.get("/usuario/{id}")
def usuario_por_id(*,sesion:Session=Depends(obten_sesion), id:int,token: str = Depends(autenticacion.validar_token_usuario)):
    print("Buscando con id:", id)
    
    user = repo.usuario_por_id(sesion, id)
    return user

#Ruta post, para registrar nuevo usuario.
@app.post("/registro")
def registro(*,sesion:Session=Depends(obten_sesion), usuario:UsersBD, response:Response):
    
    print("buscando usuario con email:", usuario.email) 
    userdb = repo.usuario_por_email(sesion,usuario.email)
    
    if userdb != None:
     print("ya existe el usuario con email:",usuario.email)
     response.status_code =status.HTTP_409_CONFLICT
    else:
     print("creando nuevo usuario con info:",usuario)
     return repo.guardar_usuario(sesion, usuario)    
    

#Ruta Put, para actualizar información del usuario 
@app.put("/usuario/{id}")
def actualizar_usuario(*,sesion:Session=Depends(obten_sesion), id:int,  usuario:UsersBDUpdate, token:str=Depends(autenticacion.validar_token_usuario), response:Response):
    if usuario.email != None:
        #obtenemos info del usuario actual
        usuario_a_actualizar = repo.usuario_por_id(sesion,id)
        #verificamos que el email no sea de algún usuario que ya existe
        print("buscando usuario con email:", usuario.email) 
        userdb = repo.usuario_por_email(sesion,usuario.email)
    
        if userdb != None and userdb.email_user!=usuario_a_actualizar.email_user:
            print("ya existe el usuario con email:",usuario.email)
            response.status_code =status.HTTP_409_CONFLICT
            return #terminamos

    print("petición put procederá a actualizar usuario con id:", id, ", con info:",usuario)    
    return repo.actualizar_usuario(sesion, id, usuario)

#Ruta delete, para eliminar al usuario
@app.delete("/usuario/{id}")
def eliminar_usuario(*,sesion:Session=Depends(obten_sesion), id:int, token:str=Depends(autenticacion.validar_token_usuario), response:Response):
    print("se eliminará usuario con id:",id, " y todas sus fotos asociadas")
    re = repo.eliminar_fotos_por_id_usuario(sesion,id)
    print("fotos eliminadas:", re)
    print("eliminando usuario con id:",id)
    repo.eliminar_usuario_por_id(sesion,id)    
    print("usuario eliminado")

    return {"estatus":"usuario eliminado"}

#Ruta Get para obtener la tabla de razas por id 
@app.get("/razas/{id}")
def raza_por_id(*,sesion:Session=Depends(obten_sesion), id:int,token:str=Depends(autenticacion.validar_token_usuario)):
    print("Buscando con id:", id)
    
    user = repo.raza_id(sesion, id)
    return user

#Ruta Get para obtener el id del usuario que ha iniciado sesión
@app.get("/usuarios/me")
def usuario_en_login(*,sesion:Session=Depends(obten_sesion),email:str=Depends(autenticacion.validar_token_usuario)):
    usuario = repo.usuario_por_email(sesion,email)
    return usuario

#Ruta Get para obtener la tabla de usuarios completa
@app.get("/usuariosCompletos ")
def usuarios_lista(*,sesion:Session=Depends(obten_sesion), lote:int=10, pag:int,token:str=Depends(autenticacion.validar_token_usuario)):
    print("lote", lote, "pag:", pag)
    
    return repo.usuarios(sesion, lote, pag)

#Ruta Get para obtener la tabla de razas completa
@app.get("/razasCompletas")
def razas_lista(*,sesion:Session=Depends(obten_sesion), lote:int=10, pag:int,token:str=Depends(autenticacion.validar_token_usuario)):
    print("lote", lote, "pag:", pag)
    
    return repo.razas(sesion, lote, pag)

#Ruta Post para crear/actualizar un avatar para el usuario
@app.post("/usuario/{id}/avatar")
async def guardar_usuario_avatar(*,sesion:Session=Depends(obten_sesion), id:int, foto:UploadFile=File(...),token:str=Depends(autenticacion.validar_token_usuario)):

    #guardamos el avatar del usuario
    
    nombre_archivo = uuid.uuid4().hex #Se genera nombre en formato hexadecimal 
    extension = os.path.splitext(foto.filename)[1]
    nombre_imagen = f'{nombre_archivo}{extension}'
    ruta_image = f'{constantes.FOTOS_RUTA_REAL}{nombre_imagen}'
    print("avatar usuario guardado en ruta:", ruta_image)   
    
    with open(ruta_image, "wb") as imagen:
        contenido = await foto.read()                
        imagen.write(contenido)
        #como es una imagen de avatar, cambiamos tamaño
        image = Image.open(ruta_image)
        new_image = image.resize((400, 400))
        new_image.save(ruta_image)
        
        #guardamos foto del avatar 
        repo.actualizar_usuario_ruta_avatar(sesion, id, nombre_imagen)

    return {"id_user":id,"foto": nombre_imagen}
        
    

#Ruta POST para subir la imagen de usuario
@app.post("/usuarios/{id}/foto")
async def guardar_usuario_foto(*,sesion:Session=Depends(obten_sesion), id:int,foto:UploadFile=File(...),token:str=Depends(autenticacion.validar_token_usuario)):

    #guardamos la imagen        
    nombre_archivo = uuid.uuid4().hex #Se genera noombre en formato hexadecimal 
    extension = os.path.splitext(foto.filename)[1]
    nombre_imagen = f'{nombre_archivo}{extension}'
    ruta_image = f'{constantes.FOTOS_RUTA_REAL}{nombre_imagen}'
    print("Guardadando imagen en ruta:", ruta_image)   
    
    with open(ruta_image, "wb") as imagen:
        contenido = await foto.read()
        imagen.write(contenido)
        print("Imagen guardada en ruta:", ruta_image)   
        #hacemos la predicción de las razas
        print("Clasificando foto:",nombre_imagen)
        predicciones = clasificador.clasificar_raza(ruta_image)
        print("Se ha clasificando foto:",nombre_imagen)        
        #guardamos en la base de datos la información de la foto
        print("guardando en base datos info de la foto:",nombre_imagen)
        foto = repo.crear_foto(sesion, id, nombre_imagen, predicciones)
        print("Se ha guardando en base datos info de la foto:",nombre_imagen)

        return foto

#Ruta GET para obtener una foto por id
@app.get("/foto/{id_foto}")
def foto_por_id(*,sesion:Session=Depends(obten_sesion), id_foto:int,token:str=Depends(autenticacion.validar_token_usuario)):
    print("obteniendo foto con id:",id_foto)
    foto = repo.foto_por_id(sesion,id_foto)
    return foto

#Ruta GET para obtener fotos por id usuario
@app.get("/usuario/{id_usuario}/fotos")
def foto_por_id(*,sesion:Session=Depends(obten_sesion), id_usuario:int, lote:int=10, pag:int,token:str=Depends(autenticacion.validar_token_usuario)):
    print("obteniendo fotos del usuario con id:",id_usuario)
    fotos = repo.fotos_por_idusuario(sesion,id_usuario, lote, pag)
    return fotos

#Ruta PUT para corregir información de la raza
@app.put("/foto/{id_foto}/correccion_raza")
def correccion_raza(*,sesion:Session=Depends(obten_sesion), id_foto:int, correccion_raza:str=Body(...,embed=True),token:str=Depends(autenticacion.validar_token_usuario)):
    print("Se hará corrección raza:",correccion_raza,"para foto con id:", id_foto)
    foto = repo.actualizar_foto_correccion_raza(sesion, id_foto, correccion_raza)
    return foto
    
#para hacer debugging
if __name__ == "__main__":
    print("Ejecutando en modo debugging")
    uvicorn.run(app, host="0.0.0.0", port=8000)