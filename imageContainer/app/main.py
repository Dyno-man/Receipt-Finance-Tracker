from fastapi import FastAPI, File, UploadFile
import easyocr
from PIL import Image
import io

"""Helper functions for the file"""

def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False

# Return a total cost, sometimes total comes before or after the total price so this function looks ahead
# and behind to see where the number may be hiding
def find_total(result):
    #Take the list and find the keyword 'total'
    for i in range(len(result)):
        if 'subtotal' in result[i].lower():
            continue
        elif 'total' in result[i].lower():
            if is_float(result[i-1].replace(' ', '')):
                return float(result[i-1].replace(' ', ''))
            elif i+1 != len(result) and is_float(result[i+1].replace(' ', '')):
                return float(result[i+1].replace(' ', ''))
    return -1

#This will take in the filepath as the image will be temporarily stored to the docker image
# and once the image has been processed and total found. We will return number
def scan_image(model, filepath):
    result = model.readtext(filepath, detail = 0)
    cost = find_total(result)
    return cost

model = easyocr.Reader(['en'])


"""This is the Router"""

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

# Write a route that accepts incoming images and passes them to the active OCR model. The model turns on as soon as the FASTAPI middleware is activated.
@app.get('/process/{filepath}')
async def process_image(filepath):
    cost = scan_image(model, filepath)
    return {'cost' : cost}


@app.post('/upload')
async def store_uploaded_file(file: UploadFile):
    #Take the uploaded picture, check to see if it is actually a picture
    filepath = f"/code/app/images/{file.filename}"
    try:
        contents = await file.read()
        print(contents)
        img = Image.open(io.BytesIO(contents))
        img.save(filepath)
    except Exception as e:
        return {"Error": "Failed to upload open file: " + str(e)}

    #If Object is an img, then run it through the scan_image function
    result = scan_image(model, filepath)

    return {"Ok" : result}

    
