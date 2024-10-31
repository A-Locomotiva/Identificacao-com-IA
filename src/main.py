import tkinter as tk
from tkinter import messagebox
from recognition.utils import initialize_camera, capture_frame, load_yolo_model, process_frame, release_camera
from audio.audio_util import record_audio_and_transcribe

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Identificação Combinada")
        self.camera = None
        self.model = None
        self.initialize_ui()

    def initialize_ui(self):
        tk.Button(self.root, text="Inicializar Câmera", command=self.start_camera).pack()
        tk.Button(self.root, text="Capturar Imagem", command=self.capture_image).pack()
        tk.Button(self.root, text="Gravar Áudio", command=self.record_audio).pack()

    def start_camera(self):
        try:
            self.camera = initialize_camera()
            self.model = load_yolo_model()
            messagebox.showinfo("Câmera", "Câmera inicializada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar câmera: {str(e)}")

    def capture_image(self):
        if self.camera and self.model:
            try:
                frame = capture_frame(self.camera)
                detected_objects = process_frame(self.model, frame)
                messagebox.showinfo("Captura de Imagem", f"Objetos detectados: {', '.join(detected_objects)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao capturar ou processar a imagem: {str(e)}")
        else:
            messagebox.showwarning("Aviso", "Inicialize a câmera primeiro.")

    def record_audio(self):
        transcription = record_audio_and_transcribe()
        messagebox.showinfo("Transcrição de Áudio", f"Transcrição: {transcription}")

    def on_close(self):
        if self.camera:
            release_camera(self.camera)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
