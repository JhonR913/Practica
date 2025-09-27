import time
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import traceback
import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets, uic
from PyQt5 import QtWidgets, QtCore, QtMultimedia, QtMultimediaWidgets
import cv2
from PyQt5.QtGui import QImage, QPixmap
import decimal
from PyQt5 import QtCore, QtGui, QtWidgets

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
    
def guardar_camara(ip, puerto, usuario, password, latitud, longitud, url_rtsp):
    import decimal
    import mysql.connector
    import os

    try:
        lat_decimal = decimal.Decimal(str(latitud))
        lon_decimal = decimal.Decimal(str(longitud))
    except decimal.InvalidOperation as e:
        print(f"Error al convertir coordenadas a decimal: {e}")
        return

    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            sql = """
                INSERT INTO camaras (ip, puerto, usuario, password, latitud, longitud, url_rtsp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            valores = (ip, puerto, usuario, password, lat_decimal, lon_decimal, url_rtsp)
            cursor.execute(sql, valores)
            conexion.commit()
            cursor.close()
    except Exception as ex:
        print(f"Error inesperado durante conexión o inserción: {ex}")
    finally:
        if conexion and conexion.is_connected():
            conexion.close()

class StreamThread(QtCore.QThread):
    change_pixmap = QtCore.pyqtSignal(QtGui.QImage)
    connection_failed = QtCore.pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.running = True
        self.skip_frames = 2
        self.frame_count = 0
        self.last_frame_time = time.time()
        self.fps_limit = 30

    def run(self):
        print(f"StreamThread intentando abrir RTSP: {self.url}")
        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp|analyzeduration;0|fflags;nobuffer|max_delay;500000"

        if not cap.isOpened():
            print("No se pudo abrir el stream RTSP")
            self.connection_failed.emit(
                "No se pudo abrir el stream RTSP.\nRevisa la IP, puerto o credenciales."
            )
            return

        received_frames = 0
        while self.running:
            ret, frame = cap.read()
            if ret:
                self.frame_count += 1
                received_frames += 1
                current_time = time.time()
                elapsed = current_time - self.last_frame_time
                if elapsed < (1.0 / self.fps_limit):
                    continue
                if self.frame_count % (self.skip_frames + 1) != 0:
                    continue
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                if w > 1280:
                    scale = 1280 / w
                    new_width = int(w * scale)
                    new_height = int(h * scale)
                    rgb_image = cv2.resize(rgb_image, (new_width, new_height), interpolation=cv2.INTER_AREA)
                    h, w = new_height, new_width
                    bytes_per_line = ch * w
                qt_image = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
                self.change_pixmap.emit(qt_image)
                self.last_frame_time = current_time
            else:
                QtCore.QThread.msleep(50)
                if received_frames == 0:
                    print("Stream abierto pero sin frames recibidos")
                    self.connection_failed.emit("Se abrió el stream, pero no se reciben frames.")
                    break
        cap.release()
        print("StreamThread terminó")

    def stop(self):
        print("Deteniendo StreamThread")
        self.running = False
        self.quit()
        self.wait()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.rtsp_thread = None
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 664)
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #2D2D30;\n"
"    color: #E0E0E0;\n"
"}\n"
"\n"
"QWidget {\n"
"    background-color: #2D2D30;\n"
"    color: #E0E0E0;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #3E3E42;\n"
"    color: #E0E0E0;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 4px;\n"
"    padding: 5px 10px;\n"
"    min-height: 25px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #505054;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #2A2A2A;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #E0E0E0;\n"
"}\n"
"\n"
"QTableView {\n"
"    background-color: #252526;\n"
"    color: #E0E0E0;\n"
"    gridline-color: #333333;\n"
"    selection-background-color: #3E3E42;\n"
"    selection-color: #FFFFFF;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #3E3E42;\n"
"    color: #E0E0E0;\n"
"    padding: 4px;\n"
"    border: 1px solid #444444;\n"
"}\n"
"\n"
"QLineEdit, QTextEdit, QComboBox {\n"
"    background-color: #3E3E42;\n"
"    color: #E0E0E0;\n"
"    border: 1px solid #555555;\n"
"    border-radius: 2px;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QStackedWidget {\n"
"    background-color: #2D2D30;\n"
"}\n"
"\n"
"#navegacionFrame {\n"
"    background-color: #252526;\n"
"    border-top: 1px solid #444444;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.camarasPage = QtWidgets.QWidget()
        self.camarasPage.setObjectName("camarasPage")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.camarasPage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.camarasTitulo = QtWidgets.QLabel(self.camarasPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.camarasTitulo.setFont(font)
        self.camarasTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.camarasTitulo.setObjectName("camarasTitulo")
        self.verticalLayout_2.addWidget(self.camarasTitulo)
        self.camarasGrid = QtWidgets.QFrame(self.camarasPage)
        self.camarasGrid.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camarasGrid.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camarasGrid.setObjectName("camarasGrid")
        self.gridLayout = QtWidgets.QGridLayout(self.camarasGrid)
        self.gridLayout.setObjectName("gridLayout")
        self.camara1Frame = QtWidgets.QFrame(self.camarasGrid)
        self.camara1Frame.setMinimumSize(QtCore.QSize(0, 150))
        self.camara1Frame.setStyleSheet("background-color: #222224; border: 1px solid #444444;")
        self.camara1Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camara1Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camara1Frame.setObjectName("camara1Frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.camara1Frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.agregarCamara1 = QtWidgets.QPushButton(self.camara1Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.agregarCamara1.sizePolicy().hasHeightForWidth())
        self.agregarCamara1.setSizePolicy(sizePolicy)
        self.agregarCamara1.setObjectName("agregarCamara1")
        self.verticalLayout_6.addWidget(self.agregarCamara1)
        self.gridLayout.addWidget(self.camara1Frame, 0, 0, 1, 1)
        self.camara2Frame = QtWidgets.QFrame(self.camarasGrid)
        self.camara2Frame.setMinimumSize(QtCore.QSize(0, 150))
        self.camara2Frame.setStyleSheet("background-color: #222224; border: 1px solid #444444;")
        self.camara2Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camara2Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camara2Frame.setObjectName("camara2Frame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.camara2Frame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.agregarCamara2 = QtWidgets.QPushButton(self.camara2Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.agregarCamara2.sizePolicy().hasHeightForWidth())
        self.agregarCamara2.setSizePolicy(sizePolicy)
        self.agregarCamara2.setObjectName("agregarCamara2")
        self.verticalLayout_7.addWidget(self.agregarCamara2)
        self.gridLayout.addWidget(self.camara2Frame, 0, 1, 1, 1)
        self.camara3Frame = QtWidgets.QFrame(self.camarasGrid)
        self.camara3Frame.setMinimumSize(QtCore.QSize(0, 150))
        self.camara3Frame.setStyleSheet("background-color: #222224; border: 1px solid #444444;")
        self.camara3Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camara3Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camara3Frame.setObjectName("camara3Frame")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.camara3Frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.agregarCamara3 = QtWidgets.QPushButton(self.camara3Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.agregarCamara3.sizePolicy().hasHeightForWidth())
        self.agregarCamara3.setSizePolicy(sizePolicy)
        self.agregarCamara3.setObjectName("agregarCamara3")
        self.verticalLayout_8.addWidget(self.agregarCamara3)
        self.gridLayout.addWidget(self.camara3Frame, 1, 0, 1, 1)
        self.camara4Frame = QtWidgets.QFrame(self.camarasGrid)
        self.camara4Frame.setMinimumSize(QtCore.QSize(0, 150))
        self.camara4Frame.setStyleSheet("background-color: #222224; border: 1px solid #444444;")
        self.camara4Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.camara4Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.camara4Frame.setObjectName("camara4Frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.camara4Frame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.agregarCamara4 = QtWidgets.QPushButton(self.camara4Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.agregarCamara4.sizePolicy().hasHeightForWidth())
        self.agregarCamara4.setSizePolicy(sizePolicy)
        self.agregarCamara4.setObjectName("agregarCamara4")
        self.verticalLayout_9.addWidget(self.agregarCamara4)
        self.gridLayout.addWidget(self.camara4Frame, 1, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.camarasGrid)
        self.stackedWidget.addWidget(self.camarasPage)
        self.agregarCamaraPage = QtWidgets.QWidget()
        self.agregarCamaraPage.setObjectName("agregarCamaraPage")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.agregarCamaraPage)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.agregarCamaraTitulo = QtWidgets.QLabel(self.agregarCamaraPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.agregarCamaraTitulo.setFont(font)
        self.agregarCamaraTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.agregarCamaraTitulo.setObjectName("agregarCamaraTitulo")
        self.verticalLayout_15.addWidget(self.agregarCamaraTitulo)
        self.scrollArea_2 = QtWidgets.QScrollArea(self.agregarCamaraPage)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 754, 457))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.configuracionRTSP_2 = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.configuracionRTSP_2.setObjectName("configuracionRTSP_2")
        self.formLayout_7 = QtWidgets.QFormLayout(self.configuracionRTSP_2)
        self.formLayout_7.setObjectName("formLayout_7")
        self.direccionIpLabel = QtWidgets.QLabel(self.configuracionRTSP_2)
        self.direccionIpLabel.setObjectName("direccionIpLabel")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.direccionIpLabel)
        self.direccionIpEdit = QtWidgets.QLineEdit(self.configuracionRTSP_2)
        self.direccionIpEdit.setObjectName("direccionIpEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.direccionIpEdit)
        self.rtspPuertoLabel_2 = QtWidgets.QLabel(self.configuracionRTSP_2)
        self.rtspPuertoLabel_2.setObjectName("rtspPuertoLabel_2")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.rtspPuertoLabel_2)
        self.rtspPuertoEdit_2 = QtWidgets.QLineEdit(self.configuracionRTSP_2)
        self.rtspPuertoEdit_2.setObjectName("rtspPuertoEdit_2")
        self.formLayout_7.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.rtspPuertoEdit_2)
        self.usuarioPredeterminadoLabel_2 = QtWidgets.QLabel(self.configuracionRTSP_2)
        self.usuarioPredeterminadoLabel_2.setObjectName("usuarioPredeterminadoLabel_2")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.usuarioPredeterminadoLabel_2)
        self.usuarioEdit = QtWidgets.QLineEdit(self.configuracionRTSP_2)
        self.usuarioEdit.setObjectName("usuarioEdit")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.usuarioEdit)
        self.passwordPredeterminadoLabel_2 = QtWidgets.QLabel(self.configuracionRTSP_2)
        self.passwordPredeterminadoLabel_2.setObjectName("passwordPredeterminadoLabel_2")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.passwordPredeterminadoLabel_2)
        self.passwordEdit = QtWidgets.QLineEdit(self.configuracionRTSP_2)
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.formLayout_7.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.passwordEdit)
        self.verticalLayout_13.addWidget(self.configuracionRTSP_2)
        self.ubicacionCamaraGeneral = QtWidgets.QGroupBox(self.scrollAreaWidgetContents_2)
        self.ubicacionCamaraGeneral.setObjectName("ubicacionCamaraGeneral")
        self.formLayout_5 = QtWidgets.QFormLayout(self.ubicacionCamaraGeneral)
        self.formLayout_5.setObjectName("formLayout_5")
        self.mapaCamaraWidget = QtWidgets.QWidget(self.ubicacionCamaraGeneral)
        self.mapaCamaraWidget.setObjectName("mapaCamaraWidget")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.mapaCamaraWidget)
        self.verticalLayout_13.addWidget(self.ubicacionCamaraGeneral)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_15.addWidget(self.scrollArea_2)
        self.agregarCamaraBtn = QtWidgets.QPushButton(self.agregarCamaraPage)
        self.agregarCamaraBtn.setObjectName("agregarCamaraBtn")
        self.verticalLayout_15.addWidget(self.agregarCamaraBtn)
        self.stackedWidget.addWidget(self.agregarCamaraPage)
        self.registrosPage = QtWidgets.QWidget()
        self.registrosPage.setObjectName("registrosPage")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.registrosPage)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.registrosTitulo = QtWidgets.QLabel(self.registrosPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.registrosTitulo.setFont(font)
        self.registrosTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.registrosTitulo.setObjectName("registrosTitulo")
        self.verticalLayout_3.addWidget(self.registrosTitulo)
        self.registrosTable = QtWidgets.QTableView(self.registrosPage)
        self.registrosTable.setAlternatingRowColors(True)
        self.registrosTable.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.registrosTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.registrosTable.setObjectName("registrosTable")
        self.verticalLayout_3.addWidget(self.registrosTable)
        self.verDetallesRegistroBtn = QtWidgets.QPushButton(self.registrosPage)
        self.verDetallesRegistroBtn.setObjectName("verDetallesRegistroBtn")
        self.verticalLayout_3.addWidget(self.verDetallesRegistroBtn)
        self.stackedWidget.addWidget(self.registrosPage)
        self.detallesRegistroPage = QtWidgets.QWidget()
        self.detallesRegistroPage.setObjectName("detallesRegistroPage")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.detallesRegistroPage)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.detallesTitulo = QtWidgets.QLabel(self.detallesRegistroPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.detallesTitulo.setFont(font)
        self.detallesTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.detallesTitulo.setObjectName("detallesTitulo")
        self.verticalLayout_4.addWidget(self.detallesTitulo)
        self.videoFrame = QtWidgets.QFrame(self.detallesRegistroPage)
        self.videoFrame.setMinimumSize(QtCore.QSize(0, 200))
        self.videoFrame.setStyleSheet("background-color: #222224; border: 1px solid #444444;")
        self.videoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoFrame.setObjectName("videoFrame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.videoFrame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.videoLabel = QtWidgets.QLabel(self.videoFrame)
        self.videoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.videoLabel.setObjectName("videoLabel")
        self.verticalLayout_10.addWidget(self.videoLabel)
        self.verticalLayout_4.addWidget(self.videoFrame)
        self.detallesGroupBox = QtWidgets.QGroupBox(self.detallesRegistroPage)
        self.detallesGroupBox.setObjectName("detallesGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.detallesGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.fechaLabel = QtWidgets.QLabel(self.detallesGroupBox)
        self.fechaLabel.setObjectName("fechaLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.fechaLabel)
        self.fechaValor = QtWidgets.QLabel(self.detallesGroupBox)
        self.fechaValor.setObjectName("fechaValor")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fechaValor)
        self.archivoLabel = QtWidgets.QLabel(self.detallesGroupBox)
        self.archivoLabel.setObjectName("archivoLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.archivoLabel)
        self.archivoValor = QtWidgets.QLabel(self.detallesGroupBox)
        self.archivoValor.setObjectName("archivoValor")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.archivoValor)
        self.localizacionLabel = QtWidgets.QLabel(self.detallesGroupBox)
        self.localizacionLabel.setObjectName("localizacionLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.localizacionLabel)
        self.localizacionValor = QtWidgets.QLabel(self.detallesGroupBox)
        self.localizacionValor.setObjectName("localizacionValor")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.localizacionValor)
        self.descripcionLabel = QtWidgets.QLabel(self.detallesGroupBox)
        self.descripcionLabel.setObjectName("descripcionLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.descripcionLabel)
        self.descripcionValor = QtWidgets.QLabel(self.detallesGroupBox)
        self.descripcionValor.setObjectName("descripcionValor")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.descripcionValor)
        self.verticalLayout_4.addWidget(self.detallesGroupBox)
        self.stackedWidget.addWidget(self.detallesRegistroPage)
        self.subirVideoPage = QtWidgets.QWidget()
        self.subirVideoPage.setObjectName("subirVideoPage")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.subirVideoPage)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.subirVideoTitulo = QtWidgets.QLabel(self.subirVideoPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.subirVideoTitulo.setFont(font)
        self.subirVideoTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.subirVideoTitulo.setObjectName("subirVideoTitulo")
        self.verticalLayout_5.addWidget(self.subirVideoTitulo)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.archivoSeleccionadoLabel = QtWidgets.QLabel(self.subirVideoPage)
        self.archivoSeleccionadoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.archivoSeleccionadoLabel.setObjectName("archivoSeleccionadoLabel")
        self.verticalLayout_5.addWidget(self.archivoSeleccionadoLabel)
        self.seleccionarVideoBtn = QtWidgets.QPushButton(self.subirVideoPage)
        self.seleccionarVideoBtn.setObjectName("seleccionarVideoBtn")
        self.verticalLayout_5.addWidget(self.seleccionarVideoBtn)
        self.accionesBotonesFrame = QtWidgets.QFrame(self.subirVideoPage)
        self.accionesBotonesFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.accionesBotonesFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.accionesBotonesFrame.setObjectName("accionesBotonesFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.accionesBotonesFrame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.subirVideoBtn = QtWidgets.QPushButton(self.accionesBotonesFrame)
        self.subirVideoBtn.setEnabled(True)
        self.subirVideoBtn.setObjectName("subirVideoBtn")
        self.horizontalLayout_2.addWidget(self.subirVideoBtn)
        self.cancelarSubidaBtn = QtWidgets.QPushButton(self.accionesBotonesFrame)
        self.cancelarSubidaBtn.setObjectName("cancelarSubidaBtn")
        self.horizontalLayout_2.addWidget(self.cancelarSubidaBtn)
        self.verticalLayout_5.addWidget(self.accionesBotonesFrame)
        self.vistaPreviaVideo = QtWidgets.QLabel(self.subirVideoPage)
        self.vistaPreviaVideo.setMinimumSize(QtCore.QSize(320, 180))
        self.vistaPreviaVideo.setFrameShape(QtWidgets.QFrame.Box)
        self.vistaPreviaVideo.setAlignment(QtCore.Qt.AlignCenter)
        self.vistaPreviaVideo.setObjectName("vistaPreviaVideo")
        self.verticalLayout_5.addWidget(self.vistaPreviaVideo)
        self.grupoDetecciones = QtWidgets.QGroupBox(self.subirVideoPage)
        self.grupoDetecciones.setObjectName("grupoDetecciones")
        self.verticalLayoutDetecciones = QtWidgets.QVBoxLayout(self.grupoDetecciones)
        self.verticalLayoutDetecciones.setObjectName("verticalLayoutDetecciones")
        self.scrollDetecciones = QtWidgets.QScrollArea(self.grupoDetecciones)
        self.scrollDetecciones.setWidgetResizable(True)
        self.scrollDetecciones.setObjectName("scrollDetecciones")
        self.scrollAreaContenido = QtWidgets.QWidget()
        self.scrollAreaContenido.setGeometry(QtCore.QRect(0, 0, 730, 85))
        self.scrollAreaContenido.setObjectName("scrollAreaContenido")
        self.layoutContenidoDetecciones = QtWidgets.QVBoxLayout(self.scrollAreaContenido)
        self.layoutContenidoDetecciones.setObjectName("layoutContenidoDetecciones")
        self.deteccionEjemplo = QtWidgets.QLabel(self.scrollAreaContenido)
        self.deteccionEjemplo.setObjectName("deteccionEjemplo")
        self.layoutContenidoDetecciones.addWidget(self.deteccionEjemplo)
        self.scrollDetecciones.setWidget(self.scrollAreaContenido)
        self.verticalLayoutDetecciones.addWidget(self.scrollDetecciones)
        self.verticalLayout_5.addWidget(self.grupoDetecciones)
        self.descargarDeteccionesBtn = QtWidgets.QPushButton(self.subirVideoPage)
        self.descargarDeteccionesBtn.setObjectName("descargarDeteccionesBtn")
        self.verticalLayout_5.addWidget(self.descargarDeteccionesBtn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.subirVideoPage)
        self.mapaPage = QtWidgets.QWidget()
        self.mapaPage.setObjectName("mapaPage")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.mapaPage)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.mapaTitulo = QtWidgets.QLabel(self.mapaPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapaTitulo.sizePolicy().hasHeightForWidth())
        self.mapaTitulo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.mapaTitulo.setFont(font)
        self.mapaTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.mapaTitulo.setObjectName("mapaTitulo")
        self.verticalLayout_14.addWidget(self.mapaTitulo)
        self.mapaWidget = QtWidgets.QWidget(self.mapaPage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mapaWidget.sizePolicy().hasHeightForWidth())
        self.mapaWidget.setSizePolicy(sizePolicy)
        self.mapaWidget.setObjectName("mapaWidget")
        self.verticalLayout_14.addWidget(self.mapaWidget)
        self.stackedWidget.addWidget(self.mapaPage)
        self.configuracionPage = QtWidgets.QWidget()
        self.configuracionPage.setObjectName("configuracionPage")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.configuracionPage)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.configuracionTitulo = QtWidgets.QLabel(self.configuracionPage)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.configuracionTitulo.setFont(font)
        self.configuracionTitulo.setAlignment(QtCore.Qt.AlignCenter)
        self.configuracionTitulo.setObjectName("configuracionTitulo")
        self.verticalLayout_11.addWidget(self.configuracionTitulo)
        self.scrollArea = QtWidgets.QScrollArea(self.configuracionPage)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 754, 457))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.configuracionGeneral = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.configuracionGeneral.setObjectName("configuracionGeneral")
        self.formLayout_2 = QtWidgets.QFormLayout(self.configuracionGeneral)
        self.formLayout_2.setObjectName("formLayout_2")
        self.rutaAlmacenamientoLabel = QtWidgets.QLabel(self.configuracionGeneral)
        self.rutaAlmacenamientoLabel.setObjectName("rutaAlmacenamientoLabel")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rutaAlmacenamientoLabel)
        self.rutaAlmacenamientoEdit = QtWidgets.QLineEdit(self.configuracionGeneral)
        self.rutaAlmacenamientoEdit.setObjectName("rutaAlmacenamientoEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rutaAlmacenamientoEdit)
        self.formatoVideoLabel = QtWidgets.QLabel(self.configuracionGeneral)
        self.formatoVideoLabel.setObjectName("formatoVideoLabel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.formatoVideoLabel)
        self.formatoVideoCombo = QtWidgets.QComboBox(self.configuracionGeneral)
        self.formatoVideoCombo.setObjectName("formatoVideoCombo")
        self.formatoVideoCombo.addItem("")
        self.formatoVideoCombo.addItem("")
        self.formatoVideoCombo.addItem("")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.formatoVideoCombo)
        self.tiempoGrabacionLabel = QtWidgets.QLabel(self.configuracionGeneral)
        self.tiempoGrabacionLabel.setObjectName("tiempoGrabacionLabel")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.tiempoGrabacionLabel)
        self.tiempoGrabacionSpin = QtWidgets.QSpinBox(self.configuracionGeneral)
        self.tiempoGrabacionSpin.setMinimum(5)
        self.tiempoGrabacionSpin.setMaximum(300)
        self.tiempoGrabacionSpin.setProperty("value", 30)
        self.tiempoGrabacionSpin.setObjectName("tiempoGrabacionSpin")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.tiempoGrabacionSpin)
        self.verticalLayout_12.addWidget(self.configuracionGeneral)
        self.configuracionDeteccion = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.configuracionDeteccion.setObjectName("configuracionDeteccion")
        self.formLayout_3 = QtWidgets.QFormLayout(self.configuracionDeteccion)
        self.formLayout_3.setObjectName("formLayout_3")
        self.sensibilidadLabel = QtWidgets.QLabel(self.configuracionDeteccion)
        self.sensibilidadLabel.setObjectName("sensibilidadLabel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.sensibilidadLabel)
        self.sensibilidadSlider = QtWidgets.QSlider(self.configuracionDeteccion)
        self.sensibilidadSlider.setOrientation(QtCore.Qt.Horizontal)
        self.sensibilidadSlider.setObjectName("sensibilidadSlider")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.sensibilidadSlider)
        self.grabarAnteriorLabel = QtWidgets.QLabel(self.configuracionDeteccion)
        self.grabarAnteriorLabel.setObjectName("grabarAnteriorLabel")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.grabarAnteriorLabel)
        self.grabarAnteriorSpin = QtWidgets.QSpinBox(self.configuracionDeteccion)
        self.grabarAnteriorSpin.setMinimum(1)
        self.grabarAnteriorSpin.setMaximum(60)
        self.grabarAnteriorSpin.setProperty("value", 10)
        self.grabarAnteriorSpin.setObjectName("grabarAnteriorSpin")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.grabarAnteriorSpin)
        self.notificacionesLabel = QtWidgets.QLabel(self.configuracionDeteccion)
        self.notificacionesLabel.setObjectName("notificacionesLabel")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.notificacionesLabel)
        self.notificacionesCheck = QtWidgets.QCheckBox(self.configuracionDeteccion)
        self.notificacionesCheck.setText("")
        self.notificacionesCheck.setChecked(True)
        self.notificacionesCheck.setObjectName("notificacionesCheck")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.notificacionesCheck)
        self.verticalLayout_12.addWidget(self.configuracionDeteccion)
        self.configuracionRTSP = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.configuracionRTSP.setObjectName("configuracionRTSP")
        self.formLayout_4 = QtWidgets.QFormLayout(self.configuracionRTSP)
        self.formLayout_4.setObjectName("formLayout_4")
        self.rtspPuertoLabel = QtWidgets.QLabel(self.configuracionRTSP)
        self.rtspPuertoLabel.setObjectName("rtspPuertoLabel")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.rtspPuertoLabel)
        self.rtspPuertoEdit = QtWidgets.QLineEdit(self.configuracionRTSP)
        self.rtspPuertoEdit.setObjectName("rtspPuertoEdit")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rtspPuertoEdit)
        self.usuarioPredeterminadoLabel = QtWidgets.QLabel(self.configuracionRTSP)
        self.usuarioPredeterminadoLabel.setObjectName("usuarioPredeterminadoLabel")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.usuarioPredeterminadoLabel)
        self.usuarioPredeterminadoEdit = QtWidgets.QLineEdit(self.configuracionRTSP)
        self.usuarioPredeterminadoEdit.setObjectName("usuarioPredeterminadoEdit")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.usuarioPredeterminadoEdit)
        self.passwordPredeterminadoLabel = QtWidgets.QLabel(self.configuracionRTSP)
        self.passwordPredeterminadoLabel.setObjectName("passwordPredeterminadoLabel")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.passwordPredeterminadoLabel)
        self.passwordPredeterminadoEdit = QtWidgets.QLineEdit(self.configuracionRTSP)
        self.passwordPredeterminadoEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordPredeterminadoEdit.setObjectName("passwordPredeterminadoEdit")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.passwordPredeterminadoEdit)
        self.verticalLayout_12.addWidget(self.configuracionRTSP)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_11.addWidget(self.scrollArea)
        self.guardarConfiguracionBtn = QtWidgets.QPushButton(self.configuracionPage)
        self.guardarConfiguracionBtn.setObjectName("guardarConfiguracionBtn")
        self.verticalLayout_11.addWidget(self.guardarConfiguracionBtn)
        self.stackedWidget.addWidget(self.configuracionPage)
        self.camaraGrandePage = QtWidgets.QWidget()
        self.camaraGrandePage.setObjectName("camaraGrandePage")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.camaraGrandePage)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.videoFrame_2 = QtWidgets.QFrame(self.camaraGrandePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoFrame_2.sizePolicy().hasHeightForWidth())
        self.videoFrame_2.setSizePolicy(sizePolicy)
        self.videoFrame_2.setMinimumSize(QtCore.QSize(0, 200))
        self.videoFrame_2.setStyleSheet("background-color: #222224; border: 1px solid #444444;")
        self.videoFrame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.videoFrame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.videoFrame_2.setObjectName("videoFrame_2")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.videoFrame_2)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.videoLabel_2 = QtWidgets.QLabel(self.videoFrame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.videoLabel_2.sizePolicy().hasHeightForWidth())
        self.videoLabel_2.setSizePolicy(sizePolicy)
        self.videoLabel_2.setText("")
        self.videoLabel_2.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.videoLabel_2.setObjectName("videoLabel_2")
        self.verticalLayout_16.addWidget(self.videoLabel_2)
        self.verticalLayout_17.addWidget(self.videoFrame_2)
        self.stackedWidget.addWidget(self.camaraGrandePage)
        self.verticalLayout.addWidget(self.stackedWidget)
        self.navegacionFrame = QtWidgets.QFrame(self.centralwidget)
        self.navegacionFrame.setMinimumSize(QtCore.QSize(0, 50))
        self.navegacionFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.navegacionFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.navegacionFrame.setObjectName("navegacionFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.navegacionFrame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verCamarasBtn = QtWidgets.QPushButton(self.navegacionFrame)
        self.verCamarasBtn.setObjectName("verCamarasBtn")
        self.horizontalLayout.addWidget(self.verCamarasBtn)
        self.verRegistrosBtn = QtWidgets.QPushButton(self.navegacionFrame)
        self.verRegistrosBtn.setObjectName("verRegistrosBtn")
        self.horizontalLayout.addWidget(self.verRegistrosBtn)
        self.subirVideoBtn_nav = QtWidgets.QPushButton(self.navegacionFrame)
        self.subirVideoBtn_nav.setObjectName("subirVideoBtn_nav")
        self.horizontalLayout.addWidget(self.subirVideoBtn_nav)
        self.MapaBtn = QtWidgets.QPushButton(self.navegacionFrame)
        self.MapaBtn.setObjectName("MapaBtn")
        self.horizontalLayout.addWidget(self.MapaBtn)
        self.configuracionBtn = QtWidgets.QPushButton(self.navegacionFrame)
        self.configuracionBtn.setObjectName("configuracionBtn")
        self.horizontalLayout.addWidget(self.configuracionBtn)
        self.salirBtn = QtWidgets.QPushButton(self.navegacionFrame)
        self.salirBtn.setObjectName("salirBtn")
        self.horizontalLayout.addWidget(self.salirBtn)
        self.verticalLayout.addWidget(self.navegacionFrame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.verCamarasBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.verRegistrosBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.subirVideoBtn_nav.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(4))
        self.MapaBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.configuracionBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.salirBtn.clicked.connect(lambda: sys.exit())
        self.agregarCamara1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamara2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamara3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamara4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamaraBtn.clicked.connect(self.agregarCamara)
        self.setupMapa()
        self.setupMapaInteractivo()
        self.cargar_camara_guardada()
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sistema de Detección de Accidentes"))
        self.camarasTitulo.setText(_translate("MainWindow", "Vista de Cámaras"))
        self.agregarCamara1.setText(_translate("MainWindow", "+"))
        self.agregarCamara2.setText(_translate("MainWindow", "+"))
        self.agregarCamara3.setText(_translate("MainWindow", "+"))
        self.agregarCamara4.setText(_translate("MainWindow", "+"))
        self.agregarCamaraTitulo.setText(_translate("MainWindow", "Agregar Camara"))
        self.configuracionRTSP_2.setTitle(_translate("MainWindow", "Configuración RTSP Predeterminada"))
        self.direccionIpLabel.setText(_translate("MainWindow", "Dirección IP:"))
        self.direccionIpEdit.setPlaceholderText(_translate("MainWindow", "192.168.1.30"))
        self.rtspPuertoLabel_2.setText(_translate("MainWindow", "Puerto RTSP Predeterminado:"))
        self.rtspPuertoEdit_2.setText(_translate("MainWindow", "554"))
        self.usuarioPredeterminadoLabel_2.setText(_translate("MainWindow", "Usuario:"))
        self.usuarioEdit.setText(_translate("MainWindow", "admin"))
        self.passwordPredeterminadoLabel_2.setText(_translate("MainWindow", "Contraseña:"))
        self.passwordEdit.setText(_translate("MainWindow", "admin"))
        self.ubicacionCamaraGeneral.setTitle(_translate("MainWindow", "Ubicacion De la Camara"))
        self.agregarCamaraBtn.setText(_translate("MainWindow", "Agregar Camara"))
        self.registrosTitulo.setText(_translate("MainWindow", "Vista de Registros"))
        self.verDetallesRegistroBtn.setText(_translate("MainWindow", "Ver Detalles del Registro Seleccionado"))
        self.detallesTitulo.setText(_translate("MainWindow", "Detalles del Registro"))
        self.videoLabel.setText(_translate("MainWindow", "Video del Accidente"))
        self.detallesGroupBox.setTitle(_translate("MainWindow", "Información del Registro"))
        self.fechaLabel.setText(_translate("MainWindow", "Fecha del Accidente:"))
        self.fechaValor.setText(_translate("MainWindow", "[Fecha]"))
        self.archivoLabel.setText(_translate("MainWindow", "Nombre del Archivo:"))
        self.archivoValor.setText(_translate("MainWindow", "[Archivo]"))
        self.localizacionLabel.setText(_translate("MainWindow", "Localización:"))
        self.localizacionValor.setText(_translate("MainWindow", "[Localización]"))
        self.descripcionLabel.setText(_translate("MainWindow", "Descripción:"))
        self.descripcionValor.setText(_translate("MainWindow", "[Descripción]"))
        self.subirVideoTitulo.setText(_translate("MainWindow", "Subir Video"))
        self.archivoSeleccionadoLabel.setText(_translate("MainWindow", "Ningún archivo seleccionado"))
        self.seleccionarVideoBtn.setText(_translate("MainWindow", "Seleccionar Video..."))
        self.subirVideoBtn.setText(_translate("MainWindow", "Continuar"))
        self.cancelarSubidaBtn.setText(_translate("MainWindow", "Cancelar"))
        self.vistaPreviaVideo.setText(_translate("MainWindow", "Vista previa del video"))
        self.grupoDetecciones.setTitle(_translate("MainWindow", "Detecciones"))
        self.deteccionEjemplo.setText(_translate("MainWindow", "Ejemplo: Accidente detectado en el segundo 12"))
        self.descargarDeteccionesBtn.setText(_translate("MainWindow", "Descargar Resultados"))
        self.mapaTitulo.setText(_translate("MainWindow", "Mapa"))
        self.configuracionTitulo.setText(_translate("MainWindow", "Configuración del Sistema"))
        self.configuracionGeneral.setTitle(_translate("MainWindow", "Configuración General"))
        self.rutaAlmacenamientoLabel.setText(_translate("MainWindow", "Ruta de Almacenamiento:"))
        self.formatoVideoLabel.setText(_translate("MainWindow", "Formato de Video Preferido:"))
        self.formatoVideoCombo.setItemText(0, _translate("MainWindow", "MP4"))
        self.formatoVideoCombo.setItemText(1, _translate("MainWindow", "AVI"))
        self.formatoVideoCombo.setItemText(2, _translate("MainWindow", "MKV"))
        self.tiempoGrabacionLabel.setText(_translate("MainWindow", "Tiempo de Grabación (segundos):"))
        self.configuracionDeteccion.setTitle(_translate("MainWindow", "Configuración de Detección"))
        self.sensibilidadLabel.setText(_translate("MainWindow", "Sensibilidad de Detección:"))
        self.grabarAnteriorLabel.setText(_translate("MainWindow", "Grabar segundos previos al accidente:"))
        self.notificacionesLabel.setText(_translate("MainWindow", "Activar Notificaciones:"))
        self.configuracionRTSP.setTitle(_translate("MainWindow", "Configuración RTSP Predeterminada"))
        self.rtspPuertoLabel.setText(_translate("MainWindow", "Puerto RTSP Predeterminado:"))
        self.rtspPuertoEdit.setText(_translate("MainWindow", "554"))
        self.usuarioPredeterminadoLabel.setText(_translate("MainWindow", "Usuario Predeterminado:"))
        self.usuarioPredeterminadoEdit.setText(_translate("MainWindow", "admin"))
        self.passwordPredeterminadoLabel.setText(_translate("MainWindow", "Contraseña Predeterminada:"))
        self.passwordPredeterminadoEdit.setText(_translate("MainWindow", "admin"))
        self.guardarConfiguracionBtn.setText(_translate("MainWindow", "Guardar Configuración"))
        self.verCamarasBtn.setText(_translate("MainWindow", "Ver Cámaras"))
        self.verRegistrosBtn.setText(_translate("MainWindow", "Ver Registros"))
        self.subirVideoBtn_nav.setText(_translate("MainWindow", "Subir Video"))
        self.MapaBtn.setText(_translate("MainWindow", "Mapa"))
        self.configuracionBtn.setText(_translate("MainWindow", "Configuración"))
        self.salirBtn.setText(_translate("MainWindow", "Salir"))



    def setupMapa(self):
        from PyQt5 import QtWebEngineWidgets, QtWidgets

        # Consulta la cámara para obtener latitud/longitud
        cam = self.consultar_camara()
        if not cam:
            print("No se encontró cámara para mostrar en el mapa.")
            return

        lat = float(cam['latitud'])
        lon = float(cam['longitud'])

        # Crear el QWebEngineView dentro de mapaWidget
        self.webview = QtWebEngineWidgets.QWebEngineView(self.mapaWidget)
        layout = QtWidgets.QVBoxLayout(self.mapaWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.webview)

        # HTML con Leaflet, centrándose en la cámara y añadiendo un marker
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Mapa Cámara</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                html, body, #map {{
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                // Inicializar mapa centrado en la cámara
                var cameraLat = {lat};
                var cameraLon = {lon};
                var map = L.map('map').setView([cameraLat, cameraLon], 16);

                // Capa base
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: 'Map data © OpenStreetMap contributors'
                }}).addTo(map);

                // Añadir marcador para la cámara
                L.marker([cameraLat, cameraLon])
                  .addTo(map)
                  .bindPopup('Cámara ID: {cam["id"]}')
                  .openPopup();
            </script>
        </body>
        </html>
        '''

        # Cargar el HTML en el webview
        self.webview.setHtml(html)


    def setupMapaInteractivo(self):
        from PyQt5 import QtWebEngineWidgets, QtWidgets

        layout = QtWidgets.QVBoxLayout(self.mapaCamaraWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.webview = QtWebEngineWidgets.QWebEngineView(self.mapaCamaraWidget)
        layout.addWidget(self.webview)
        self.webview.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)

        html = '''
        <!DOCTYPE html>
        <html><head>
          <meta charset="utf-8" />
          <title>Mapa Bogotá</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
          <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
          <style> html, body, #map { height:100%; margin:0; padding:0; } </style>
        </head><body>
          <div id="map"></div>
          <script>
            var marker = null;
            var map = L.map('map').setView([4.7110, -74.0721], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
              attribution: 'Map data © OpenStreetMap contributors'
            }).addTo(map);

            map.on('click', function(e) {
              var lat = e.latlng.lat, lng = e.latlng.lng;
              if (marker) map.removeLayer(marker);
              marker = L.marker([lat, lng]).addTo(map);
            });

            // Función que Python invoca para obtener coords
            function getLastLatLng() {
              if (!marker) return null;
              return { lat: marker.getLatLng().lat, lng: marker.getLatLng().lng };
            }
          </script>
        </body></html>
        '''

        self.webview.setHtml(html)
        self.mapaCamaraWidget.resizeEvent = self.adjust_map_size

    def adjust_map_size(self, event):
        # Ajustar el tamaño del webview al tamaño del widget contenedor
        self.webview.resize(self.mapaCamaraWidget.size())

    def agregarCamara(self):
        # 1) Leer campos
        ip   = self.direccionIpEdit.text().strip()
        port = self.rtspPuertoEdit_2.text().strip()
        user = self.usuarioEdit.text().strip()
        pwd  = self.passwordEdit.text().strip()

        if not all([ip, port, user, pwd]):
            QtWidgets.QMessageBox.warning(None, "Datos incompletos",
                "Debes llenar IP, puerto, usuario y contraseña.")
            return

        # 2) Ejecutar JS para obtener coordenadas desde el mapa
        self.webview.page().runJavaScript("getLastLatLng();", lambda res: self._onGotCoords(res, ip, port, user, pwd))
        
    def _onGotCoords(self, res, ip, port, user, pwd):
        print("Entró a _onGotCoords")
        if not res:
            print("No hay coordenadas, muestra advertencia y sale")
            QtWidgets.QMessageBox.warning(
                None,
                "Sin ubicación",
                "Primero selecciona la posición en el mapa."
            )
            return

        lat = res['lat']
        lng = res['lng']
        print(f"Latitud recibida: {lat} ({type(lat)})")
        print(f"Longitud recibida: {lng} ({type(lng)})")

        puerto = str(port)  # 🔧 Asegúrate de que sea string

        rtsp_url = f"rtsp://{user}:{pwd}@{ip}:{puerto}/Streaming/Channels/101"
        print(f"URL RTSP construida: {rtsp_url}")

        # Guardar en base de datos
        guardar_camara(ip, puerto, user, pwd, lat, lng, rtsp_url)
        
        QtWidgets.QMessageBox.information(
            None,
            "URL RTSP",
            f"Intentando conectar a:\n{rtsp_url}"
        )

        try:
            print("Preparando layout de camara1Frame")
            if not self.camara1Frame.layout():
                print("No hay layout, creando uno nuevo QVBoxLayout")
                self.camara1Frame.setLayout(QtWidgets.QVBoxLayout())

            layout1 = self.camara1Frame.layout()
            for i in reversed(range(layout1.count())):
                w = layout1.itemAt(i).widget()
                if w:
                    print("Eliminando widget previo del layout")
                    w.setParent(None)

            print("Creando QLabel para video en camara1Frame")
            self.video_label = QtWidgets.QLabel()
            # 1) Política expansiva para ocupar todo el espacio
            self.video_label.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding
            )
            # 2) Tamaño mínimo para que el escalado funcione correctamente
            self.video_label.setMinimumSize(1, 1)
            # 3) Centrar el contenido del video dentro del QLabel
            self.video_label.setAlignment(QtCore.Qt.AlignCenter)
            # 4) Fondo negro (sin setScaledContents aquí)
            self.video_label.setStyleSheet("background-color: black;")
            layout1.addWidget(self.video_label)

            # Iniciar o reutilizar el stream RTSP para camara1Frame sin agrandar el frame
            if hasattr(self, 'rtsp_thread') and self.rtsp_thread and self.rtsp_thread.isRunning():
                print("Hilo RTSP ya corriendo, solo reconectando señal para camara1Frame")
                try:
                    self.rtsp_thread.change_pixmap.disconnect()
                except Exception:
                    pass
                self.rtsp_thread.change_pixmap.connect(
                    lambda img: self.video_label.setPixmap(
                        QtGui.QPixmap.fromImage(img)
                            .scaled(
                                self.video_label.size(),
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.SmoothTransformation
                            )
                    )
                )
            else:
                print("Iniciando nuevo hilo RTSP")
                self._start_rtsp_stream(rtsp_url, self.video_label)

        except Exception:
            err_text = traceback.format_exc()
            print("Error al preparar o iniciar stream:")
            print(err_text)
            QtWidgets.QMessageBox.critical(
                None,
                "Error al iniciar Stream",
                f"{err_text}"
            )
            return

        self.camara1Frame.mouseDoubleClickEvent = self._onCam1DoubleClick
        print("Se asignó evento mouseDoubleClick a camara1Frame")

        QtWidgets.QMessageBox.information(
            None,
            "¡Éxito!",
            f"Cámara conectada y reproducida en camara1Frame.\n"
            f"Ubicación: ({lat:.5f}, {lng:.5f})"
        )
        print("Fin de _onGotCoords")


    def _start_rtsp_stream(self, rtsp_url, target_label):
        print(f"Entró a _start_rtsp_stream con URL: {rtsp_url}")
        if hasattr(self, 'rtsp_thread') and self.rtsp_thread and self.rtsp_thread.isRunning():
            print("Deteniendo hilo RTSP anterior")
            self.rtsp_thread.stop()

        # Asegúrate de que StreamThread esté bien definida y fuera de cualquier método
        self.rtsp_thread = StreamThread(rtsp_url)

        # Conectar las señales correctamente
        self.rtsp_thread.change_pixmap.connect(
            lambda img: self._update_video_label(img, target_label)
        )

        self.rtsp_thread.connection_failed.connect(
            lambda msg: QtWidgets.QMessageBox.critical(None, "Error de conexión RTSP", msg)
        )

        self.rtsp_thread.start()
        print("Hilo RTSP iniciado")

    def _update_video_label(self, img, label):
        """Función centralizada para actualizar etiquetas de video con mejor rendimiento"""
        pixmap = QtGui.QPixmap.fromImage(img)

        # Optimización: solo escalar si es necesario
        if pixmap.width() > label.width() or pixmap.height() > label.height():
            pixmap = pixmap.scaled(
                label.size(),
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )

        label.setPixmap(pixmap)


    def _onCam1DoubleClick(self, event):
        print("Doble click en camara1Frame detectado")
        if event.button() != QtCore.Qt.LeftButton:
            print("No es click izquierdo, ignora")
            return

        self.stackedWidget.setCurrentIndex(7)
        print("Cambiado stackedWidget a índice 7")

        if not self.videoFrame_2.layout():
            print("Creando layout para videoFrame_2")
            self.videoFrame_2.setLayout(QtWidgets.QVBoxLayout())

        layout2 = self.videoFrame_2.layout()
        for i in reversed(range(layout2.count())):
            w = layout2.itemAt(i).widget()
            if w:
                print("Eliminando widget previo de videoFrame_2")
                w.setParent(None)

        print("Creando QLabel para videoFrame_2")
        self.video_label_2 = QtWidgets.QLabel()
        self.video_label_2.setStyleSheet("background-color: black;")
        self.video_label_2.setAlignment(QtCore.Qt.AlignCenter)  # Centrar contenido
        self.video_label_2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        layout2.addWidget(self.video_label_2)

        print("Asignando evento mouseDoubleClick a video_label_2 para volver a camara1Frame")
        self.video_label_2.mouseDoubleClickEvent = self._onVideoLabel2DoubleClick

        print("Reusando hilo RTSP y reconectando señal para videoFrame_2")
        try:
            if hasattr(self, 'rtsp_thread') and self.rtsp_thread and self.rtsp_thread.isRunning():
                try:
                    self.rtsp_thread.change_pixmap.disconnect()
                except Exception:
                    pass
                self.rtsp_thread.change_pixmap.connect(
                    lambda img: self._update_video_label(img, self.video_label_2)
                )
            else:
                print("No hay hilo RTSP activo, no se puede mostrar videoFrame_2")
        except Exception as e:
            print(f"Error reconectando señal: {e}")

        print("Fin de _onCam1DoubleClick")


    def _onVideoLabel2DoubleClick(self, event):
        print("Doble click en video_label_2 detectado")
        if event.button() != QtCore.Qt.LeftButton:
            print("No es click izquierdo, ignora")
            return

        self.stackedWidget.setCurrentIndex(0)
        print("Cambiado stackedWidget a índice 0")

        if not self.camara1Frame.layout():
            print("No hay layout en camara1Frame, creando uno")
            self.camara1Frame.setLayout(QtWidgets.QVBoxLayout())

        layout1 = self.camara1Frame.layout()
        for i in reversed(range(layout1.count())):
            w = layout1.itemAt(i).widget()
            if w:
                print("Eliminando widget previo en camara1Frame")
                w.setParent(None)

        print("Creando QLabel para video en camara1Frame")
        self.video_label = QtWidgets.QLabel()
        self.video_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.video_label.setMinimumSize(1, 1)
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)  # Centrar contenido
        layout1.addWidget(self.video_label)

        print("Reusando hilo RTSP y reconectando señal para camara1Frame")
        try:
            if hasattr(self, 'rtsp_thread') and self.rtsp_thread and self.rtsp_thread.isRunning():
                try:
                    self.rtsp_thread.change_pixmap.disconnect()
                except Exception:
                    pass
                self.rtsp_thread.change_pixmap.connect(
                    lambda img: self._update_video_label(img, self.video_label)
                )
            else:
                print("No hay hilo RTSP activo para mostrar en camara1Frame")
        except Exception as e:
            print(f"Error reconectando señal: {e}")

        self.camara1Frame.mouseDoubleClickEvent = self._onCam1DoubleClick
        print("Evento mouseDoubleClick reasignado a camara1Frame")

        print("Fin de _onVideoLabel2DoubleClick")


    def _onVerCamarasClicked(self):
        print("Botón verCamaras presionado, volviendo a índice 0 y mostrando camara1Frame")

        self.stackedWidget.setCurrentIndex(0)

        try:
            if not hasattr(self, 'last_rtsp_url'):
                print("No se encontró URL RTSP previa para mostrar stream.")
                return

            if not self.camara1Frame.layout():
                print("No hay layout en camara1Frame, creando uno")
                self.camara1Frame.setLayout(QtWidgets.QVBoxLayout())

            layout1 = self.camara1Frame.layout()
            for i in reversed(range(layout1.count())):
                w = layout1.itemAt(i).widget()
                if w:
                    print("Eliminando widget previo en camara1Frame")
                    w.setParent(None)

            print("Creando QLabel para video en camara1Frame")
            self.video_label = QtWidgets.QLabel()
            self.video_label.setSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Expanding
            )
            self.video_label.setMinimumSize(1, 1)
            self.video_label.setAlignment(QtCore.Qt.AlignCenter)
            self.video_label.setStyleSheet("background-color: black;")
            layout1.addWidget(self.video_label)

            print("Reusando hilo RTSP y reconectando señal para camara1Frame")
            if hasattr(self, 'rtsp_thread') and self.rtsp_thread and self.rtsp_thread.isRunning():
                try:
                    self.rtsp_thread.change_pixmap.disconnect()
                except Exception:
                    pass
                self.rtsp_thread.change_pixmap.connect(
                    lambda img: self._update_video_label(img, self.video_label)
                )
            else:
                print("No hay hilo RTSP activo para mostrar en camara1Frame")
                self._start_rtsp_stream(self.last_rtsp_url, self.video_label)

            self.camara1Frame.mouseDoubleClickEvent = self._onCam1DoubleClick
            print("Evento mouseDoubleClick reasignado a camara1Frame")

        except Exception:
            err_text = traceback.format_exc()
            print("Error al mostrar stream en camara1Frame:")
            print(err_text)
            QtWidgets.QMessageBox.critical(
                None,
                "Error al mostrar Stream",
                f"{err_text}"
            )

