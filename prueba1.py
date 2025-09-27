import sys
import os
import time
import cv2
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QMutex
from gui.interfaz import Ui_MainWindow
from traffic_accident_detector.detector import AccidentDetector
from traffic_accident_detector.utils.file_system import ensure_output_folder_exists

# Callback para video pregrabado
def on_accident(path: str):
    print(f"¡ACCIDENTE DETECTADO EN VIDEO! Video guardado en: {path}")
    QMessageBox.information(None, "Accidente Detectado",
                            f"Un accidente ha sido detectado y guardado en:\n{path}")

# Callback para cámara en vivo
def on_accident_camara(path: str):
    print(f"¡ACCIDENTE DETECTADO EN CÁMARA EN VIVO!: {path}")

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()

        # Variables para control de actualización
        self._last_update1 = 0.0
        self._last_update2 = 0.0
        self._update_interval = 0.033  # ~30fps
        
        # Mutexes para sincronización de actualización de frames
        self._view1_mutex = QMutex()
        self._view2_mutex = QMutex()

        # Botones video pregrabado
        self.seleccionarVideoBtn.clicked.connect(self.select_video)
        self.subirVideoBtn.clicked.connect(self.process_video)

        # Variables para almacenar las dimensiones originales de los labels
        self.video_label_size = None
        self.video_label_2_size = None
        
        # Configuración específica para video_label_2 para evitar redimensionamiento
        if hasattr(self, 'video_label_2'):
            # Forzar que el contenido se ajuste al tamaño del label exactamente
            self.video_label_2.setScaledContents(True)
            # Desactivar SizePolicy para evitar que QT controle el redimensionamiento
            self.video_label_2.setSizePolicy(QtCore.QSizePolicy.Fixed, QtCore.QSizePolicy.Fixed)
        
        # Inicializar interfaz con cámaras
        self.cargar_camara_guardada()
        
        # Colocar tamaños correctos solo después de que todo sea visible
        QtCore.QTimer.singleShot(500, self.initialize_video_sizes)
        
        # Arrancar detección para ambas vistas
        self.start_camera_thread(self.last_rtsp_url)

    def initialize_video_sizes(self):
        """Guarda los tamaños iniciales de los labels de video"""
        if hasattr(self, 'video_label'):
            self.video_label_size = self.video_label.size()
        if hasattr(self, 'video_label_2'):
            self.video_label_2_size = self.video_label_2.size()
        print(f"Tamaños inicializados: Label1={self.video_label_size}, Label2={self.video_label_2_size}")

    def select_video(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Video", "", "Archivos de Video (*.mp4 *.avi)"
        )
        self.archivoSeleccionadoLabel.setText(path or "")

    def process_video(self):
        video_path = self.archivoSeleccionadoLabel.text().strip()
        if not video_path:
            QMessageBox.warning(self, "Error", "Por favor selecciona un video primero.")
            return

        out_dir = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta de Salida")
        if not out_dir:
            QMessageBox.warning(self, "Error", "Por favor selecciona carpeta de salida.")
            return

        ensure_output_folder_exists(out_dir)
        detector = AccidentDetector(save_clips=True, output_dir=out_dir, callback=on_accident)
        cap = cv2.VideoCapture(video_path)
        
        # Para mantener registro del tiempo de detección continua
        detection_start_time = None
        min_detection_time = 3.0  # Tiempo mínimo en segundos para confirmar detección
        confirmed_detection = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            results = detector.model(frame)[0]
            ann = frame.copy()
            
            # Comprobar si hay detección en este frame
            current_detection = False
            for conf in results.boxes.conf:
                if conf >= detector.confidence_threshold:
                    current_detection = True
                    break
                    
            current_time = time.time()
            
            # Actualizar lógica de detección sostenida
            if current_detection:
                if detection_start_time is None:
                    detection_start_time = current_time
                elif current_time - detection_start_time >= min_detection_time:
                    confirmed_detection = True
            else:
                detection_start_time = None
                confirmed_detection = False
            
            # Dibujar recuadros SOLO si la detección está confirmada
            if confirmed_detection:
                for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
                    if conf >= detector.confidence_threshold:
                        x1, y1, x2, y2 = map(int, box)
                        cv2.rectangle(ann, (x1, y1), (x2, y2), (0, 0, 255), 2)
                        cv2.putText(ann, f"Accidente {conf:.2f}",
                                (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            # Actualizar estado en la interfaz
            h, w, _ = ann.shape
            qimg = QImage(ann.data, w, h, 3*w, QImage.Format_BGR888)
            self.vistaPreviaVideo.setPixmap(QPixmap.fromImage(qimg))
            
            # Actualizar texto de estado
            if confirmed_detection:
                self.deteccionEjemplo.setText("🚨 ¡Accidente Detectado!")
            elif current_detection:
                self.deteccionEjemplo.setText(f"⚠️ Posible accidente... ({current_time - detection_start_time:.1f}s)")
            else:
                self.deteccionEjemplo.setText("✅ Sin accidentes detectados")
                
            QtCore.QCoreApplication.processEvents()
        cap.release()

    def start_camera_thread(self, rtsp_url):
        live_dir = os.path.join(os.getcwd(), "live_detections")
        ensure_output_folder_exists(live_dir)
        
        # Detener hilos existentes si los hay
        if hasattr(self, 'cam_thread1') and self.cam_thread1.isRunning():
            self.cam_thread1.stop()
        if hasattr(self, 'cam_thread2') and self.cam_thread2.isRunning():
            self.cam_thread2.stop()
            
        # Primer hilo para videoLabel
        cam_det1 = AccidentDetector(save_clips=False, output_dir=live_dir, callback=on_accident_camara)
        self.cam_thread1 = CameraDetectionThread(rtsp_url, cam_det1)
        self.cam_thread1.frame_ready.connect(self._update_view1)
        self.cam_thread1.detection_status.connect(self._update_status1)
        
        # Segundo hilo para videoLabel_2
        cam_det2 = AccidentDetector(save_clips=False, output_dir=live_dir, callback=on_accident_camara)
        self.cam_thread2 = CameraDetectionThread(rtsp_url, cam_det2)
        self.cam_thread2.frame_ready.connect(self._update_view2)
        self.cam_thread2.detection_status.connect(self._update_status2)

        self.cam_thread1.start()
        self.cam_thread2.start()

    def _scale_pixmap_fixed(self, qimg, label):
        """Escala el pixmap manteniendo proporciones fijas y consistentes"""
        if not label:
            return None
            
        # Obtener el nombre del label para tratamiento especial
        label_name = label.objectName()
        
        # Para video_label_2, usar un enfoque diferente para garantizar tamaño exacto
        if label_name == "video_label_2":
            # Forzar que el pixmap ocupe exactamente el tamaño del label
            # sin preservar proporciones para video_label_2
            target_size = label.size()
            pix = QPixmap.fromImage(qimg)
            return pix.scaled(
                target_size.width(), 
                target_size.height(),
                Qt.IgnoreAspectRatio,  # Forzar tamaño exacto
                Qt.SmoothTransformation
            )
        # Para video_label, mantener el enfoque original con proporción
        else:
            # Usar el tamaño inicial guardado o el actual si no hay guardado
            if label_name == "video_label" and self.video_label_size:
                target_size = self.video_label_size
            else:
                target_size = label.size()
                
            # Crear el pixmap y escalarlo manteniendo proporción
            pix = QPixmap.fromImage(qimg)
            return pix.scaled(
                target_size, 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )

    def _update_view1(self, qimg: QImage):
        if not hasattr(self, 'video_label'):
            return
            
        self._view1_mutex.lock()
        try:
            now = time.time()
            if now - self._last_update1 < self._update_interval:
                return
            self._last_update1 = now
            
            # Procesar y actualizar el pixmap
            scaled_pix = self._scale_pixmap_fixed(qimg, self.video_label)
            if scaled_pix:
                self.video_label.clear()
                self.video_label.setPixmap(scaled_pix)
        finally:
            self._view1_mutex.unlock()
            
    def _update_status1(self, status: str):
        # Si existe statusLabel1, actualízala, de lo contrario usa una etiqueta alternativa
        if hasattr(self, 'statusLabel1'):
            self.statusLabel1.setText(status)
        elif hasattr(self, 'deteccionEjemplo'):
            # Usar la etiqueta de detección de ejemplo como alternativa
            self.deteccionEjemplo.setText(f"Cámara 1: {status}")

    def _update_view2(self, qimg: QImage):
        if not hasattr(self, 'video_label_2'):
            return
            
        self._view2_mutex.lock()
        try:
            now = time.time()
            if now - self._last_update2 < self._update_interval:
                return
            self._last_update2 = now
            
            # Procesar y actualizar el pixmap con tamaño fijo
            scaled_pix = self._scale_pixmap_fixed(qimg, self.video_label_2)
            if scaled_pix:
                self.video_label_2.clear()
                self.video_label_2.setPixmap(scaled_pix)
                
                # Asegurar que el pixmap ocupe todo el label exactamente
                self.video_label_2.setScaledContents(True)
        finally:
            self._view2_mutex.unlock()
            
    def _update_status2(self, status: str):
        # Si existe statusLabel2, actualízala, de lo contrario usa una etiqueta alternativa
        if hasattr(self, 'statusLabel2'):
            self.statusLabel2.setText(status)
        elif hasattr(self, 'deteccionEjemplo'):
            # Actualizar también la etiqueta de detección de ejemplo
            current_text = self.deteccionEjemplo.text()
            if "Cámara 1:" in current_text:
                self.deteccionEjemplo.setText(f"{current_text} | Cámara 2: {status}")
            else:
                self.deteccionEjemplo.setText(f"Cámara 2: {status}")

    def closeEvent(self, event):
        if hasattr(self, 'cam_thread1'):
            self.cam_thread1.stop()
        if hasattr(self, 'cam_thread2'):
            self.cam_thread2.stop()
        event.accept()

    def resizeEvent(self, event):
        # Al redimensionar la ventana, no actualizar los tamaños guardados
        # para evitar cambios de proporciones durante el escalado
        super().resizeEvent(event)


class CameraDetectionThread(QtCore.QThread):
    frame_ready = QtCore.pyqtSignal(QImage)
    detection_status = QtCore.pyqtSignal(str)

    def __init__(self, rtsp_url, detector):
        super().__init__()
        self.rtsp_url = rtsp_url
        self.detector = detector
        self._running = True
        
        # Variables para la detección basada en tiempo
        self.detection_start_time = None
        self.min_detection_time = 5.0  # 5 segundos para confirmar detección
        self.confirmed_detection = False
        
        # Variables para mantener recuadros fijos
        self.accident_boxes = []
        self.detection_display_time = 10.0  # Tiempo que se mostrará el recuadro fijo (10 segundos)
        self.last_detection_time = None
        
        # Control de procesamiento
        self.processing_frame = False
        self.last_processed_time = 0
        self.processing_interval = 0.5  # Procesar cada 0.5 segundos (2 fps para análisis)
        
        # Control para la estabilidad de frames
        self.frame_buffer = None

    def run(self):
        cap = cv2.VideoCapture()
        # Configurar el protocolo de transporte preferido para RTSP
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)  # Un buffer mayor puede mejorar estabilidad
        
        # Intentar abrir con diferentes configuraciones si fallan las primeras
        success = False
        try:
            # Primer intento con FFMPEG
            cap.open(self.rtsp_url, cv2.CAP_FFMPEG)
            if cap.isOpened():
                success = True
                print(f"Conexión exitosa usando FFMPEG a {self.rtsp_url}")
            else:
                # Segundo intento, sin especificar API backend
                cap.open(self.rtsp_url)
                if cap.isOpened():
                    success = True 
                    print(f"Conexión exitosa usando backend predeterminado a {self.rtsp_url}")
        except Exception as e:
            print(f"Error al abrir stream: {e}")
            
        if not success:
            print(f"ERROR: No se pudo abrir RTSP: {self.rtsp_url}")
            self.detection_status.emit("❌ Error de conexión")
            return
        
        # Limitamos la búsqueda de frames
        frame_skip_counter = 0
        frame_skip_value = 1  # Procesar cada N frames para mejorar rendimiento si es necesario
        
        while self._running:
            try:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.1)  # Espera un poco más larga si no hay frame
                    continue
                    
                # Saltar frames si es necesario
                frame_skip_counter += 1
                if frame_skip_counter % frame_skip_value != 0:
                    continue
                
                # Mantener un frame de respaldo para cuando fallen las lecturas
                if self.frame_buffer is None:
                    self.frame_buffer = frame.copy()
                else:
                    # Actualizar el buffer solo cada cierto tiempo para mantener estabilidad
                    self.frame_buffer = frame.copy()

                current_time = time.time()
                ann = frame.copy()  # Siempre trabajamos con una copia limpia del frame actual
                
                # Determinar si es momento de procesar este frame para detección
                should_process = (current_time - self.last_processed_time) >= self.processing_interval
                
                # Verificar si hay que buscar accidentes
                if not self.confirmed_detection and should_process and not self.processing_frame:
                    self.processing_frame = True  # Marcar que estamos procesando
                    self.last_processed_time = current_time
                    
                    try:
                        # Detección en un thread separado o proceso
                        results = self.detector.model(frame)[0]
                        
                        # Comprobar si hay detección en este frame
                        current_detection = False
                        highest_conf = 0.0
                        detected_boxes = []
                        
                        for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
                            if conf >= self.detector.confidence_threshold:
                                current_detection = True
                                highest_conf = max(highest_conf, conf)
                                x1, y1, x2, y2 = map(int, box)
                                detected_boxes.append((x1, y1, x2, y2, conf))
                        
                        # Actualizar lógica de detección sostenida
                        if current_detection:
                            if self.detection_start_time is None:
                                # Primer frame con detección
                                self.detection_start_time = current_time
                                print(f"Posible accidente detectado (confianza: {highest_conf:.2f})")
                            elif current_time - self.detection_start_time >= self.min_detection_time:
                                # Detección confirmada después del tiempo mínimo
                                if not self.confirmed_detection:
                                    print(f"¡ACCIDENTE CONFIRMADO! Después de {self.min_detection_time} segundos")
                                    # Guardar las cajas de detección
                                    self.accident_boxes = detected_boxes
                                    self.confirmed_detection = True
                                    self.last_detection_time = current_time
                        else:
                            # Sin detección, reiniciar cronómetro
                            if self.detection_start_time is not None:
                                print("Posible accidente descartado.")
                            self.detection_start_time = None
                    except Exception as e:
                        print(f"Error en procesamiento: {e}")
                    
                    self.processing_frame = False  # Marcar que terminamos de procesar
                
                # Dibujar recuadros si hay detección confirmada
                if self.confirmed_detection:
                    # Verificar si el tiempo de mostrar la detección ha expirado
                    if current_time - self.last_detection_time >= self.detection_display_time:
                        print("Tiempo de mostrar accidente expirado, volviendo a monitoreo normal")
                        self.confirmed_detection = False
                        self.accident_boxes = []
                    else:
                        # Dibujar los recuadros fijos en el frame actual
                        for x1, y1, x2, y2, conf in self.accident_boxes:
                            # Dibujar rectángulo
                            cv2.rectangle(ann, (x1, y1), (x2, y2), (0, 0, 255), 3)
                            
                            # Texto con nivel de confianza
                            label = f"Accidente {conf:.2f}"
                            
                            # Fondo para el texto
                            text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                            cv2.rectangle(ann, (x1, y1 - 20), (x1 + text_size[0], y1), (0, 0, 255), -1)
                            
                            # Texto
                            cv2.putText(ann, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Actualizar texto de estado
                if self.confirmed_detection:
                    # Mostrar tiempo restante en la alerta
                    remaining = self.detection_display_time - (current_time - self.last_detection_time)
                    self.detection_status.emit(f"🚨 ¡ACCIDENTE DETECTADO! ({remaining:.1f}s)")
                elif self.detection_start_time is not None:
                    # Estado en progreso con barra de progreso
                    elapsed = current_time - self.detection_start_time
                    progress = (elapsed / self.min_detection_time) * 100
                    progress_bar = "▓" * int(progress/10) + "░" * (10 - int(progress/10))
                    self.detection_status.emit(f"⚠️ Posible accidente [{progress_bar}] {elapsed:.1f}/{self.min_detection_time:.1f}s")
                else:
                    # Sin detección
                    self.detection_status.emit("✅ Monitoreo normal")

                # Emitir frame - siempre enviamos el frame más nuevo
                h, w, _ = ann.shape
                qimg = QImage(ann.data, w, h, 3*w, QImage.Format_BGR888).copy()  # .copy() para evitar problemas
                self.frame_ready.emit(qimg)
                
            except Exception as e:
                print(f"Error en bucle principal: {e}")
                # Si hay error y tenemos buffer, usarlo temporalmente
                if self.frame_buffer is not None:
                    try:
                        h, w, _ = self.frame_buffer.shape
                        qimg = QImage(self.frame_buffer.data, w, h, 3*w, QImage.Format_BGR888).copy()
                        self.frame_ready.emit(qimg)
                    except:
                        raise
                time.sleep(0.1)  # Prevenir bucle cerrado de errores
            
        cap.release()
        
    def stop(self):
        self._running = False
        self.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())