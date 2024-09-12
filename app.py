# Autor: Jonathan Hernández
# Fecha: 11 Septiembre 2024
# Descripción: Código para procesamiento de imagenes con Sobel.
# GitHub: https://github.com/Jona163

from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpeta donde se almacenan las imágenes subidas y procesadas
UPLOAD_FOLDER = 'static/img/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Rutas permitidas para cargar
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'txt'}

def allowed_file(filename):
    """ Verifica si el archivo tiene una extensión permitida """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def aplicar_sobel(imagen_path):
    """ Aplica el filtro Sobel a una imagen dada y guarda el resultado """
    try:
        imagen = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
        if imagen is None:
            raise ValueError("Imagen no válida o corrupta")
        sobel_x = cv2.Sobel(imagen, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(imagen, cv2.CV_64F, 0, 1, ksize=3)
        magnitud = np.sqrt(sobel_x**2 + sobel_y**2)
        magnitud = np.uint8(255 * magnitud / np.max(magnitud))

        
        # Guardar la imagen resultante
        resultado_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sobel_resultado.png')
        cv2.imwrite(resultado_path, magnitud)
        return 'img/sobel_resultado.png'  # Asegúrate de que esta ruta es correcta
    except Exception as e:
        print(f"Error al aplicar Sobel: {e}")
        return None

def txt_a_imagen(txt_path):
    """ Convierte un archivo de texto de matriz a una imagen y aplica el filtro Sobel """
    try:
        # Leer la matriz desde el archivo de texto
        matriz = np.loadtxt(txt_path, delimiter=',')
        
        # Normalizar la matriz para que sea una imagen
        matriz_normalizada = np.uint8(255 * matriz / np.max(matriz))
        
        # Aplicar el filtro Sobel
        sobel_x = cv2.Sobel(matriz_normalizada, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(matriz_normalizada, cv2.CV_64F, 0, 1, ksize=3)
        magnitud = np.sqrt(sobel_x**2 + sobel_y**2)
        magnitud = np.uint8(255 * magnitud / np.max(magnitud))
        
        # Guardar la imagen resultante
        resultado_path = os.path.join(app.config['UPLOAD_FOLDER'], 'sobel_resultado.png')
        cv2.imwrite(resultado_path, magnitud)
        return 'img/sobel_resultado.png'
    except Exception as e:
        print(f"Error al convertir TXT a imagen y aplicar Sobel: {e}")
        return None

