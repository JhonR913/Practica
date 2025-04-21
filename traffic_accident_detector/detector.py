import os
import cv2
import torch
import random
from datetime import datetime, timedelta
from traffic_accident_detector.models.loader import load_model, select_model_file
from PyQt5.QtGui import QImage, QPixmap

class AccidentDetector:
    def __init__(self,
                 model_path: str = None,
                 save_clips: bool = True,                  # <–– lo re‑agregamos
                 output_dir: str = 'detected_clips',
                 callback=None,
                 consecutive_threshold: int = 10,
                 confidence_threshold: float = 0.5,
                 snapshot_cooldown: float = 5.0,   # segundos entre snapshots
                 device: str = "auto",
                 update_label_callback=None,
                 retrain_dir: str = r'C:\Users\jhonr\Desktop\proyecto_deteccion\yolov8'):

        if model_path is None:
            model_path = select_model_file()
        self.model = load_model(model_path, device)

        # aunque ahora no lo usemos para nada, evitamos el TypeError
        self.save_clips = save_clips

        # Carpeta para GUARDAR SOLO EL VIDEO
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # Carpetas para GUARDAR snapshots full-frame + .txt YOLO
        self.retrain_dir = retrain_dir
        for subset in ['train', 'valid', 'test']:
            os.makedirs(os.path.join(self.retrain_dir, subset, 'images'), exist_ok=True)
            os.makedirs(os.path.join(self.retrain_dir, subset, 'labels'), exist_ok=True)

        self.callback = callback
        self.update_label_callback = update_label_callback

        self.consecutive_threshold = consecutive_threshold
        self.confidence_threshold = confidence_threshold

        # clases que nos interesan
        self.target_labels = {'Accident', 'NoAccident', 'moderate', 'severe'}

        # snapshot throttle
        self.snapshot_cooldown = timedelta(seconds=snapshot_cooldown)
        self.last_snapshot_time = None

    def convert_frame_to_pixmap(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        return QPixmap(QImage(rgb.data, w, h, ch * w, QImage.Format_RGB888))

    def choose_dataset_folder(self):
        r = random.random()
        if r < 0.7:
            return 'train'
        elif r < 0.9:
            return 'valid'
        else:
            return 'test'

    def save_snapshot(self, frame, boxes, confs, cls_idxs):
        """Guarda full-frame + .txt YOLO en train/valid/test solo para target_labels."""
        now = datetime.now()
        if self.last_snapshot_time and now - self.last_snapshot_time < self.snapshot_cooldown:
            return  # aún en cooldown

        h, w = frame.shape[:2]
        ts = now.strftime('%Y%m%d_%H%M%S')
        base = ts
        img_name = f"{base}.jpg"
        lbl_name = f"{base}.txt"

        subset = self.choose_dataset_folder()
        img_path = os.path.join(self.retrain_dir, subset, 'images', img_name)
        lbl_path = os.path.join(self.retrain_dir, subset, 'labels', lbl_name)

        # guardar imagen completa
        cv2.imwrite(img_path, frame)

        # guardar cada caja en formato YOLO
        with open(lbl_path, 'w') as f:
            for box, conf, cls in zip(boxes, confs, cls_idxs):
                cls_int = int(cls)
                name = self.model.names[cls_int]
                if conf < self.confidence_threshold or name not in self.target_labels:
                    continue
                x1, y1, x2, y2 = map(int, box)
                xc = (x1 + x2) / 2 / w
                yc = (y1 + y2) / 2 / h
                bw = (x2 - x1) / w
                bh = (y2 - y1) / h
                f.write(f"{cls_int} {xc:.6f} {yc:.6f} {bw:.6f} {bh:.6f}\n")

        self.last_snapshot_time = now
        print(f"[{subset.upper()}] Snapshot: {img_path}, {lbl_path}")

    def detect_from_video(self, video_path: str, user_output_dir: str = None):
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise RuntimeError("No se pudo abrir el video")

            fps    = int(cap.get(cv2.CAP_PROP_FPS))
            w      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

            video_dir = user_output_dir or self.output_dir
            os.makedirs(video_dir, exist_ok=True)

            writer = None
            recording = False
            count_severe = 0
            cooldown_frames = 0
            title_on = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                res = self.model(frame)[0]
                ann = frame.copy()

                has_target = False
                is_severe = False

                # dibujar todas las cajas y revisar clases
                for box, conf, cls in zip(res.boxes.xyxy, res.boxes.conf, res.boxes.cls):
                    name = self.model.names[int(cls)]
                    if conf >= self.confidence_threshold and name == 'severe':  # Solo "severe"
                     x1, y1, x2, y2 = map(int, box)
                     cv2.rectangle(ann, (x1, y1), (x2, y2), (0, 0, 255), 2)
                     cv2.putText(ann, f"{name} {conf:.2f}", (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                     is_severe = True  # Marcar que es un accidente severo
               
                if has_target:
                    self.save_snapshot(frame, res.boxes.xyxy, res.boxes.conf, res.boxes.cls)

                # lógica de vídeo para severe
                if is_severe:
                    count_severe += 1
                else:
                    count_severe = max(0, count_severe - 1)

                if count_severe >= self.consecutive_threshold and not recording:
                    recording = True
                    title_on = False
                    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
                    vid_path = os.path.join(video_dir, f"accidente_severe_{ts}.mp4")
                    writer = cv2.VideoWriter(vid_path, fourcc, fps, (w, h))
                    print("Grabando video (severe) en:", vid_path)
                    if self.callback:
                        self.callback(vid_path)

                if recording:
                    if not title_on:
                        cv2.putText(ann, "ACCIDENTE SEVERE", (50,50),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 5, cv2.LINE_AA)
                        title_on = True
                    writer.write(ann)
                    cooldown_frames += 1
                    if count_severe == 0 and cooldown_frames > fps * 2:
                        recording = False
                        cooldown_frames = 0
                        writer.release()
                        writer = None
                        print("Finalizada grabación severe.")

                if self.update_label_callback:
                    self.update_label_callback(self.convert_frame_to_pixmap(ann))

                cv2.imshow("Detección de Accidentes", ann)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()

        except Exception as e:
            print("Error al procesar el video:", e)
