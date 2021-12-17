from sqlalchemy.orm import Session 
#Repositorio
import orm.modelos as modelos
from orm.esquemas import UsersBD

#Solicitud GET usuarios (Por id)
def usuario_por_id(sesion : Session, id : int):
    return sesion.query(modelos.Users).filter(modelos.Users.id == id).first()

#Solicitud GET usuario (todos los renglones de la tabla razas)
def usuarios(sesion : Session, lote : int, pag : int):
    return sesion.query(modelos.Users).limit(lote).offset(pag*lote).all()

#Solicitud GET razas (todos los renglones de la tabla razas)
def razas(sesion : Session, lote : int, pag : int):
    return sesion.query(modelos.Razas).limit(lote).offset(pag*lote).all()

#Solicitud GET razas (Por id)
def raza_id(sesion : Session, id : int):
    return sesion.query(modelos.Razas).filter(modelos.Razas.id == id).first()


def guardar_usuario(sesion : Session, usr:UsersBD):
    
    usr_nuevo = modelos.Users()
    usr_nuevo = usr.nombre
    usr_nuevo.email_user = usr.email
    usr_nuevo.password_hash = usr.password
    usr_nuevo.telefono = usr.telefono
    usr_nuevo.ruta_avatar = usr.ruta_avatar
    
    
    
    sesion.add(usr_nuevo)
    sesion.commit() #Guarda los cambios datos en la base de datos
    sesion.refresh(usr_nuevo) #Con esto ibtenemos el id que le asigno la base
    
    return usr_nuevo

def actualizar_usuario(sesion:Session, id_usuario:int, usr:UsersBD):
    usr_act = usuario_por_id(sesion, id_usuario)
    
    usr_act.nombre = usr.nombre
    usr_act.email_user = usr.email
    usr_act.password_hash = usr.password
    usr_act.telefono = usr.telefono
    usr_act.ruta_avatar = usr.ruta_avatar

    sesion.commit()
    sesion.refresh(usr_act)
    
    return usr_act



