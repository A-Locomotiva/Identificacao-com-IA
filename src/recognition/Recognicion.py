"""!pip install torch torchvision
!pip install opencv-python-headless
!pip install pyttsx3
!pip install SpeechRecognition pyaudio
!git clone https://github.com/ultralytics/yolov5  # Clona o repositório do Github YOLOv5
!pip install -r yolov5/requirements.txt  # Instala dependências do YOLO
!pip install sounddevice
!pip install SpeechRecognition
!pip install torch torchvision"""

import torch
import cv2
import pyttsx3
import sounddevice as sd 
import speech_recognition as sr 
import numpy as np
from ultralytics import YOLO


model = YOLO("yolo11n.pt") 
# Configurar o motor de voz
def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

# Função para capturar e reconhecer fala
def reconhecer_fala():
    recognizer = sr.Recognizer()

    # Função interna para capturar áudio com sounddevice
    def capturar_audio_durante_tempo(duracao=5, fs=44100):
        print("Gravando por 5 segundos...")
        audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1)
        sd.wait()  # Espera a captura de áudio terminar
        return np.squeeze(audio)

    # Grava o áudio do microfone durante 5 segundos
    try:
        audio = capturar_audio_durante_tempo()

        # Normaliza o áudio para 16-bit PCM
        audio_data = np.int16(audio * 32767).tobytes()

        # Converte para AudioData do SpeechRecognition
        audio_data = sr.AudioData(audio.tobytes(), 44100, 2)
        texto = recognizer.recognize_google(audio_data, language='pt-BR')
        print(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        print("Não consegui entender a fala.")
        return ""
    except sr.RequestError:
        print("Erro na requisição do serviço de reconhecimento de fala.")
        return ""

# Função para processar a posição do objeto na tela
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

    return f"O objeto está {pos_x} da tela, {pos_y}."

# Captura de imagem da câmera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detecção de objetos
    results = model(frame)
    largura_tela, altura_tela = frame.shape[1], frame.shape[0]

    # Mostrar a imagem com a detecção
    cv2.imshow('Detecção de Objetos', results.render()[0])

    # Processar perguntas do usuário
    texto_pergunta = reconhecer_fala()

    if texto_pergunta:
        for obj in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = obj
            objeto = model.names[int(cls)]
            
            if objeto in texto_pergunta:
                posicao = analisar_posicao(x1, y1, x2, y2, largura_tela, altura_tela)
                resposta = f"O {objeto} está {posicao}."
                print(resposta)
                falar(resposta)
                break
    
    # Interromper o loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()