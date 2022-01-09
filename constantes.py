import os

#el home del usuario 
HOME_USUARIO = os.path.expanduser("~")

#la ruta donde se van a guardar las fotos y avatars, debe ir la diagonal al final
FOTOS_RUTA_REAL=f'{HOME_USUARIO}/usuario/fotos/'

#ruta para acceder a los archivos de RUTA_FOTOS_REAL, se acceden de la forma:
#http://SERVIDOR/RUTA_FOTOS_VIRTUAL
FOTOS_RUTA_VIRTUAL='/static/fotos'

#ruta donde se encuentra el modelo vgg16 entrenado para razas
VGG16_RUTA_MODELO=f'{HOME_USUARIO}/cnn/modelo-vgg16.h5'

#ruta donde se encuentran las clases (razas) usadas en el modelo vgg16 entrenado para razas
VGG16_RUTA_MODELO_CLASES=f'{HOME_USUARIO}/cnn/razas.pickle'
