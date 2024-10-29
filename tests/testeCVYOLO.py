from ultralytics import YOLO
import cv2
import numpy as np
import os

windowName = "CameraReceba"

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("nao abriu")

model = YOLO("yolov8s.pt")

seguir = False

while True:
    success, frame = cap.read()
    
    if success:
        if seguir:
            results = model.track(frame, persist=True)
        else:
            results = model(frame)
        
        for result in results:
            frame = result.plot()

        #mostrar a camera
        cv2.imshow(windowName, frame)

    k = cv2.waitKey(1)

    #Ao apertar a tecla "q" fecha a camera
    if k == ord('q'):
        break
    
    #Pode fechar no X da camera
    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
cap.release()
print("Fechando")


