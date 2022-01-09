from re import escape
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import pickle
import constantes as constantes
from orm import esquemas

print("leyendo modelo vgg16")
#leemos el modelo
modelo=load_model(constantes.VGG16_RUTA_MODELO)
#leemos las clases (razas) que se usaron enn el modelo
razas = pickle.loads(open(constantes.VGG16_RUTA_MODELO_CLASES, "rb").read())
print("modelo vgg16 ha sido leido")
#modelo.summary()

#clasifica una imagen y regresa un objeto esquemas.prediccionRaza con los resultados
def clasificar_raza(ruta_imagen):
    #leemos la imagen a clasificar
    imagen = load_img(ruta_imagen, target_size=(224, 224))
    imagen = img_to_array(imagen)
    imagen = imagen.reshape((1, imagen.shape[0], imagen.shape[1], imagen.shape[2]))
    imagen = preprocess_input(imagen)
    #hacemos la predicción
    prediccion = modelo.predict(imagen)
    #obtenemos los porcentajes
    porcentajes = prediccion[0]
    #print(prediccion)
    #obtenemos los indices de los 3 porcentajes más altos de la predicción, de menor a mayor
    ind_maximos = np.argpartition(porcentajes, -3)[-3:]
    #revertimos el arreglo, ahora van de mayor a menor
    ind_maximos = np.flipud(ind_maximos)
    #obtenemos indices de los porcentajes primario, secundario y terciario
    ind_prim = ind_maximos[0]
    ind_sec = ind_maximos[1]
    ind_ter = ind_maximos[2]
    #obtenemos las razas y su porcentaje de probabilidad    
    porcentaje_prim=porcentajes[ind_prim]
    raza_prim=razas[ind_prim]
    porcentaje_sec=porcentajes[ind_sec]
    raza_sec=razas[ind_sec]
    porcentaje_ter=porcentajes[ind_ter]
    raza_ter=razas[ind_ter]
    #preparamos el objeto con los resultados
    res = esquemas.PrediccionRaza(
        porcentaje_primaria = porcentaje_prim,
        raza_primaria = raza_prim,
        porcentaje_secundario = porcentaje_sec,
        raza_secundaria = raza_sec,
        porcentaje_terciario = porcentaje_ter,
        raza_terciaria = raza_ter 
    )    

    return res
    
