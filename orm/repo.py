from sqlalchemy.orm import Session 
#Repositorio
import orm.modelos as modelos

def usuario_por_id(session:Session, id=int):
    return session.query(modelos.Users).filter(modelos.Users.id_users == id).first()
