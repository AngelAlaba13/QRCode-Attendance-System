import cv2
import numpy as np
from pyzbar.pyzbar import decode
import re

name, year, block = None, None, None

def convertedData(data):
    string = str(data)
    # print("Decoded Data: ", string)

    name_pattern = r'Name:\s*(.*?)\s*Year\s*and\s*Block:'
    year_block_pattern = r'Year\s*and\s*Block:\s*(\d+)[A-Za-z]*([A-Za-z])$' 
    
    name_match = re.search(name_pattern, string)
    if name_match:
        name = name_match.group(1).strip()

    year_block_match = re.search(year_block_pattern, string)
    if year_block_match:
        year = year_block_match.group(1)
        block = year_block_match.group(2)
   
    print(f"Name: {name}")
    print(f"Year: {year}")
    print(f"Block: {block}")
    
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break
    
    name = None
    year, block = None, None

    for code in decode(img):
        decoded_data = code.data.decode('UTF-8')
        # print("Uncoded Data: ",decoded_data)
        # print()
        convertedData(decoded_data)
         
        rect_pts = code.rect
        if decoded_data:
            pts = np.array([code.polygon], np.int32)
            cv2.polylines(img, [pts], True, (0, 225, 0), 3)
            

    cv2.imshow("Img: ", img)
    cv2.waitKey(1)
    
cap.release()