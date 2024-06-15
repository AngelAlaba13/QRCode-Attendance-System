import cv2
import pyzbar.pyzbar as pyzbar

img = cv2.imread("D:/VS Code Python/TKinter/QRCode Generator/qrcodes/image2.png")
# img = cv2.imread("D:/VS Code Python/TKinter/QRCode Generator/VER 3/qrcodes/Angel Kyle L. Alaba_QRCode.png")



decodedImg = pyzbar.decode(img)
# print(decodedImg)

for obj in decodedImg:
    print("Data: ", obj.data.decode('UTF-8'))
    
    