import os
from ultralytics import YOLO
from typing import Dict, Any

def load_model(model_path: str, device: str = "auto") -> YOLO:
    """
    Carga un modelo YOLO desde una ruta
    """
    try:
        model = YOLO(model_path)
        if device != "auto":
            model.to(device)
        return model
    except Exception as e:
        raise RuntimeError(f"Error al cargar el modelo desde {model_path}: {e}")

def get_model_info(model: YOLO) -> Dict[str, Any]:
    """
    Obtiene información sobre un modelo YOLO
    """
    return {
        "task": getattr(model, "task", "unknown"),
        "names": getattr(model, "names", {}),
        "device": str(getattr(model, "device", "unknown")),
    }

def select_model_file() -> str:
    """
    Retorna la ruta al archivo `best.pt` que debe estar en el directorio raíz del paquete.
    """
    model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'best.pt')
    if os.path.exists(model_path):
        return model_path
    else:
        raise FileNotFoundError(f"No se encontró 'best.pt' en: {model_path}")
