import tkinter as tk
from tkinter import filedialog

def select_video_file():
    """
    Muestra un diálogo para seleccionar un archivo de video.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter
    video_path = filedialog.askopenfilename(
        title="Selecciona el archivo de video",
        filetypes=[("Videos", "*.mp4 *.avi *.mov *.mkv")]
    )
    return video_path

def select_output_folder():
    """
    Muestra un diálogo para seleccionar una carpeta de salida.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter
    output_folder = filedialog.askdirectory(
        title="Selecciona la carpeta donde guardar las grabaciones procesadas"
    )
    return output_folder
