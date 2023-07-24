import sqlite3
import os
from PIL import Image
from io import BytesIO
from pathlib import Path

# Get the directory containing this module
module_dir = os.path.dirname(__file__)

# Join the directory with the filename
history_path= os.path.join(module_dir, "historial.db")

database_path=os.path.join(module_dir, "imagenes.db")

def open_db():
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    return [connection, cursor]

def open_historial():
    connection = sqlite3.connect(history_path)
    cursor = connection.cursor()
    return [connection, cursor]

def create_table():
    connection, cursor = open_db()
    # Se crea una tabla para contener las imagenes generadas por IA
    cursor.execute("""
    CREATE TABLE imagenes 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    prompt TEXT NOT NULL, 
    categoria TEXT NOT NULL, 
    content BLOB NOT NULL)""")

    connection.commit()
    connection.close()

def create_historial():
    connection, cursor = open_historial()
    cursor.execute("""
    CREATE TABLE historial 
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nombre TEXT NOT NULL, 
    categoria TEXT NOT NULL, 
    content BLOB NOT NULL)""")

    connection.commit()
    connection.close()

def insert_img(prompt,categoria,filename):
    connection, cursor = open_db()
    blob = convert_img(filename)

    # Se inserta la imagen en la base de datos, especificando su prompt
    # asociado y categoria
    cursor.execute("""INSERT INTO imagenes 
                   (prompt, categoria, content) 
                   VALUES (?,?,?)""",(prompt,categoria,blob,))
    connection.commit()
    connection.close()

def insert_historial(nombre, imagen, categoria='historial'):
    connection, cursor = open_historial()

    imagen=convert_img(imagen)

    cursor.execute("""INSERT INTO historial 
                   (nombre, categoria, content) 
                   VALUES (?,?,?)""",(nombre,categoria,imagen,))
    connection.commit()
    connection.close()

def convert_img(filename):
    with open(filename, 'rb') as img:
        blob_img = img.read()
        return blob_img

def access_img(categoria):
    # Conexión a la base de datos
    conn, cursor = open_db()

    # Consulta SQL para obtener las imágenes de la categoría especificada
    query = "SELECT prompt, content FROM imagenes WHERE categoria = ?"
    cursor.execute(query, (categoria,))

    # Recorremos los resultados y mostramos las imágenes
    images=[]
    for row in cursor.fetchall():
        nombre = row[0]
        dato_binario = row[1]
        print(nombre)
        imagen = Image.open(BytesIO(dato_binario))
        #imagen.show()
        name=nombre+'.png'
        images.append(name)
        imagen.save(nombre+'.png')

    # Cerramos la conexión a la base de datos
    conn.close()
    return images

def access_historial(categoria='historial'):
    # Conexión a la base de datos
    conn, cursor = open_historial()

    # Consulta SQL para obtener las imágenes de la categoría especificada
    query = "SELECT nombre, content FROM historial WHERE categoria = ?"
    cursor.execute(query, (categoria,))

    # Recorremos los resultados y mostramos las imágenes
    images=[]
    for row in cursor.fetchall():
        nombre = row[0]
        dato_binario = row[1]
        print(nombre)
        imagen = Image.open(BytesIO(dato_binario))
        #imagen.show()
        name=nombre+'.png'
        images.append(name)
        imagen.save(nombre+'.png')

    # Cerramos la conexión a la base de datos
    conn.close()
    return images
    
def access_categoria():
    connection, cursor = open_db()
    # Consulta SQL de todas las categorias
    cursor.execute("SELECT categoria FROM imagenes")
    
    categorias = []
    for categoria in cursor.fetchall():
        categorias.append(categoria)

    # Eliminar nombres de categorias repetid
    categorias = list(dict.fromkeys(categorias))

    categories=[]
    for categoria in categorias:
        print(categoria[0])
        categories.append(categoria[0])
    
    return categories

"""
create_table()
insert_img("genera una imagen de un perro husky", "perro", "./src/database/images/perros/husky.jpg")
insert_img("genera una imagen de un pug", "perro", "./src/database/images/perros/pug.jpeg")

insert_img("genera una imagen de un gato blanco", "gato", "./src/database/images/gatos/blanco.jpeg")
insert_img("genera una imagen de un gato de ojos verdes", "gato", "./src/database/images/gatos/verdes.png")
insert_img("genera una imagen de un gato naranja", "gato", "./src/database/images/gatos/garfield.jpg")

insert_img("genera una imagen de un caballo blanco", "caballo", "./src/database/images/caballos/blanco.jpg")
insert_img("genera una imagen de un caballo cafe", "caballo", "./src/database/images/caballos/cafe.jpg")
insert_img("genera una imagen de dos caballos", "caballo", "./src/database/images/caballos/dos.jpg")
"""

#access_img("caballos")