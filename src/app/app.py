import os
import openai
import json
from dotenv import load_dotenv
from pathlib import Path
from base64 import b64decode

#Load the .env file
load_dotenv()

#Get the api key
openai.api_key = os.getenv("OPENAI_API_KEY")

#Function that generates image from prompt
def generate_image(PROMPT, number=1, SIZE="512x512"):

    #Folders to store json files
    DATA_DIR = Path.cwd() / "responses"
    DATA_DIR.mkdir(exist_ok=True)

    response= openai.Image.create(prompt=PROMPT, 
        n=number, 
        size=SIZE, 
        response_format="b64_json",
        )
    
    #Save json files
    file_name = DATA_DIR / f"{PROMPT}-{response['created']}.json"
    with open(file_name, mode="w", encoding="utf-8") as file:
        json.dump(response, file)

    #Folder to save files temporarily
    JSON_FILE = DATA_DIR / file_name
    IMAGE_DIR = Path.cwd() / "images" / JSON_FILE.stem
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    files=[]

    #Convert json files into png
    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
        response = json.load(file)
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
        image_name=image_file.stem
        files.append([image_file, image_name])
        with open(image_file, mode="wb") as png:
            png.write(image_data)

    return files

#Function that creates variations from an image
def generate_variations(image_data, number=1, SIZE="512x512"):
    #Folders to store json files
    DATA_DIR = Path.cwd() / "responses"
    DATA_DIR.mkdir(exist_ok=True)

    response = openai.Image.create_variation(
       image=open(image_data, 'rb'),
       n=number,
       size=SIZE,
       response_format="b64_json",
       )

    file_name = DATA_DIR / f"vary-{image_data[:-4]}-{response['created']}.json"
    with open(file_name, mode="w", encoding="utf-8") as file:
       json.dump(response, file)

    #Folder to save files temporarily
    JSON_FILE = DATA_DIR / file_name
    IMAGE_DIR = Path.cwd() / "images" / JSON_FILE.stem
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    files=[]

    #Convert json files into png
    with open(JSON_FILE, mode="r", encoding="utf-8") as file:
        response = json.load(file)
    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = IMAGE_DIR / f"{JSON_FILE.stem}-{index}.png"
        image_name=image_file.stem
        files.append([image_file, image_name])
        with open(image_file, mode="wb") as png:
            png.write(image_data)

    return files