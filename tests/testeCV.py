from ultralytics import YOLO
import cv2
import numpy as np
import os

windowName = "CameraReceba"

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("nao abriu")

while True:
    resp, frame = cap.read()

    if not resp:
        print("nao tem resposta")
        break

    cv2.imshow(windowName, frame)

    k = cv2.waitKey(1)

    #Ao apertar a tecla "q" fecha a camera
    if k == ord('q'):
        break

    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
cap.release()
print("Fechando")


