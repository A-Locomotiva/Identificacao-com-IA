import cv2
from ultralytics import YOLO

def initialize_camera(camera_index=0):
    """Inicializa a câmera."""
    camera = cv2.VideoCapture(camera_index)
    if not camera.isOpened():
        raise Exception("Erro ao abrir a câmera.")
    return camera

def release_camera(camera):
    """Libera a câmera e fecha as janelas abertas do OpenCV."""
    if camera:
        camera.release()
        cv2.destroyAllWindows()

def capture_frame(camera):
    """Captura um frame da câmera."""
    ret, frame = camera.read()
    if not ret:
        raise Exception("Erro ao capturar o frame da câmera.")
    return frame

def load_yolo_model(model_path='yolov8n.pt'):
    """Carrega o modelo YOLO."""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        raise Exception(f"Erro ao carregar o modelo YOLO: {e}")

def process_frame(model, frame):
    """Processa o frame para detecção de objetos e retorna os nomes dos objetos detectados."""
    results = model(frame)
    detected_objects = [result['name'] for result in results]
    return detected_objects
