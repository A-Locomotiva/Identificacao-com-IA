from ultralytics import YOLO
import cv2
import numpy as np


windowName = "Camera"
# Abrir câmera selecionada

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera não foi encontrada/ocorreu um erro")
    exit()

# Carregamento do Modelo do YOLOV8
model = YOLO("yolov8s.pt")

# Criação de um dicionário para transformar as IDs dos objetos, nos nomes
class_names = model.names

seguir = False

while True:
    success, frame = cap.read()
    
    if success:
        if seguir:
            results = model.track(frame, persist=True)
        else:
            results = model(frame)
        
        # Resultados
        for result in results:
            boxes = result.boxes  # Resultado das caixas em volta dos objetos
            for box in boxes:
                # Coordenadas dos objetos
                x1, y1, x2, y2 = box.xyxy[0].numpy() 
                confidence = box.conf[0].item()  # Porcentagem de Certeza
                class_id = int(box.cls[0].item())  # ID do objeto

                # Transformação do ID do objeto para o nome | Somente para fins visuais
                object_name = class_names[class_id]

                # Desenhar as caixas de detecção em volta dos objetos
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
                # Mostrar nome e porcentagem de certeza da detecção de um objeto
                cv2.putText(frame, f'{object_name} {confidence:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                # Função para determinar a posição do objeto na tela
                def analisar_posicao(x1, y1, x2, y2, largura_tela, altura_tela):
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
                
                largura_tela, altura_tela = frame.shape[1], frame.shape[0]

                # Calcula a posição do objeto
                posicao = analisar_posicao(x1, y1, x2, y2, largura_tela, altura_tela)              
                                    
                # Print do resultado dos objetos e sua posição
                print(f"O objeto '{object_name}' está {posicao}.")

        # Imagem da câmera enquanto acontece o código de detecção
        cv2.imshow(windowName, frame)

    k = cv2.waitKey(1)

    # Fechar código se pressionar a tecla "X"
    if k == ord('x'):
        break
    
    # Se a janela da câmera for fechada, interrompe o código
    if cv2.getWindowProperty(windowName, cv2.WND_PROP_VISIBLE) < 1:
        break

# Interromper todas as janelas e detecções
cv2.destroyAllWindows()
cap.release()
print("Closing")