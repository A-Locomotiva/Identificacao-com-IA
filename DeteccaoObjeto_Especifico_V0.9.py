from ultralytics import YOLO
import cv2
import numpy as np
import speech_recognition as sr
import pyttsx3

windowName = "Camera"

# Inicializa o motor TTS
engine = pyttsx3.init()

# Função para falar o resultado
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Abrir câmera selecionada
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Camera não foi encontrada/Ocorreu um erro")
    exit()

# Carregamento do Modelo do YOLOV8
model = YOLO("yolov8s.pt")

# Criação de um dicionário para transformar as IDs dos objetos nos nomes
class_names = model.names

# Função para ouvir o microfone
def ouvirMicrofone():
    rec = sr.Recognizer()
    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic)
        print("Gravando...")
        audio = rec.listen(mic)
        try:
            texto = rec.recognize_google(audio, language='pt-BR')
            print(texto)
            return texto
        except sr.UnknownValueError:
            print("Não Entendi")
            return ""

object_to_search = ouvirMicrofone()

# Cores aleatórias para os quadrados em volta dos objetos
colors = np.random.randint(0, 255, size=(len(class_names), 3), dtype='uint8')

# Flag para verificar se o objeto já foi falado
object_found = False

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
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
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

            if searched_object_position and not object_found:
                # Posição do objeto procurado
                centro_x = (searched_object_position[0] + searched_object_position[2]) / 2
                centro_y = (searched_object_position[1] + searched_object_position[3]) / 2

                # Compara a posição com os outros objetos
                for obj_name, (x1, y1, x2, y2) in detected_objects:
                    if obj_name.lower() != object_to_search.lower():
                        # Calcula o centro para os outros objetos
                        other_centro_x = (x1 + x2) / 2
                        other_centro_y = (y1 + y2) / 2

                        # Determina a posição relativa do objeto procurado em relação aos outros
                        if centro_x < other_centro_x:
                            relative_position_x = "à esquerda"
                        else:
                            relative_position_x = "à direita"

                        if centro_y < other_centro_y:
                            relative_position_y = "acima"
                        else:
                            relative_position_y = "abaixo"

                        # Exibe a mensagem formatada
                        result_message = f"O objeto '{object_to_search}' está {relative_position_y} e {relative_position_x} do objeto '{obj_name}'."
                        print(result_message)
                        speak(result_message)
                        object_found = True  # Marca que o objeto foi encontrado e falado

            elif not searched_object_position and object_found:
                # Se o objeto não for encontrado novamente, reseta a flag
                object_found = False
                not_found_message = f"O objeto '{object_to_search}' não foi encontrado."
                print(not_found_message)
                speak(not_found_message)

        # Imagem da câmera enquanto acontece o código de detecção
        cv2.imshow(windowName, frame)

    k = cv2.waitKey(1)

    # Fechar código se pressionar a tecla "X"
    if k == ord('x'):
        break

# Interromper todas as janelas e detecções
cv2.destroyAllWindows()
cap.release()
print("Closing")

'''
ToDo:
- Permitir que o usuário faça outra pergunta
- Caso não consiga entender a fala do usuário, rodar função de gravação de voz de novo até conseguir identificar
'''
