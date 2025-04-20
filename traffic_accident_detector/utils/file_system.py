import os

def ensure_output_folder_exists(output_folder):
    """
    Verifica si la carpeta de salida existe. Si no, la crea.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
