#!/usr/bin/env python
# -*- coding: utf-8 -*-

#el siguiente if permite ejecutar este script directamente desde linea de comandos
if __name__ == "__main__":
    import sys
    from os.path import dirname, abspath                     
    sys.path.insert(0, dirname(dirname(abspath(__file__)))) 
    
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Activation, Dense, Flatten, BatchNormalization, Conv2D, MaxPool2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import itertools
import os
import shutil
import random
import glob
import pathlib
import matplotlib.pyplot as plt
import warnings
import pickle
from tensorflow.python.ops.gen_batch_ops import batch
#deshabilitamos en la salida de la consola mensajes que sean del tipo
#future warning
#warnings.simplefilter(action="ignore", category=FutureWarning)


#Función de utileria para leer el archivo de razas del dataset de oxford, 
# regresa un diccionario que se arma de siguiente forma: 
#     razas[nombre_raza] = (especie,total_imagenes)
# donde especie puede ser "gato" o "perro"
#
# Se pueden obtener los nombres de las razas con:
#
# Ejemplo de uso:
#
#   razas = listar_razas("annotations/annotations/list.txt")
#   nombres_razas = list(razas.keys())
#
def listar_razas(ruta_archivo):    
    razas=dict()
    total=0  #total de imagenes
    with open(ruta_archivo, "r") as archivo:
        for linea_con_break in archivo:
            #removemos el break (fin de línea) del texto con linea.strip
            texto_linea = linea_con_break.strip() 
            #si el texto no es un comentario
            if texto_linea[0]!="#":
                #separamos el texto en parametros usando el espacio como delimitador
                params=texto_linea.split()
                raza=params[0]
                raza=raza[:raza.rindex("_")] #removemos el guión bajo del nombre de la raza (el último)
                #obtenemos especie: 1=gato  2=perro
                especie="gato" if params[2]=="1" else "perro"  
                total=total+1
                
                if raza not in razas:                    
                    contador=1 #primera vez que contamos esta raza
                else:
                    tupla=razas[raza]  #obtenemos una tupla (especie,contador) que guardamos previamente
                    contador=tupla[1]  #obtenemos el contador
                    contador=contador+1 #actualizamos el contador
                
                #actualizamos/creamos la tupla con info de la especie y contador de la raza
                razas[raza]=(especie,contador) 
    
    #print("total de imagenes:",total)
    return razas


# Función para mover TODAS las imagenes de manera recursiva de una carpeta origen a destino
# 
# Ejemplo de uso:
#    mover_imagenes("images/imagenes-origen","images/images-destino")
#
def mover_imagenes(ruta_origen, ruta_destino):                 
    imagenes = glob.glob(ruta_origen + "/**/*.jpg",recursive=True)
    
    movidas=0
    for img in imagenes:
        if not os.path.exists(ruta_destino + "/" + os.path.basename(img)):
            #print("moviendo:",img)            
            shutil.move(img,ruta_destino)
            movidas=movidas+1
       # else:
       #     print("no se moverá a:",img)
    
    print("total imagenes encontradas:",len(imagenes))
    print("se movieron en total:", movidas)


# Dada una lista de clases clases=["clase1","clase2",...,"clasesN"], esta función mueve las imagenes en el 
# directorio "ruta_imagenes" de la forma "clase1*jpg", "clase2*jpg",..."claseN*jpg" a los directorios 
# train, valid y test en proporción al diccionario "porcentaje", que es de la forma 
# {"train":porcentaje1,"valid":porcentaje2,"test":porcentaje3}. Los porcentajes son valores entre 0 y 1 y 
# la suma de estos debe ser menor o igual que 1.
#
# Ejemplo de uso:
#  razas=["raza1","raza2","raza3"]
#  preparar_clases_archivos("images/images",razas,{"train":0.7,"valid":0.2,"test":0.1})
#
def preparar_clases_archivos(ruta_imagenes, clases, porcentajes):
    
    if len(porcentajes)!=3:
        raise Exception("Se deben indicar 3 porcentajes para cada directorio: train, valid y test")        
        
    if sum(porcentajes.values())>1:
        raise Exception("La suma de los porcentajes no puede ser mayor a 1")        
        
    for clase in clases:
        #obtenemos las imagenes que son de la clase en forma de conjunto
        imagenes_clase=glob.glob(ruta_imagenes + "/" + clase + "*.jpg") 
        
        total_imagenes_clase=len(imagenes_clase);
        
        #preparamos sus directorios train, valid y test para la clase 
        #en cada directorio se coloca un número de imagenes del total de acuerdo al porcentaje
        for directorio in ["train","valid", "test"]:                    
            
            ruta_clase = ruta_imagenes + "/" + directorio +"/" + clase
            #si no existe el directorio de la clase lo creamos
            if os.path.isdir(ruta_clase) is False:
                os.makedirs(ruta_clase)
            
            #calculamos el tam de la muestra de acuerdo al porcentaje
            tam_muestra=round(porcentajes[directorio]*total_imagenes_clase)                        
            #nos aseguramos que el tam de la muestra no sobrepase el total de imagenes de la clase
            tam_muestra=min(tam_muestra, len(imagenes_clase))
            print("se moveran", tam_muestra," imagenes hacia:",ruta_clase)
            #obtenemos la muestra y actualizamos el conjunto de imagenes de la clase
            muestra=random.sample(imagenes_clase, tam_muestra)            
            
            #movemos las imagenes de la muestra a su directorio que le corresponde
            for img in muestra:
                #print("moviendo:", img, " hacia:",ruta_clase)
                shutil.move(img, ruta_clase)                  
                #removemos la imagen de la lista para evitar intentar removerla dos veces
                imagenes_clase.remove(img)

