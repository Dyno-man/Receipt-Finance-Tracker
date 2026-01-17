import easyocr
import requests


def pretty_print(l):
    for i in l:
        print(i)

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



totalCost = []
reader = easyocr.Reader(['en'])

ran = 1
test_pic = '/home/grant/Pictures/test3-receipt.webp'
pic = '/home/grant/Pictures/test'
ture = '-receipt.webp'
val = 'total'
for i in range(3):
    full = pic + str((i+1)) + ture
    result = reader.readtext(full, detail = 0)

    cost = find_total(result)
    totalCost.append(cost)



print(totalCost)