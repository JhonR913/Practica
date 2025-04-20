# Traffic Accident Detector

Una biblioteca Python para detectar accidentes de tránsito en tiempo real utilizando modelos YOLOv8.

## Características

- Detección de accidentes en tiempo real desde cámaras IP, webcams o archivos de video
- Grabación automática de clips cuando se detecta un accidente
- Conservación de buffer previo al accidente
- API sencilla para integración en otros proyectos
- Ejemplos listos para usar

## Instalación

```bash
pip install traffic-accident-detector
```

O directamente desde el repositorio:

```bash
git clone https://github.com/tuusuario/traffic-accident-detector
cd traffic-accident-detector
pip install -e .
```

## Requisitos

- Python 3.7+
- OpenCV
- Ultralytics (YOLOv8)

## Uso básico

```python
from traffic_accident_detector import AccidentDetector

# Inicializar detector con tu modelo entrenado
detector = AccidentDetector(
    model_path="best.pt",
    confidence=0.5,
    consecutive_detections=10
)

# Procesar un archivo de video
detector.process_source("video.mp4", display=True)

# O una cámara IP
detector.process_source("rtsp://usuario:contraseña@ip:puerto/stream", display=True)

# O la webcam local
detector.process_source(0, display=True)
```

## Uso avanzado

### Callbacks personalizados

```python
# Definir callbacks
def on_accident(frame, results):
    # Enviar notificación, activar alarma, etc.
    print("¡Accidente detectado!")

# Configurar callbacks en el detector
detector.set_callbacks(on_accident_detected=on_accident)
```

### Filtrar por clases específicas

```python
# Solo detectar la clase 0 (ajustar según tu modelo)
detector = AccidentDetector(
    model_path="best.pt",
    class_filter=[0]
)
```

## Ejemplos

Consulta la carpeta 'examples' para ver implementaciones completas:

- `examples/video_file.py`: Procesar un archivo de video
- `examples/rtsp_stream.py`: Monitoreo continuo de una cámara IP
- `examples/webcam_detection.py`: Usar la webcam local
