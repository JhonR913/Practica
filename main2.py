import sys
import os
import cv2
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from gui.interfaz import Ui_MainWindow
from traffic_accident_detector.detector import AccidentDetector
from traffic_accident_detector.utils.file_system import ensure_output_folder_exists

# Función que se ejecuta cuando se detecta un accidente
def on_accident(path: str):
    print(f"¡ACCIDENTE DETECTADO! Video guardado en: {path}")
    QMessageBox.information(None, "Accidente Detectado", f"Un accidente ha sido detectado y guardado en:\n{path}")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Mostrar en pantalla completa
        self.showMaximized()

        # Conectar botones
        self.seleccionarVideoBtn.clicked.connect(self.select_video)
        self.subirVideoBtn.clicked.connect(self.process_video)

    def select_video(self):
        video_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Video", "", "Archivos de Video (*.mp4 *.avi)")
        if video_path:
            self.archivoSeleccionadoLabel.setText(f"Archivo seleccionado: {video_path}")
        else:
            self.archivoSeleccionadoLabel.setText("Ningún archivo seleccionado")

    def process_video(self):
        video_path = self.archivoSeleccionadoLabel.text().split(":")[-1].strip()
        if not video_path or video_path == "Ningún archivo seleccionado":
            QMessageBox.warning(self, "Error", "Por favor selecciona un archivo de video primero.")
            return

        output_folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Salida")
        if not output_folder:
            QMessageBox.warning(self, "Error", "No se seleccionó carpeta de salida.")
            return

        ensure_output_folder_exists(output_folder)

        try:
            detector = AccidentDetector(
                save_clips=True,
                output_dir=output_folder,
                callback=on_accident
            )
            print(f"Procesando video: {video_path}")

            cap = cv2.VideoCapture(video_path)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                results = detector.model(frame)[0]
                annotated_frame = frame.copy()
                deteccion_en_frame = False

                for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
                    class_name = str(detector.model.names[int(cls)])
                    if conf >= detector.confidence_threshold and class_name in detector.target_labels:
                        x1, y1, x2, y2 = map(int, box)
                        label = f"Accidente {conf:.2f}"
                        color = (0, 0, 255)
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(annotated_frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                        deteccion_en_frame = True

                # Convertir y mostrar en QLabel
                height, width, channel = annotated_frame.shape
                bytes_per_line = 3 * width
                q_img = QImage(annotated_frame.data, width, height, bytes_per_line, QImage.Format_BGR888)
                self.vistaPreviaVideo.setPixmap(QPixmap.fromImage(q_img))

                # Actualizar mensaje de detección
                if deteccion_en_frame:
                    self.deteccionEjemplo.setText("🚨 ¡Accidente Detectado!")
                else:
                    self.deteccionEjemplo.setText("✅ Sin accidentes detectados")

                cv2.waitKey(1)

            cap.release()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error al procesar el video: {str(e)}")

# Iniciar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()  # Ya se usa showMaximized en el constructor
sys.exit(app.exec_())
