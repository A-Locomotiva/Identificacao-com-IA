# Use uma imagem base do Python
FROM python:3.9-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    portaudio19-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências do Python
RUN pip install --upgrade pip

# Instalar dependências do PyTorch e OpenCV
RUN pip install torch torchvision opencv-python-headless pyttsx3 sounddevice SpeechRecognition pyaudio

# Clonar o repositório YOLOv5
RUN git clone https://github.com/ultralytics/yolov8

# Instalar dependências do YOLOv5
RUN pip install -r yolov5/requirements.txt

# Definir o diretório de trabalho da aplicação
WORKDIR /app

# Copiar todos os arquivos do projeto para dentro do contêiner
COPY . .

# Comando para executar o script principal
CMD ["python", "src/main.py"]

