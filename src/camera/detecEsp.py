# camera_detection.py

from ultralytics import YOLO
import cv2

# Função para inicializar a câmera


# Função para carregar o modelo YOLOv8
def load_yolo_model(model_path="yolov8s.pt"):
    model = YOLO(model_path)
    return model

# Função para processar o quadro da câmera com o modelo YOLO
def detect_objects(model, frame):
    results = model(frame)
    return results

# Função para desenhar caixas e mostrar informações na imagem
def draw_detections(frame, results, object_to_search, class_names):
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Coordenadas dos objetos
            x1, y1, x2, y2 = box.xyxy[0].numpy()
            confidence = box.conf[0].item()
            class_id = int(box.cls[0].item())

            object_name = class_names[class_id]

            if object_name.lower() == object_to_search.lower():
                # Desenhar caixa de detecção
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                cv2.putText(frame, f'{object_name} {confidence:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Calcula e exibe a posição do objeto na tela
                largura_tela, altura_tela = frame.shape[1], frame.shape[0]
                posicao = analyze_position(x1, y1, x2, y2, largura_tela, altura_tela)
                print(f"O objeto '{object_to_search}' está {posicao}.")

# Função para determinar a posição do objeto na tela
def analyze_position(x1, y1, x2, y2, largura_tela, altura_tela):
    centro_x = (x1 + x2) / 2
    centro_y = (y1 + y2) / 2

    if centro_x < largura_tela / 3:
        pos_x = "à esquerda"
    elif centro_x > 2 * largura_tela / 3:
        pos_x = "à direita"
    else:
        pos_x = "no centro"

    if centro_y < altura_tela / 3:
        pos_y = "no topo"
    elif centro_y > 2 * altura_tela / 3:
        pos_y = "na parte inferior"
    else:
        pos_y = "no meio"

    return f"{pos_x} e {pos_y}"

# Função para liberar a câmera e fechar a janela
def close_camera(cap):
    cap.release()
    cv2.destroyAllWindows()

# Função principal para executar o loop de detecção
def run_detection_loop(model, cap, object_to_search):
    class_names = model.names
    windowName = "Camera"
    
    while True:
        success, frame = cap.read()
        
        if success:
            results = detect_objects(model, frame)
            draw_detections(frame, results, object_to_search, class_names)
            cv2.imshow(windowName, frame)

        k = cv2.waitKey(1)
        if k == ord('x') or cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
            break
