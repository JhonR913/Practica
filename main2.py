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
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from PyQt5 import QtWidgets, QtWebEngineWidgets, uic
from PyQt5 import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap
import decimal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QModelIndex

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)



def connect_to_database():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )
    
    
# Callback para video pregrabado
def on_accident(path: str):
    print(f"¡ACCIDENTE DETECTADO EN VIDEO! Video guardado en: {path}")
    QMessageBox.information(None, "Accidente Detectado",
                            f"Un accidente ha sido detectado y guardado en:\n{path}")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showMaximized()
        self.load_registros()
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

        # Ruta final del vídeo anotado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(out_dir, f"video_analizado_{timestamp}.mp4")

        detector = AccidentDetector(
            save_clips=False,      # ya grabamos todo el vídeo
            output_dir=out_dir,
            callback=on_accident
        )

        if hasattr(self, 'video_thread') and self.video_thread.isRunning():
            self.video_thread.stop()

        self.video_thread = VideoDetectionThread(
            video_path,
            detector,
            output_file,
            min_detection_time=3.0
        )
        self.video_thread.frame_ready.connect(
            lambda qimg: self.vistaPreviaVideo.setPixmap(QPixmap.fromImage(qimg))
        )
        self.video_thread.detection_status.connect(
            lambda txt: self.deteccionEjemplo.setText(txt)
        )
        self.video_thread.start()


        
    def connect_to_database(self):
        return connect_to_database()

    def load_registros(self):
        """
        Carga todos los registros de la tabla `accidentes` en el QTableView `registrosTable`,
        arranca sin ninguna fila seleccionada, modo solo lectura, selección de fila completa,
        ajuste automático de columnas y coloreado alterno de filas.
        """
        try:
            conn = connect_to_database()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    id,
                    id_camara,
                    DATE_FORMAT(fecha_accidente, '%Y-%m-%d %H:%i:%s') AS fecha_accidente,
                    ruta_archivo,
                    latitud,
                    longitud,
                    descripcion,
                    DATE_FORMAT(creado_en, '%Y-%m-%d %H:%i:%s') AS creado_en
                FROM accidentes
                ORDER BY fecha_accidente DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
        except Error as e:
            print(f"Error al cargar registros: {e}")
            return

        headers = ["ID", "Cámara", "Fecha Accidente", "Ruta Archivo",
                   "Latitud", "Longitud", "Descripción", "Creado En"]

        # 1) Crear el modelo
        model = QStandardItemModel(len(rows), len(headers), self)
        model.setHorizontalHeaderLabels(headers)

        # 2) Rellenar el modelo
        for r, record in enumerate(rows):
            for c, key in enumerate([
                "id", "id_camara", "fecha_accidente", "ruta_archivo",
                "latitud", "longitud", "descripcion", "creado_en"
            ]):
                text = str(record[key] or "")
                item = QStandardItem(text)
                # Marcar SOLO como seleccionable y habilitado (no editable)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                model.setItem(r, c, item)

        # 3) Asignar modelo a la vista
        tv = self.registrosTable
        tv.setModel(model)

        # 4) Ajustes de selección y visuales
        tv.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tv.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tv.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tv.horizontalHeader().setStretchLastSection(True)
        tv.resizeColumnsToContents()

        # 5) Colores alternos para filas
        tv.setAlternatingRowColors(False)

        # 6) Arrancar sin ninguna fila resaltada
        tv.clearSelection()
        tv.setCurrentIndex(QModelIndex())

    def consultar_camara(self):
        """Devuelve un dict con id, ip, puerto, usuario, password, latitud y longitud."""
        try:
            conn = connect_to_database()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT id, ip, puerto, usuario, password, latitud, longitud
                FROM camaras
                ORDER BY id
                LIMIT 1
                """
            )
            resultado = cursor.fetchone()
            cursor.close()
            conn.close()
            return resultado
        except Error as e:
            print(f"Error al consultar la cámara: {e}")
            return None

    def cargar_camara_guardada(self):
        """Carga la cámara desde la BDD y prepara el label y URL RTSP."""
        datos = self.consultar_camara()
        if not datos:
            print("No hay cámara registrada en la base de datos.")
            return

        self.camera_data = datos
        ip = datos['ip']
        port = datos['puerto']
        user = datos['usuario']
        pwd = datos['password']
        self.last_rtsp_url = f"rtsp://{user}:{pwd}@{ip}:{port}/Streaming/Channels/101"
        print(f"Cargando cámara guardada: {self.last_rtsp_url}")

        # Configurar frame de video
        if not self.camara1Frame.layout():
            self.camara1Frame.setLayout(QtWidgets.QVBoxLayout())
        layout = self.camara1Frame.layout()
        for i in reversed(range(layout.count())):
            w = layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        self.video_label = QtWidgets.QLabel()
        self.video_label.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_label)

        # Iniciar o reconectar hilo RTSP
        thread = getattr(self, 'rtsp_thread', None)
        if thread and thread.isRunning():
            try:
                thread.change_pixmap.disconnect()
            except Exception:
                pass
            thread.change_pixmap.connect(
                lambda img: self._update_video_label(img, self.video_label)
            )
        else:
            self._start_rtsp_stream(self.last_rtsp_url, self.video_label)

        self.camara1Frame.mouseDoubleClickEvent = self._onCam1DoubleClick

    def registrar_accidente(self, ruta_archivo, descripcion=None):
        """
        Inserta un registro en la tabla `accidentes` usando
        los datos de la cámara actualmente cargada (self.camera_data).
        """
        if not self.camera_data:
            print("No hay cámara cargada para asociar el accidente.")
            return

        cam = self.camera_data
        sql = (
            "INSERT INTO accidentes "
            "(id_camara, ruta_archivo, latitud, longitud, descripcion) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        params = (
            cam['id'], ruta_archivo,
            cam['latitud'], cam['longitud'],
            descripcion or ""
        )
        try:
            conn = connect_to_database()
            cursor = conn.cursor()
            cursor.execute(sql, params)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"Accidente registrado en DB (cámara {cam['id']}).")
        except Error as e:
            print(f"Error al registrar accidente: {e}")

    def on_accident_camara(self, ruta_archivo: str):
        print(f"¡ACCIDENTE DETECTADO EN CÁMARA!: {ruta_archivo}")
        self.registrar_accidente(ruta_archivo, descripcion="Detectado por RTSP en vivo")
        self.load_registros()
        
    def start_camera_thread(self, rtsp_url):
        live_dir = os.path.join(os.getcwd(), "live_detections")
        ensure_output_folder_exists(live_dir)
        
        # Detener hilos existentes si los hay
        if hasattr(self, 'cam_thread1') and self.cam_thread1.isRunning():
            self.cam_thread1.stop()
        if hasattr(self, 'cam_thread2') and self.cam_thread2.isRunning():
            self.cam_thread2.stop()
            
        # Primer hilo para videoLabel
        cam_det1 = AccidentDetector(save_clips=True, output_dir=live_dir, callback=self.on_accident_camara)
        self.cam_thread1 = CameraDetectionThread(rtsp_url, cam_det1)
        self.cam_thread1.frame_ready.connect(self._update_view1)
        self.cam_thread1.detection_status.connect(self._update_status1)
        
        # Segundo hilo para videoLabel_2
        cam_det2 = AccidentDetector(save_clips=False, output_dir=live_dir)
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

class VideoDetectionThread(QtCore.QThread):
    frame_ready     = QtCore.pyqtSignal(QImage)
    detection_status = QtCore.pyqtSignal(str)

    def __init__(self, video_path, detector, output_path, min_detection_time=3.0):
        super().__init__()
        self.video_path          = video_path
        self.detector            = detector
        self.output_path         = output_path
        self.min_detection_time  = min_detection_time

        self.detection_start_time = None
        self.confirmed_detection  = False
        self.processing_interval  = 1/30
        self.last_processed_time  = 0

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            self.detection_status.emit("❌ No se pudo abrir el vídeo")
            return

        # Parámetros para VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps    = cap.get(cv2.CAP_PROP_FPS) or 30
        w      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        writer = cv2.VideoWriter(self.output_path, fourcc, fps, (w, h))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            now = time.time()
            if now - self.last_processed_time < self.processing_interval:
                continue
            self.last_processed_time = now

            results = self.detector.model(frame)[0]
            current_detection = any(conf >= self.detector.confidence_threshold
                                    for conf in results.boxes.conf)

            if current_detection:
                if self.detection_start_time is None:
                    self.detection_start_time = now
                elif now - self.detection_start_time >= self.min_detection_time:
                    self.confirmed_detection = True
            else:
                self.detection_start_time = None
                self.confirmed_detection  = False

            ann = frame.copy()
            if self.confirmed_detection:
                for box, conf in zip(results.boxes.xyxy, results.boxes.conf):
                    if conf >= self.detector.confidence_threshold:
                        x1, y1, x2, y2 = map(int, box)
                        cv2.rectangle(ann, (x1,y1), (x2,y2), (0,0,255), 2)
                        cv2.putText(ann, f"Accidente {conf:.2f}",
                                    (x1, y1-10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

            # Emitir frame para previsualizar
            h_img, w_img, _ = ann.shape
            qimg = QImage(ann.data, w_img, h_img, 3*w_img, QImage.Format_BGR888)
            self.frame_ready.emit(qimg)

            # Actualizar estado
            if self.confirmed_detection:
                self.detection_status.emit("🚨 ¡Accidente Detectado!")
            elif self.detection_start_time:
                elapsed = now - self.detection_start_time
                self.detection_status.emit(f"⚠️ Posible accidente... ({elapsed:.1f}s)")
            else:
                self.detection_status.emit("✅ Sin accidentes detectados")

            # Grabar el frame anotado
            writer.write(ann)

        cap.release()
        writer.release()
        self.detection_status.emit(f"✅ Vídeo guardado en:\n{self.output_path}")

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
        self.min_detection_time = 0.8  # 6 segundos para confirmar detección
        self.confirmed_detection = False
        
        # Variables para mantener recuadros fijos
        self.accident_boxes = []
        self.detection_display_time = 7.0  # Tiempo que se mostrará el recuadro fijo (10 segundos)
        self.last_detection_time = None
        
        # Control de procesamiento
        self.processing_frame = False
        self.last_processed_time = 0
        self.processing_interval = 0.4  # Procesar cada 2fps
        
        # Control para la estabilidad de frames
        self.frame_buffer = None
        
        # Control para evitar registros duplicados
        self.last_register_time = 0
        self.min_register_interval = 15.0  # Tiempo mínimo entre registros (30 segundos)

    def run(self):
        cap = cv2.VideoCapture()
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        
        # Intentos de conexión RTSP
        success = False
        try:
            cap.open(self.rtsp_url, cv2.CAP_FFMPEG)
            if cap.isOpened(): success = True
            else:
                cap.open(self.rtsp_url)
                success = cap.isOpened()
        except Exception as e:
            print(f"Error al abrir stream: {e}")
        if not success:
            print(f"ERROR: No se pudo abrir RTSP: {self.rtsp_url}")
            self.detection_status.emit("❌ Error de conexión")
            return
        
        frame_skip_counter = 0
        frame_skip_value = 1
        
        while self._running:
            try:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.1)
                    continue
                frame_skip_counter += 1
                if frame_skip_counter % frame_skip_value != 0:
                    continue

                # Actualizar buffer
                self.frame_buffer = frame.copy() if self.frame_buffer is not None else frame.copy()
                current_time = time.time()
                ann = frame.copy()
                should_process = (current_time - self.last_processed_time) >= self.processing_interval

                # Detección principal
                if not self.confirmed_detection and should_process and not self.processing_frame:
                    self.processing_frame = True
                    self.last_processed_time = current_time
                    try:
                        results = self.detector.model(frame)[0]
                        current_detection = False
                        detected_boxes = []
                        for box, conf, cls in zip(results.boxes.xyxy, results.boxes.conf, results.boxes.cls):
                            if conf >= self.detector.confidence_threshold:
                                current_detection = True
                                x1, y1, x2, y2 = map(int, box)
                                detected_boxes.append((x1, y1, x2, y2, conf))
                        if current_detection:
                            if self.detection_start_time is None:
                                self.detection_start_time = current_time
                            elif current_time - self.detection_start_time >= self.min_detection_time:
                                print(f"¡ACCIDENTE CONFIRMADO! Después de {self.min_detection_time} segundos")
                                self.accident_boxes = detected_boxes
                                self.confirmed_detection = True
                                self.last_detection_time = current_time
                                
                                # Verificar si ha pasado suficiente tiempo desde el último registro
                                tiempo_desde_ultimo_registro = current_time - self.last_register_time
                                if tiempo_desde_ultimo_registro >= self.min_register_interval and hasattr(self.detector, 'callback'):
                                    try:
                                        live_dir = self.detector.output_dir
                                        os.makedirs(live_dir, exist_ok=True)
                                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                        snapshot_path = os.path.join(live_dir, f"accidente_{timestamp}.jpg")
                                        cv2.imwrite(snapshot_path, frame)
                                        self.detector.callback(snapshot_path)
                                        self.last_register_time = current_time  # Actualizar tiempo del último registro
                                        print(f"Accidente registrado en la BD a las {timestamp}")
                                    except Exception as e:
                                        print(f"Error al invocar callback manual de accidente: {e}")
                                else:
                                    tiempo_restante = self.min_register_interval - tiempo_desde_ultimo_registro
                                    if tiempo_restante > 0:
                                        print(f"Esperando {tiempo_restante:.1f} segundos para registrar otro accidente")
                        else:
                            self.detection_start_time = None
                    except Exception as e:
                        print(f"Error en procesamiento: {e}")
                    finally:
                        self.processing_frame = False

                # Dibujar recuadros fijos
                if self.confirmed_detection:
                    if current_time - self.last_detection_time >= self.detection_display_time:
                        self.confirmed_detection = False
                        self.accident_boxes = []
                    else:
                        for x1, y1, x2, y2, conf in self.accident_boxes:
                            cv2.rectangle(ann, (x1, y1), (x2, y2), (0,0,255), 3)
                            label = f"Accidente {conf:.2f}"
                            text_sz = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                            cv2.rectangle(ann, (x1, y1-20), (x1+text_sz[0], y1), (0,0,255), -1)
                            cv2.putText(ann, label, (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

                # Estado
                if self.confirmed_detection:
                    remaining = self.detection_display_time - (current_time - self.last_detection_time)
                    tiempo_desde_ultimo_registro = current_time - self.last_register_time
                    
                    if tiempo_desde_ultimo_registro < self.min_register_interval:
                        tiempo_espera = self.min_register_interval - tiempo_desde_ultimo_registro
                        self.detection_status.emit(f"🚨 ¡ACCIDENTE DETECTADO! ({remaining:.1f}s) [Próximo registro en {tiempo_espera:.1f}s]")
                    else:
                        self.detection_status.emit(f"🚨 ¡ACCIDENTE DETECTADO! ({remaining:.1f}s) [Listo para registrar]")
                elif self.detection_start_time is not None:
                    elapsed = current_time - self.detection_start_time
                    pct = int((elapsed/self.min_detection_time)*100)
                    bar = "▓"* (pct//10) + "░"*(10-pct//10)
                    self.detection_status.emit(f"⚠️ Posible accidente [{bar}] {elapsed:.1f}/{self.min_detection_time:.1f}s")
                else:
                    self.detection_status.emit("✅ Monitoreo normal")

                # Emitir frame
                h, w, _ = ann.shape
                qimg = QImage(ann.data, w, h, 3*w, QImage.Format_BGR888).copy()
                self.frame_ready.emit(qimg)

            except Exception as e:
                print(f"Error en bucle principal: {e}")
                if self.frame_buffer is not None:
                    try:
                        h, w, _ = self.frame_buffer.shape
                        qimg = QImage(self.frame_buffer.data, w, h, 3*w, QImage.Format_BGR888).copy()
                        self.frame_ready.emit(qimg)
                    except:
                        pass
                time.sleep(0.1)
        cap.release()

    def stop(self):
        self._running = False
        self.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
    
    #dele de aqui para atras