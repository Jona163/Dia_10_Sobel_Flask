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


@app.route('/')
def index():
    """ Página principal con el formulario para subir imágenes o archivos .txt """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """ Maneja la subida de imágenes y archivos .txt """
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return redirect(request.url)
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    result_image_path = None
    file_content = None
    error_message = None
    result_type = None


    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        result_image_path = aplicar_sobel(file_path)
        if result_image_path is None:
            error_message = "La imagen está corrupta o no es válida."
        result_type = 'imagen'
    elif filename.lower().endswith('.txt'):
        result_image_path = txt_a_imagen(file_path)
        if result_image_path is None:
            error_message = "El archivo .txt no pudo ser procesado."
        with open(file_path, 'r') as f:
            file_content = f.read()
        result_type = 'txt'

    return render_template('index.html', original_file=filename, result_image=result_image_path, file_content=file_content, result_type=result_type, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
