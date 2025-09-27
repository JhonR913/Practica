
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import QtWidgets, QtWebEngineWidgets, uic



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
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
        self.detallesRegistroBtn_nav = QtWidgets.QPushButton(self.navegacionFrame)
        self.detallesRegistroBtn_nav.setObjectName("detallesRegistroBtn_nav")
        self.horizontalLayout.addWidget(self.detallesRegistroBtn_nav)
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
        self.detallesRegistroBtn_nav.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(3))
        self.MapaBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(5))
        self.configuracionBtn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(6))
        self.salirBtn.clicked.connect(lambda: sys.exit())
        self.agregarCamara1.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamara2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamara3.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.agregarCamara4.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.setupMapa()
        self.setupMapaInteractivo()
        

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
        self.detallesRegistroBtn_nav.setText(_translate("MainWindow", "Detalles de Registro"))
        self.MapaBtn.setText(_translate("MainWindow", "Mapa"))
        self.configuracionBtn.setText(_translate("MainWindow", "Configuración"))
        self.salirBtn.setText(_translate("MainWindow", "Salir"))



    def setupMapa(self):
      from PyQt5 import QtWebEngineWidgets, QtWidgets

      # Crear el QWebEngineView
      self.webview = QtWebEngineWidgets.QWebEngineView(self.mapaWidget)

      # Crear un layout para que el webview ocupe todo el espacio del mapaWidget
      layout = QtWidgets.QVBoxLayout(self.mapaWidget)
      layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
      layout.addWidget(self.webview)

      # HTML para mostrar el mapa
      html = '''
      <!DOCTYPE html>
      <html>
      <head>
          <meta charset="utf-8" />
          <title>Mapa Bogotá</title>
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
          <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
          <style>
              html, body, #map {
                  height: 100%;
                  margin: 0;
                  padding: 0;
              }
          </style>
      </head>
      <body>
          <div id="map"></div>
          <script>
              var map = L.map('map').setView([4.7110, -74.0721], 13);  // Bogotá, Colombia
              L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                  attribution: 'Map data © OpenStreetMap contributors'
              }).addTo(map);
          </script>
      </body>
      </html>
      '''

      # Establecer el HTML al webview
      self.webview.setHtml(html)

    def setupMapaInteractivo(self):
        from PyQt5 import QtWebEngineWidgets, QtWidgets

        # Crear un layout para el mapa dentro de mapaCamaraWidget
        layout = QtWidgets.QVBoxLayout(self.mapaCamaraWidget)
        layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes

        # Crear el QWebEngineView para mostrar el mapa dentro de mapaCamaraWidget
        self.webview = QtWebEngineWidgets.QWebEngineView(self.mapaCamaraWidget)

        # Añadir el webview al layout
        layout.addWidget(self.webview)

        # HTML para mostrar el mapa y agregar un marcador interactivo
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8" />
            <title>Mapa Bogotá</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                html, body, #map {
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                var map = L.map('map').setView([4.7110, -74.0721], 13);  // Bogotá, Colombia

                // Capa base de OpenStreetMap
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: 'Map data © OpenStreetMap contributors'
                }).addTo(map);

                var marker = null;  // Variable para guardar el marcador

                // Evento de clic en el mapa para agregar un marcador
                map.on('click', function(e) {
                    var latlng = e.latlng;  // Obtener las coordenadas del clic
                    if (marker) {
                        // Si ya existe un marcador, lo eliminamos
                        map.removeLayer(marker);
                    }
                    // Colocamos un nuevo marcador en la ubicación donde se hizo clic
                    marker = L.marker(latlng).addTo(map);
                });
            </script>
        </body>
        </html>
        '''

        # Establecer el HTML al webview para mostrar el mapa interactivo
        self.webview.setHtml(html)

        # Asegurarse de que el webview ocupa todo el espacio del mapaCamaraWidget
        self.webview.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Ajustar el tamaño automáticamente del QWebEngineView al tamaño del widget contenedor
        self.mapaCamaraWidget.resizeEvent = self.adjust_map_size

    def adjust_map_size(self, event):
        # Ajustar el tamaño del webview al tamaño del widget contenedor
        self.webview.resize(self.mapaCamaraWidget.size())
