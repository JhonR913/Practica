import sys
import os
import tkinter as tk
from traffic_accident_detector.detector import AccidentDetector
from traffic_accident_detector.utils.file_dialog import select_video_file, select_output_folder
from traffic_accident_detector.utils.file_system import ensure_output_folder_exists

# Añadir la carpeta principal del proyecto a sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'traffic_accident_detector')))

def on_accident(path: str):
    """
    Callback que se ejecuta al detectar un accidente.
    """
    print(f"Accidente detectado y guardado en: {path}")

def main():
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter

    # Selección del archivo de video
    video_path = select_video_file()
    if not video_path:
        print("No se seleccionó un video.")
        return

    # Selección de la carpeta de salida
    output_folder = select_output_folder()
    if not output_folder:
        print("No se seleccionó carpeta de salida.")
        return

    # Asegurarse de que la carpeta de salida exista
    ensure_output_folder_exists(output_folder)

    try:
        # Iniciar el detector de accidentes
        detector = AccidentDetector(
            save_clips=True,
            output_dir=output_folder,
            callback=on_accident
        )
        print(f"Procesando video: {video_path}")
        detector.detect_from_video(video_path)
    except FileNotFoundError as e:
        print(f"No se encontró el archivo: {e}")
    except RuntimeError as e:
        print(f"Error de ejecución: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        root.quit()  # Cierra la ventana de tkinter

if __name__ == "__main__":
    main()
