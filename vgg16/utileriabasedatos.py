#!/usr/bin/env python
# -*- coding: utf-8 -*-

#el siguiente if permite ejecutar este script directamente desde linea de comandos
if __name__ == "__main__":
    import sys
    from os.path import dirname, abspath                     
    sys.path.insert(0, dirname(dirname(abspath(__file__)))) 

from entrenamiento import listar_razas
import orm.repo as repo
from orm.modelos import Razas
from orm.config import SessionClass
import constantes
import wikipedia

def guardar_en_base(sesion,nombre_raza,especie):    
    ruta_archivo_oxford = f'{constantes.HOME_USUARIO}/cnn/list.txt'
    razas = listar_razas(ruta_archivo_oxford)    
    nombres_razas = list(razas.keys())        
    sesion = SessionClass()
    for nombre_raza in nombres_razas:
        razaBD = repo.raza_por_nombre_raza(sesion,nombre_raza)
        #si la raza no existe en la base
        if razaBD is None:
            especie = razas[nombre_raza][0]
            raza_nueva = Razas()    
            raza_nueva.especie = especie
            raza_nueva.raza = nombre_raza
            print("guardando en Base datos raza:",nombre_raza, ", especie:", especie)
            sesion.add(raza_nueva)
            sesion.commit()
            sesion.refresh(raza_nueva)     
    sesion.close()    

def generar_texto_insert():
    ruta_archivo_oxford = f'{constantes.HOME_USUARIO}/cnn/list.txt'
    razas = listar_razas(ruta_archivo_oxford)    
    nombres_razas = list(razas.keys())            
    texto_insert = ""
    for nombre_raza in nombres_razas:                
        especie = razas[nombre_raza][0]            
        raza_alias = obten_raza_esp_wikipedia(nombre_raza)
        texto_insert = texto_insert + f"INSERT INTO app.razas(raza, especie, raza_alias) VALUES('{nombre_raza}','{especie}','{raza_alias}');\n"
    print(texto_insert)

def obten_raza_esp_wikipedia(raza):
    #print("buscando alias en español para raza:", raza)
    wikipedia.set_lang("es")
    res_busqueda = wikipedia.search(raza)    
    #print(res_busqueda)
    raza_alias = res_busqueda[0]
    print("Para raza:",raza,"se econtró alias:",raza_alias)
    return raza_alias

#funcion a ejecutar si se corre directamente este script
def main():
   generar_texto_insert()

if __name__ == "__main__":
    main()
