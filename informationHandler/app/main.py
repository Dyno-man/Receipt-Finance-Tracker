from fastapi import FastAPI, UploadFile
import httpx
from PIL import Image
import io
import subprocess
import requests

imageContainerAddress = 'http://172.17.0.2:80'

app = FastAPI()

# Health check to make sure backend is accesible
@app.get('/health')
async def health():
    response = requests.get(imageContainerAddress)
    print(response)
    return response.json()

@app.post("/upload")
async def send_to_image_container(file: UploadFile):
# Take file name and create a save for it inside of the container    
    filepath_save = f'/code/app/images/{file.filename}'

# Take image and wait for contents to read all of it, then open the image in bytes to double check it's an image, then save the image to the container
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img.save(filepath_save)
    
# Open the image as bytes, create a file json obj with the necessary data    
    with open(filepath_save, 'rb') as img_file:
        files = {
            'file' : (file.filename, img_file.read(), file.content_type)
        }

# Send the image obj to the backend docker container to be processed
        req = requests.post(f'{imageContainerAddress}/upload', files=files)

# Return the information to the sender
        return req.json()
