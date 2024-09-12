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
