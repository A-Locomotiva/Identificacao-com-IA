import speech_recognition as sr

def record_audio(duration=5):
    """Grava áudio do microfone por um período definido."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando para o ruído ambiente... Aguarde.")
        recognizer.adjust_for_ambient_noise(source)
        print("Gravando áudio...")
        audio = recognizer.listen(source, timeout=duration)
    return audio

def transcribe_audio(audio):
    """Transcreve o áudio capturado usando o Google Speech Recognition."""
    recognizer = sr.Recognizer()
    try:
        print("Transcrevendo áudio...")
        transcription = recognizer.recognize_google(audio, language="pt-BR")
        return transcription
    except sr.RequestError:
        return "Erro na conexão com o serviço de reconhecimento de fala."
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio."

def record_audio_and_transcribe():
    """Combina a gravação e transcrição em uma função."""
    try:
        audio = record_audio()
        transcription = transcribe_audio(audio)
        return transcription
    except Exception as e:
        return f"Erro ao gravar ou transcrever o áudio: {e}"
