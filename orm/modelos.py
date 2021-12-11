from sqlalchemy import Column, ForeignKey, Integer, Float, String, DateTime
from orm.config import BaseClass
import datetime

class Users(BaseClass):
    __tablename__="users"
    id_users = Column(Integer, primary_key=True)
    email_user = Column("email",String(500))
    pasword_hash = Column(String(800))
    nombre = Column(String(300))
    telefono = Column(String(100))
    ruta_avatar = Column(String(5000))
    fecha_registro = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    
class Razas(BaseClass):
    __tablename__="razas"
    id = Column(Integer, primary_key=True)
    raza = Column(String(300))
    especie = Column(String(300))
    descripcion = Column(String)
    cuidados = Column(String)
    
    
    
    