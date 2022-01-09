from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from sqlalchemy.orm import relationship
from orm.config import BaseClass
import datetime

class Users(BaseClass):
    __tablename__="users"
    id = Column(Integer, primary_key=True)
    email_user = Column("email", String(500))
    password_hash = Column(String(800))
    nombre = Column(String(300))
    telefono = Column(String(100))
    ruta_avatar = Column(String(5000))
    fecha_registro = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    
class Razas(BaseClass):
    __tablename__="razas"
    id = Column(Integer, primary_key=True)
    raza = Column(String(300))
    raza_alias = Column(String(300))
    especie = Column(String(300))
    descripcion = Column(String)
    cuidados = Column(String)
    
class Fotos(BaseClass):
    __tablename__ = "fotos"
    id = Column(Integer, primary_key=True)
    id_users = Column(Float, ForeignKey(Users.id))
    ruta = Column(String)
    correccion_raza = Column(String)    
    clasificacion_id_raza_primaria = Column(Integer, ForeignKey(Razas.id))
    clasificacion_id_raza_secundaria = Column(Integer, ForeignKey(Razas.id))
    clasificacion_id_raza_terciaria = Column(Integer, ForeignKey(Razas.id))
    porcentaje_clasificacion_primaria = Column(Float)
    porcentaje_clasificacion_secundaria = Column(Float)
    porcentaje_clasificacion_terciaria = Column(Float)
    fecha  = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)    
    # mapeo de relacion uno-a-uno con tabla Razas
    razaPrimaria = relationship("Razas", foreign_keys=clasificacion_id_raza_primaria,lazy="subquery")        
    razaSecundaria = relationship("Razas", foreign_keys=clasificacion_id_raza_secundaria,lazy="subquery")        
    razaTerciaria = relationship("Razas", foreign_keys=clasificacion_id_raza_terciaria,lazy="subquery")        


    
    