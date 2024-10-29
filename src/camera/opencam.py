import cv2

def initialize_camera(camera_index=1):
    cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("Camera não foi encontrada/ocorreu um erro")
        exit()
    return cap