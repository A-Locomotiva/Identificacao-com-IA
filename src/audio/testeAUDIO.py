#pip install pyaudio
#pip install SpeechRecognition

import speech_recognition as sr
import os


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

ouvirMicrofone()




