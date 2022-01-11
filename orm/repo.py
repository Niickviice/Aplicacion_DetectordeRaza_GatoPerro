from sqlalchemy.orm import Session 
from sqlalchemy import func
#Repositorio
import orm.modelos as modelos
import constantes as constantes
from orm.esquemas import PrediccionRaza, UsersBD

#Solicitud de usuarios (Por id)
def usuario_por_id(sesion : Session, id : int):
    return sesion.query(modelos.Users).filter(modelos.Users.id == id).first()

#Solicitud de usuario (todos los renglones de la tabla razas)
def usuarios(sesion : Session, lote : int, pag : int):
    return sesion.query(modelos.Users).limit(lote).offset(pag*lote).all()

#Solicitud de razas (todos los renglones de la tabla razas)
def razas(sesion : Session, lote : int, pag : int):
    return sesion.query(modelos.Razas).limit(lote).offset(pag*lote).all()

#Solicitud de raza (Por id)
def raza_id(sesion : Session, id : int):
    return sesion.query(modelos.Razas).filter(modelos.Razas.id == id).first()

#Solicitud de raza (Por raza)
def raza_por_nombre_raza(sesion: Session, nombre_raza: str):
    return sesion.query(modelos.Razas).filter(func.lower(modelos.Razas.raza) == func.lower(nombre_raza)).first()

#guardar usuario
def guardar_usuario(sesion : Session, usr:UsersBD):    
    usr_nuevo = modelos.Users()    
    usr_nuevo.email_user = usr.email
    usr_nuevo.password_hash = usr.password
    usr_nuevo.nombre = usr.nombre
    usr_nuevo.telefono = usr.telefono
    
    
    sesion.add(usr_nuevo)
    sesion.commit() #Guarda los cambios datos en la base de datos
    sesion.refresh(usr_nuevo) #Con esto ibtenemos el id que le asigno la base
    
    return usr_nuevo

#actualizar usuario
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

#actualizar la ruta de avatar de un usuario
def actualizar_usuario_ruta_avatar(sesion:Session, id_usuario:int, ruta_avatar:str):
    usr_act=usuario_por_id(sesion, id_usuario)
    usr_act.ruta_avatar = ruta_avatar

    sesion.commit()
    sesion.refresh(usr_act)
    
    return usr_act

#crear una foto
def crear_foto(sesion:Session, id_usuario:int, nombre_imagen:str, predicciones:PrediccionRaza):
    foto = modelos.Fotos()
    #información de la raza primaria
    razaPrim = raza_por_nombre_raza(sesion,predicciones.raza_primaria)
    foto.clasificacion_id_raza_primaria = razaPrim.id
    foto.porcentaje_clasificacion_primaria = predicciones.porcentaje_primaria
    #información de la raza secundaria
    razaSec = raza_por_nombre_raza(sesion,predicciones.raza_secundaria)
    foto.clasificacion_id_raza_secundaria = razaSec.id
    foto.porcentaje_clasificacion_secundaria = predicciones.porcentaje_secundario    
    #información de la raza terciaria
    razaTer = raza_por_nombre_raza(sesion,predicciones.raza_terciaria)
    foto.clasificacion_id_raza_terciaria = razaTer.id
    foto.porcentaje_clasificacion_terciaria = predicciones.porcentaje_terciario   
    #resto de la información de la foto
    foto.id_users = id_usuario
    foto.ruta = nombre_imagen
    
    sesion.add(foto)
    sesion.commit()
    sesion.refresh(foto)

    #print("PRIMARIA:",foto.razaPrimaria)
    
    return foto

#Solicitud de foto (Por id)
def foto_por_id(sesion : Session, id_foto : int):
    return sesion.query(modelos.Fotos).filter(modelos.Fotos.id == id_foto).first()

#Solicitud de fotos por id usuario (todos los renglones de la tabla fotos por id_users)
def fotos_por_idusuario(sesion : Session, id_usuario:int, lote : int, pag : int):
    return sesion.query(modelos.Fotos).filter(modelos.Fotos.id_users == id_usuario).limit(lote).offset(pag*lote).all()

#actualizar campo correccion raza de una foto
def actualizar_foto_correccion_raza(sesion:Session, id_foto:int, correcion_raza:str):
    foto = foto_por_id(sesion, id_foto)
    foto.correccion_raza = correcion_raza
    
    sesion.commit()
    sesion.refresh(foto)
    
    return foto