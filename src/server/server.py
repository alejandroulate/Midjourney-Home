from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import os
import time
import shutil
from pathlib import Path
sys.path.append("../app/")
sys.path.append("../database/")
import app
import db

import base64
from PIL import Image
import io

#def convert_base64_to_png(base64_string, output_filename):




IMAGE_DIR = Path.cwd() / "images"
DATA_DIR = Path.cwd() / "responses"

class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/process-text':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            text = data['text']
            variations = data['variations']
            print("Texto recibido del cliente:", text, variations)

            # Lógica para generar imágenes

            files=app.generate_image(text, int(variations))
            images=[]
            for file in files:
                print(file[0])
                db.insert_historial(file[1], file[0])
                images.append(str(file[0]))
            #print(images)
            # images = ["perro.png", "perro.png", "perro.png"]


            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(images).encode('utf-8'))
            #time.sleep(30)
            #shutil.rmtree(IMAGE_DIR)
            #shutil.rmtree(DATA_DIR)
        elif self.path == '/access-history':
            print("Señal para acceder al historial recibida del cliente")

            # Lógica para acceder al historial aquí
            images =db.access_historial()
            for i in range(len(images)):
                images[i]='../server/'+images[i]
            
            #images = ["perro.png", "perro.png", "perro.png"]

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(images).encode('utf-8'))
            #time.sleep(30)
            #for image in images:
            #    os.remove(image)

        elif self.path == '/subscribe':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            category = data['category']
            print("Subscribed to category:", category)

            # Lógica para devolver imagenes de cateogría
            images = db.access_img(category)
            for i in range(len(images)):
                images[i]='../server/'+images[i]
            print(images)
            #images = ["perro.png", "perro.png", "perro.png"]

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(images).encode('utf-8'))
            #for image in images:
            #    os.remove(image)

        elif self.path == '/upload-image':
            print('Variaciones de imagen')
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Obtener el archivo de imagen en formato base64
            image_data = data.get('image')
            name = data.get('fileName')
            variations=data.get('number')
            print(variations, name)
            header, base64_data = image_data.split(',')
            # print("ImageData" + image_data)
            #file_type = data.get('fileType')
            #print("Filetype:" + file_type)

            if base64_data:
                # Decodificar el archivo base64 y guardar la imagen en el servidor
                image_bytes = base64.b64decode(base64_data)
                image = Image.open(io.BytesIO(image_bytes))
                image.save(name)

                # Lógica para generar imágenes

                files=app.generate_variations(name, variations)
                images=[]
                for file in files:
                    print(file[0])
                    db.insert_historial(file[1], file[0])
                    images.append(str(file[0]))

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(images).encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

    def do_GET(self):
        if self.path == '/categories':

            # Actualizar categorías
            categories = db.access_categoria()
            #categories =['Category 1', 'Category 2', 'Category 3', 'Category 4']  # Ejemplo de lista de categorías

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(categories).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()       

filename = "../database/historial.db"

#Revisar si hay historial
if os.path.exists(filename):
    print('Historial existente')
else:
    print("Creando historial")
    db.create_historial()

server_address = ('localhost', 8000)
httpd = HTTPServer(server_address, RequestHandler)
print('Servidor en ejecución en localhost:8000')
httpd.serve_forever()