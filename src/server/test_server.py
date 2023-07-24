import sys
import os
import time
import shutil
from pathlib import Path

sys.path.append("../app/")
sys.path.append("../database/")
import app
import db

IMAGE_DIR = Path.cwd() / "images"
DATA_DIR = Path.cwd() / "responses"

if __name__ == "__main__":
    filename = "../database/historial.db"

    #Revisar si hay historial
    if os.path.exists(filename):
        pass
    else:
        print("Creando historial")
        db.create_historial()
    '''
    prompt = "photograph of an astronaut riding a horse"
    files=app.generate_image(prompt, 2)
    for file in files:
        print(file[0])
        db.insert_historial(file[1], file[0])
    
    files=app.generate_variations('perro.png', 2)
    for file in files:
        print(file)
        db.insert_historial(file[1], file[0])
    
    time.sleep(30)
    shutil.rmtree(IMAGE_DIR)
    shutil.rmtree(DATA_DIR)
    '''
    img=db.access_img('gato')
    print(img)
    time.sleep(30)
    for image in img:
        os.remove(image)