#Crea un modelo basado enn vgg16 con un total de salidas dadas por "total_salidas"
#
# Ejemplo de uso:
#  razas = ["raza1","raza2","raza3"]
#  crear_modelo(len(razas))
def crear_modelo(total_salidas):
    #creamos un modelo vgg16
    modelo_vgg16=tf.keras.applications.vgg16.VGG16()
    #modelo_vgg16.summary()

    #Copiamos todas las capas del vgg16 menos la última a nuestro modelo:
    modelo=Sequential()
    #iteramos todas las capas menos la última
    for capa in modelo_vgg16.layers[:-1]:
        #deshabilitamos que las capas sean entrenables
        capa.trainable=False
        #copiamos la capa de vgg16 a nuestro modelo
        modelo.add(capa)

    #Agreamos una última capa al modelo para las salidas:
    modelo.add(Dense(units=total_salidas,activation="softmax"))
    modelo.summary()

    return modelo

# Esta funnción entrena un modelo dado con las imagenes definidas en 
# las rutas "train_dir" y "valid_dir", se toman solo las imagenes que esten
# en las clases dadas por la lista "clases" (cada clase es una carpeta que
# agrupa imagenes)
#
# Ejemplo de uso:
#   train_dir = "images/images/train"
#   valid_dir = "images/images/valid"
#   razas = ["raza1","raza2","raza3"]
#   modelo = crear_modelo(len(razas))
#   entrenar_modelo(modelo,train_dir,valid_dir)
#
def entrenar_modelo(modelo,clases,train_dir,valid_dir):       
    #creamos el lote de imagenes para entrenamiento
    lotes_train=ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)\
    .flow_from_directory(directory=train_dir,target_size=(224,224),classes=clases,batch_size=10)
    #creamos el lote de imagenes para validar
    lotes_valid=ImageDataGenerator(preprocessing_function=tf.keras.applications.vgg16.preprocess_input)\
    .flow_from_directory(directory=valid_dir,target_size=(224,224),classes=clases,batch_size=10)
    #compilamos el modelo
    modelo.compile(optimizer=Adam(learning_rate=0.0001),loss="categorical_crossentropy",metrics=["accuracy"])
    #iniciamos entrenamiento
    modelo.fit(x=lotes_train,validation_data=lotes_valid,epochs=5,verbose=2)

#Guarda el modelo y las etiquetas de las clases
#
# Ejemplo de uso:
#    g_modelo("modelo-vgg16.h5","modelo-clases.pickle")
#
def guardar_modelo(modelo,clases, ruta_modelo, ruta_clases):
    modelo.save(ruta_modelo)
    f = open(ruta_clases, "wb")
    f.write(pickle.dumps(clases))
    f.close()

#lee el modelo y las etiquetas de las clases
def leer_modelo(ruta_modelo,ruta_clases):
    print("leyendo modelo vgg16")
    #leemos el modelo
    modelo=load_model("")
    #leemos las clases que se usaron enn el modelo
    clases = pickle.loads(open(ruta_clases, "rb").read())
    print("modelo vgg16 ha sido leido")
    #modelo.summary()
    return [modelo,clases]


#funcion a ejecutar si se corre directamente este script
def main():
    train_dir = "images/images/train"
    valid_dir = "images/images/valid"
    razas = listar_razas("annotations/annotations/list.txt")
    modelo = crear_modelo(len(razas))
    entrenar_modelo(modelo,train_dir,valid_dir)
    guardar_modelo(modelo,razas,"modelo-entrenado-vgg16.h5","razas.pickle")
    

if __name__ == "__main__":
    main()
