import os
import cv2
import torch
from datetime import datetime
from traffic_accident_detector.models.loader import load_model, select_model_file
from PyQt5.QtGui import QImage, QPixmap


class AccidentDetector:
    def __init__(self,
                 model_path: str = None,
                 save_clips: bool = True,
                 output_dir: str = 'detected_clips',
                 callback=None,
                 consecutive_threshold: int = 10,
                 confidence_threshold: float = 0.5,
                 device: str = "auto",
                 update_label_callback=None):  # Callback para actualizar el QLabel
        if model_path is None:
            model_path = select_model_file()

        self.model = load_model(model_path, device)
        self.save_clips = save_clips
        self.output_dir = output_dir
        self.callback = callback
        self.consecutive_threshold = consecutive_threshold
        self.confidence_threshold = confidence_threshold
        self.update_label_callback = update_label_callback  # Callback para actualizar el QLabel

        if save_clips and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.target_labels = {'severe'}

    def convert_frame_to_pixmap(self, frame):
        """Convierte un fotograma de OpenCV (BGR) a un QPixmap para mostrar en QLabel"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convierte de BGR a RGB
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap(q_image)

    def detect_from_video(self, video_path: str):
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("No se pudo abrir el video")

            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            writer = None
            accident_active = False
            detection_count = 0
            cooldown_frames = 0
            title_displayed = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                results = self.model(frame)[0]
                annotated_frame = frame.copy()
                has_relevant = False

                for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
                    class_name = str(self.model.names[int(cls)])
                    if conf >= self.confidence_threshold and class_name in self.target_labels:
                        has_relevant = True
                        x1, y1, x2, y2 = map(int, box)
                        label = f"Accidente {conf:.2f}"
                        color = (0, 0, 255)  # rojo
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(annotated_frame, label, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                if has_relevant:
                    detection_count += 1
                    if detection_count >= self.consecutive_threshold and not accident_active:
                        accident_active = True
                        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                        clip_name = os.path.join(self.output_dir, f'accidente_detectado_{ts}.mp4')
                        writer = cv2.VideoWriter(clip_name, fourcc, fps, (width, height))
                        print(f"Accidente confirmado. Guardando en: {clip_name}")
                        if self.callback:
                            self.callback(clip_name)
                else:
                    if detection_count > 0:
                        detection_count -= 1

                if accident_active and not title_displayed:
                    cv2.putText(annotated_frame, "Accidente Detectado", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
                    title_displayed = True

                if accident_active and writer:
                    writer.write(annotated_frame)
                    cooldown_frames += 1
                    if detection_count == 0 and cooldown_frames > fps * 2:
                        accident_active = False
                        cooldown_frames = 0
                        title_displayed = False
                        writer.release()
                        writer = None
                        print("Grabación finalizada por fin de accidente.")

                # Si tenemos el callback para actualizar el QLabel, lo llamamos
                if self.update_label_callback:
                    pixmap = self.convert_frame_to_pixmap(annotated_frame)
                    self.update_label_callback(pixmap)

                cv2.imshow('Detección de Accidentes', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print(f"Error al procesar el video: {e}")
