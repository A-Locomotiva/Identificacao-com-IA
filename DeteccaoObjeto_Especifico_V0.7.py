from ultralytics import YOLO
import cv2
import numpy as np

windowName = "Camera"

# Abrir câmera selecionada
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera não foi encontrada/Ocorreu um erro")
    exit()

# Carregamento do Modelo do YOLOV8
model = YOLO("yolov8s.pt")

# Criação de um dicionário para transformar as IDs dos objetos nos nomes
class_names = model.names

# Input para pesquisar por um objeto em específico
object_to_search = input("Escreva o objeto a ser procurado: ")

#Cores aleatórias para os quadrados em volta dos objetos
colors = np.random.randint(0, 255, size=(len(class_names), 3), dtype='uint8')

while True:
    success, frame = cap.read()
    
    if success:
        results = model(frame)
        
        # Guarda a posição dos objetos detectados em uma lista
        detected_objects = []

        # Processamento dos resultados
        for result in results:
            boxes = result.boxes  # Resultado das caixas em volta dos objetos 
            for box in boxes:
                # Coordenadas dos objetos
                x1, y1, x2, y2 = box.xyxy[0].numpy()
                confidence = box.conf[0].item()  # Porcentagem de Certeza
                class_id = int(box.cls[0].item())  # ID do objeto

                # Transformação do ID do objeto para o nome | Somente para fins visuais
                object_name = class_names[class_id]

                # Guarda as coordenadas dos objetos
                detected_objects.append((object_name, (x1, y1, x2, y2)))

                # Desenhar as caixas de detecção em volta dos objetos
                color = colors[class_id]
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color.tolist(), 2)
                cv2.putText(frame, f'{object_name} {confidence:.2f}', (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color.tolist(), 2)

        # Encontrar coordenadas do objeto procurado baseado em outros objetos
        searched_object_position = None
        for obj_name, (x1, y1, x2, y2) in detected_objects:
            if obj_name.lower() == object_to_search.lower():
                searched_object_position = (x1, y1, x2, y2)
                break

        if searched_object_position:
            # Analisa a posição do objeto procurado
            largura_tela, altura_tela = frame.shape[1], frame.shape[0]
            centro_x = (searched_object_position[0] + searched_object_position[2]) / 2
            centro_y = (searched_object_position[1] + searched_object_position[3]) / 2

            # Torna o objeto procurado o "centro da tela"
            print(f"O objeto '{object_to_search}' está no centro da tela.")

            # Compara a posição com os outros objetos
            relative_positions = []
            for obj_name, (x1, y1, x2, y2) in detected_objects:
                if obj_name.lower() != object_to_search.lower():
                    # Calcula o centro para os outros objetos
                    other_centro_x = (x1 + x2) / 2
                    other_centro_y = (y1 + y2) / 2

                    if other_centro_x < centro_x:
                        relative_position_x = "à esquerda"
                    else:
                        relative_position_x = "à direita"

                    if other_centro_y < centro_y:
                        relative_position_y = "acima"
                    else:
                        relative_position_y = "abaixo"

                    relative_positions.append(f"{obj_name} está {relative_position_x} e {relative_position_y} do '{object_to_search}'.")

            # Mostra a posição baseada em outros objetos
            for position in relative_positions:
                print(position)

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