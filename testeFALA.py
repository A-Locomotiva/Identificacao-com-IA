import pyttsx3
from ultralytics import YOLO
import cv2
import numpy as np
import os
import speech_recognition as sr

def falaIa():
    # Inicialize o mecanismo TTS
    engine = pyttsx3.init()

    # Obtenha a lista de vozes disponíveis e selecione uma
    voices = engine.getProperty("voices")
    for voice in voices:
        print(voice.id)

    # Defina a voz para "brazil"
    engine.setProperty("voice", "brazil")

    # Defina o texto que você deseja que o Python fale
    text = ouvirMicrofone()

    # Fale o texto
    engine.say(text)

    # Aguarde até que a fala seja concluída antes de encerrar o programa
    engine.runAndWait()

    return text


def ouvirMicrofone():

   #Habilita o microfone 
    rec = sr.Recognizer()

    #mic = sr.Microphone()

    #print(sr.Microphone().list_microphone_names())

    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic)
        print("Gravando...")
        audio = rec.listen(mic)
        try:
            texto = rec.recognize_google(audio, language='pt-BR')
            print(texto)

            #if "navegador" in texto:
                #os.system("start Chrome.exe")

        except sr.UnkownValueError:
            print("Não Entendi")
    
    return texto


falaIa()



