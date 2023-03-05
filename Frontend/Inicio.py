from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QFont
import parametros as p

window_name, base_class = uic.loadUiType(p.RUTA_UI_INICIO)

class VentanaInicio(window_name,base_class):

    senal_abrir_pago_diario = pyqtSignal()
    senal_abrir_pago_semanal = pyqtSignal()
    senal_abrir_balance = pyqtSignal()
    senal_abrir_asistencia = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.boton_pago_diario.clicked.connect(self.abrir_pago_diario)
        self.boton_pago_semanal.clicked.connect(self.abrir_pago_semanal)
        self.boton_balance.clicked.connect(self.abrir_balance)
        self.boton_asistencia.clicked.connect(self.abrir_asistencia)
        self.centralWidget().setContentsMargins(0,0,0,0)
        self.botones = [self.boton_pago_diario, self.boton_asistencia, self.boton_pago_semanal]
        self.style2 = "QPushButton{\ncolor:black; \ntext-align:left;\nmargin:0;\nbackground-color:#d9dde2;\nborder-radius:10;\n}\nQPushButton:hover{\nbackground-color:rgb(83, 82, 82);\n}"
        
    def select(self):
        style1 = "QPushButton{\ncolor:#dddcdf; \ntext-align:left;\nmargin:0;\nbackground-color:transparent;\nborder-radius:10;\n}\nQPushButton:hover{\nbackground-color:rgb(83, 82, 82);\n}"
        for boton in self.botones: boton.setStyleSheet(style1)

    def change_widget(self, new_widget):
        self.stack.setCurrentWidget(new_widget)
        new_widget.start()

    def mostrar(self):
        self.show()

    def abrir_pago_diario(self):
        self.select()
        self.boton_pago_diario.setStyleSheet(self.style2)
        self.senal_abrir_pago_diario.emit()

    def abrir_pago_semanal(self):
        self.select()
        self.boton_pago_semanal.setStyleSheet(self.style2)
        self.senal_abrir_pago_semanal.emit()

    def abrir_balance(self):
        #self.select()
        #self.boton_pago_d.setStyleSheet(self.style2)
        self.senal_abrir_balance.emit()

    def abrir_asistencia(self):
        self.select()
        self.boton_asistencia.setStyleSheet(self.style2)
        self.senal_abrir_asistencia.emit()