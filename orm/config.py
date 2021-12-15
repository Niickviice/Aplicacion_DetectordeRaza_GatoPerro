from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_BASE_DATOS="postgresql://C&D_owner:08Aj#476a@localhost:5432/CatDog_app_DB"
engine= create_engine(URL_BASE_DATOS, connect_args={"options": "-csearch_path=app"})
SessionClass = sessionmaker(engine)
BaseClass = declarative_base()

def obten_sesion():
    sesion=SessionClass()
    try:
        yield sesion
    finally:
        sesion.close()

