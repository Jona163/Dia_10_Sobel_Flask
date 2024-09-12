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
